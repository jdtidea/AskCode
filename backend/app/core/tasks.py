from typing import Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI

from app.core.config import initialize_environment
from app.core.logger import initialize_logger
from app.ranking import initialize_ranking
from app.skills.registry import initialize_skill_registry


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        initialize_environment()
        initialize_skill_registry()
        initialize_ranking()
        initialize_logger()
        scheduler = AsyncIOScheduler()
        # refresh config every 5m
        scheduler.add_job(initialize_environment, IntervalTrigger(minutes=5))
        scheduler.add_job(initialize_skill_registry, IntervalTrigger(minutes=5))
        scheduler.add_job(initialize_ranking, IntervalTrigger(minutes=5))
        scheduler.start()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        # Implement as-needed
        pass

    return stop_app
