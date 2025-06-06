# import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRouter
# from starlette_exporter import handle_metrics
# from starlette_exporter import PrometheusMiddleware

from settings import settings
from api.user.handlers import user_router
from api.user.login_handler import login_router
from api.user.service import service_router


from api.course.handlers.course import router as course_router
from api.course.handlers.category import router as category_router
from api.course.handlers.module import router as module_router
from api.course.handlers.lesson import router as lesson_router
from api.course.handlers.material import router as material_router
from api.course.handlers.tag import router as tag_router

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
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(service_router, tags=["service"])

main_api_router.include_router(course_router, prefix="/courses", tags=["courses"])
main_api_router.include_router(category_router, prefix="/categories", tags=["categories"])
main_api_router.include_router(module_router, prefix="/modules", tags=["modules"])
main_api_router.include_router(lesson_router, prefix="/lessons", tags=["lessons"])
main_api_router.include_router(material_router, prefix="/materials", tags=["materials"])
main_api_router.include_router(tag_router, prefix="/tags", tags=["tags"])


app.include_router(main_api_router)