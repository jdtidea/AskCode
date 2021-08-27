import json
import os

import pytest
from pydantic import ValidationError

from app.models.domains.ava import AVABNEResult, AVATopicResponse


@pytest.fixture
async def test_bne_valid_result() -> AVABNEResult:
    with open(os.path.join(os.path.dirname(__file__), "data/bne_valid.json")) as f:
        data = json.load(f)

    result = AVABNEResult(**data)
    return result


@pytest.fixture
async def test_bne_bad_result() -> AVABNEResult:
    with open(os.path.join(os.path.dirname(__file__), "data/bne_bad.json")) as f:
        data = json.load(f)
    try:
        result = AVABNEResult(**data)
    except ValidationError as e:
        raise e

    return result


@pytest.fixture
async def test_vcm_valid_result() -> AVATopicResponse:
    with open(
        os.path.join(os.path.dirname(__file__), "data/vcm_valid_response.json")
    ) as f:
        data = json.load(f)

    result = AVATopicResponse(**data)
    return result
