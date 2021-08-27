from typing import Any, Dict, List, Optional

from app.models.core import CoreModel


class Query(CoreModel):
    query: str


class ABIbaagSection(CoreModel):
    content: str
    header: str


class ABIbaagPriorAuth(CoreModel):
    header: str
    lines: List[str]


class ABIbaagItem(CoreModel):
    code: str
    isCsr: bool
    sectionName: str
    sections: List[ABIbaagSection]
    priorAuths: Optional[List[ABIbaagPriorAuth]] = None


class AVABNetwork(CoreModel):
    label: str
    network: str
    remaining: int
    total: int
    used: int


class AVABAccumulator(CoreModel):
    code: str
    networks: List[AVABNetwork]
    serviceName: str


class AVABNEResult(CoreModel):
    type = "AVA:BNE"
    accumulators: Optional[List[AVABAccumulator]] = []
    ibaag: Optional[List[ABIbaagItem]] = []


class AVATopicResponse(CoreModel):
    topics: List[str]
    probability: float


class AVMember(CoreModel):
    timestamp1: str


class AVUtterances(CoreModel):
    agent: Dict[str, Any] = {}
    member: Optional[AVMember] = AVMember(timestamp1="")


class AVAddress(CoreModel):
    street1: str
    street2: str
    street3: str
    city: str
    zip: str
    zip4: str
    state: str
    countryCode: str


class AVDependent(CoreModel):
    firstName: str
    lastName: str
    permanentAddress: AVAddress
    mailingAddress: AVAddress
    dateOfBirth: str
    relationshipCode: str
    crossReferenceId: str
    crossReferencePartitionNumber: str
    asOfDate: str
    sharedArrangementCode: str


class AVBNERequest(CoreModel):  # create a new model with logic for only BNE requests
    # from vcm api (topics/code)
    accumulatorServiceCodes: Optional[List[str]]
    ibaagServiceCodes: List[str]
    # generic
    at: str
    agentID: Optional[str] = ""  # empty
    cosmosDiv: Optional[str] = ""  # empty
    # optional
    deductible: Optional[
        bool
    ] = False  # set to false - if true, it returns details of insurance $ available
    eligibility: Optional[
        bool
    ] = False  # set to false - if true, it return eligibility details
    planDetails: Optional[
        bool
    ] = False  # set to false - if true, it returns plan details
    docLink: Optional[bool] = False  # set to false - if true, it returns link to docs
    # from user profile - BIG 5
    firstName: str
    lastName: str
    dob: str
    memberID: str  # or from eligibility api
    planID: str  # or from eligibility api
    subscriber: Optional[str]  # from user profile / body request for eligibility
    # from eligibility
    coverageSystemCode: Optional[str]
    dependentNumber: Optional[str]
    documentType: Optional[str]
    fundingArrangement: Optional[str]
    legacySubscriberId: Optional[str]
    marketType: Optional[str]
    productType: Optional[str]
    relationshipCode: Optional[str]
    setNumber: Optional[str]  # from eligibility "documentSetNumber"
    sourceCode: Optional[str]


class AVBNERequestStage(
    CoreModel
):  # create a new model with logic for only BNE requests
    # from vcm api (topics/code)

    ibaagServiceCodes: List[str]
    # generic
    at: str
    agentID: Optional[str] = ""  # empty
    deductible: Optional[
        bool
    ] = False  # set to false - if true, it returns details of insurance $ available
    eligibility: Optional[
        bool
    ] = False  # set to false - if true, it return eligibility details
    planDetails: Optional[
        bool
    ] = False  # set to false - if true, it returns plan details
    docLink: Optional[bool] = False  # set to false - if true, it returns link to docs
    # from user profile - BIG 5
    firstName: str
    lastName: str
    dob: str
    memberID: str  # or from eligibility api
    planID: str  # or from eligibility api AKA Group Number
