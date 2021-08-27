from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import Field

from app.models.core import CoreModel
from app.models.domains.domains import DomainsEnum
from app.models.user import UserPublic


class Input(CoreModel):
    raw_query: str
    identity: Optional[UserPublic]


class Variant(Enum):
    HTML = "html"
    MD = "md"


class Item(CoreModel):
    variant: Variant
    title: Optional[str]
    content: Optional[str]


class SkillResult(CoreModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    url: Optional[str]
    skill: str
    domain: DomainsEnum
    content: Optional[str]
    variant: Variant
    meta: Optional[dict]


class SkillTypeEnum(Enum):
    static = "static"
    dynamic = "dynamic"


class SkillMeta(CoreModel):
    heading: Optional[str] = ""
    content: Optional[str] = ""
    alias: str
    displayName: str
    url: Optional[str]
    entities: Optional[List[str]] = []
    intents: Optional[List[str]] = []
    domain: Optional[DomainsEnum]
    type: Optional[SkillTypeEnum] = SkillTypeEnum.static

    def to_result(self) -> SkillResult:
        if self.type is not SkillTypeEnum.static:
            raise ValueError("Only skills of static type can use this method")
        return SkillResult(
            title=self.heading,
            url=self.url,
            skill=self.alias,
            domain=DomainsEnum.unknown,
            content=self.content,
            variant=Variant.MD,
            meta={"entities": self.entities, "intents": self.intents},
        )


class SkillRegistry(CoreModel):
    skills: List[SkillMeta] = []
