import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_health import health

import app.core.tracing as tracing
from app.api.routes import router as api_router
from app.core import tasks
from app.core.config import ALLOWED_HOST_ORIGINS, PROJECT_NAME, VERSION


def get_health():
    return True


def get_application():
    app = FastAPI(
        title=PROJECT_NAME,
        version=VERSION,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOST_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")
    app.add_api_route("/api/health", health([get_health]))
    return app


app = get_application()


@app.middleware("http")
async def middleware_open_census(request: Request, call_next):
    # TODO: Explore dependency injection + middleware
    # https://github.com/tiangolo/fastapi/issues/402
    await tracing.pre(request)
    response = await call_next(request)
    await tracing.post(response)
    return response


"""
 This code will only execute if you invoke this file like: python backend/app/main.py
 you'd do this if you wanted to attach a debugger to the fastAPI processes
 in normal operation, this server file is imported rather than invoked thus this wont run and conflict
 with normal operations and is safe to keep for debuggers
"""
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["../../"],
        log_level="debug",
    )
