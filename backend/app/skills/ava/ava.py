import json
from datetime import date, timedelta
from typing import List

from dateutil.parser import parse
from loguru import logger

from app.core.breakers import bne_breaker, vcm_breaker
from app.core.config import REQUEST_TIMEOUT, RemoteConfig, get_config
from app.core.http import async_client, insecure_async_client
from app.core.tokens import StargateEnv, create_access_token
from app.models.domains.ava import (
    ABIbaagSection,
    AVABNEResult,
    AVATopicResponse,
    AVBNERequestStage,
    Query,
)
from app.models.skills import DomainsEnum, Input, SkillResult, Variant
from app.models.user import UserPublic
from app.skills import Skill


class AvaSkill(Skill):
    name = "AVA"
    alias = "ava"

    domains = [DomainsEnum.benefits]

    async def trigger_skill(self, req: Input) -> List[SkillResult]:
        await super().trigger_skill(req)
        results = []
        if req.identity is None:
            return []
        try:
            # extract the topics from AskOptum VCM API
            vcm_response = await self.fetch_ava_vcm_topic_response(query=req.raw_query)

            # Don't call AVA if 'Others' is the only topic retrieved
            if len(vcm_response.topics) > 0 and vcm_response.topics[0] == "Others":
                return []
            # submit the AVA BNE request
            payload = await self.fetch_ava_bne_response(
                vcm_topic_codes=[t.split(":")[0] for t in vcm_response.topics],
                user=req.identity,
            )

            if payload.ibaag is not None and len(payload.ibaag) > 0:
                for ibaag in payload.ibaag:
                    content = ""
                    for section in ibaag.sections:
                        content = content + self.sanitize_content(section)
                    results.append(
                        SkillResult(
                            variant=Variant.MD,
                            title=ibaag.sectionName,
                            domain=DomainsEnum.benefits,
                            skill=self.name,
                            content=content,
                            meta={"vcm": vcm_response},
                        )
                    )
        except Exception as e:
            logger.error(e)

        return results

    @staticmethod
    @vcm_breaker
    async def fetch_ava_vcm_topic_response(query: str) -> AVATopicResponse:

        req = Query(query=query)

        # get a topic extraction from AskOptum VCM API
        async with insecure_async_client() as client:
            header = {"Content-Type": "application/json"}
            resp = await client.post(
                get_config(RemoteConfig.AVA_VCM_URL),
                headers=header,
                data=req.json(),
                timeout=REQUEST_TIMEOUT,
            )

        data = json.loads(resp.text)

        return AVATopicResponse(**data)

    @bne_breaker
    async def fetch_ava_bne_response(
        self, vcm_topic_codes: List[str], user: UserPublic
    ) -> AVABNEResult:
        bne_url = get_config(RemoteConfig.AVA_BNE_URL_STAGE)
        auth_token = create_access_token(stargate_env=StargateEnv.STAGE)
        at = date.today() - timedelta(days=1)
        dob = parse(user.date_of_birth)
        bne_request = AVBNERequestStage(
            ibaagServiceCodes=vcm_topic_codes,
            at=at.strftime("%Y-%m-%d"),
            dob=dob.strftime("%Y-%m-%d"),
            firstName=user.given_name,
            lastName=user.family_name,
            memberID=user.member_id,
            planID=user.group_number,
            planDetails=False,
            deductible=False,
            docLink=False,
            eligibility=False,
            agentID="",
        )

        async with async_client() as client:
            header = {
                "Content-Type": "application/json",
                "Authorization": ("Bearer " + auth_token),
            }
            resp = await client.post(
                bne_url,
                headers=header,
                data=bne_request.json(),
                timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            data = json.loads(resp.text)

        return AVABNEResult(**data)

    @staticmethod
    def sanitize_content(section: ABIbaagSection):
        parts = section.content.replace("·", "*").splitlines()
        subheader = parts.pop(0)
        if len(parts) == 0:
            parts.append(subheader)
            subheader = ""
        return """##### {header}
###### {subheader}

{content}

""".format(
            header=section.header, subheader=subheader, content="\n".join(parts)
        )
