from enum import Enum
from typing import Any, List

from app.models.core import CoreModel


class DomainsEnum(Enum):
    """
    Values:
    - BENEFITS
    - PROVIDER
    - PHARMACY
    - FINANCIAL
    - CLAIMS
    - HEALTH
    """

    benefits = "BENEFITS"
    provider = "PROVIDER"
    pharmacy = "PHARMACY"
    financial = "FINANCIAL"
    claims = "CLAIMS"
    health = "HEALTH"
    unknown = "UNKNOWN"


class UHGDomainsResponse(CoreModel):
    domains: List[Any]


class DomainPercentage(CoreModel):
    domain: DomainsEnum
    percentage: float
