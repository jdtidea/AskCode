from typing import Any, Dict, List, Optional

from app.models.core import CoreModel


class HealthLibraryAPI(CoreModel):
    wt: str
    q: str
    start: int
    languageCD: str
    brandNM: str
    spellcheck: str


class HLSpellCheck(CoreModel):
    suggestions: List[str]
    correctlySpelled: bool
    collations: List[str]


class HLDocs(CoreModel):
    lex_title: str
    docType_s: Optional[str]
    id: str
    title_t: List[str]
    description_t: List[str]
    url_t: str
    score: int


class HLResponse(CoreModel):
    numFound: int
    start: int
    maxScore: int
    docs: List[HLDocs]


class HLResponseHeader(CoreModel):
    zkConnected: bool
    status: int
    QTime: int


class HLFacetsCounts(CoreModel):
    facet_queries: Dict[str, Any] = {}
    facet_fields: Dict[str, Any] = {}
    facet_ranges: Dict[str, Any] = {}
    facet_intervals: Dict[str, Any] = {}
    facet_heatmaps: Dict[str, Any] = {}


class HealthLibraryResponse(CoreModel):
    spellcheck: Optional[HLSpellCheck]
    response: Optional[HLResponse]
    responseHeader: Optional[HLResponseHeader]
    facets_counts: Optional[HLFacetsCounts]
