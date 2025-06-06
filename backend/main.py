# import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRouter
# from starlette_exporter import handle_metrics
# from starlette_exporter import PrometheusMiddleware

from settings import settings
from api.user.handlers import user_router
from api.user.login_handler import login_router
from api.user.service import service_router

# sentry configuration
# sentry_sdk.init(
#     dsn=settings.SENTRY_URL,
#     traces_sample_rate=1.0,
# )


# create instance of the app
app = FastAPI(
    title="education platform",
    description="This project is an educational platform",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    debug=settings.DEBUG
    )
# app.add_middleware(PrometheusMiddleware)
# app.add_route("/metrics", handle_metrics)

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(service_router, tags=["service"])
app.include_router(main_api_router)