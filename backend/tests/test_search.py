import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK


class TestSearch:
    @pytest.mark.asyncio
    async def test_search_v0_200(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(
            app.url_path_for("search:search-query:v0"), params={"q": "i have back pain"}
        )
        assert res.status_code == HTTP_200_OK

    @pytest.mark.asyncio
    async def test_search_v1_200(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(
            app.url_path_for("search:search-query:v1"), params={"q": "i have back pain"}
        )
        assert res.status_code == HTTP_200_OK

    @pytest.mark.asyncio
    async def test_search_v2_200(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(
            app.url_path_for("search:search-query:v2"), params={"q": "i have back pain"}
        )
        assert res.status_code == HTTP_200_OK
