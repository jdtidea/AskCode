from app.skills.ava.ava import AvaSkill
from app.skills.healthlibrary.health import HealthSkill
from app.skills.myuhc.benefits import BenefitsSkill
from app.skills.myuhc.claims import ClaimsSkill
from app.skills.myuhc.providers import ProvidersSkill
from app.skills.optumbank.financial import FinancialSkill
from app.skills.optumrx.pharmacy import PharmacySkill


class BaseRepository:
    def __init__(self) -> None:
        # TODO: Only execute skills based on domains
        self.skills = [
            AvaSkill(),
            BenefitsSkill(),
            ClaimsSkill(),
            ProvidersSkill(),
            FinancialSkill(),
            PharmacySkill(),
            HealthSkill(),
        ]
        self.dynamic_skills = {
            AvaSkill.alias: AvaSkill(),
            HealthSkill.alias: HealthSkill(),
        }
