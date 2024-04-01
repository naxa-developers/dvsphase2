import json
import django
django.setup()

from django.conf import settings

# fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Define Routers Here
# from .user import routers as user_routers
# from .core import routers as core_routers
# from .core import infographics as infographics_routers
# from .core import breakdown as breakdown_routers
# from .core import report as report_routers

#import for fastapi
def get_application() -> FastAPI:
    """Get the FastAPI app instance, with settings."""

    _app = FastAPI(
        title="DVS",
        description="DVS Fast API",
        debug=settings.DEBUG,
    )

    """register fast api routers here"""

    # _app.include_router(user_routers.router)
    # _app.include_router(core_routers.router)
    # _app.include_router(infographics_routers.router)
    # _app.include_router(breakdown_routers.router)
    # _app.include_router(report_routers.router)

    return _app

"""intialize fast api instance"""
app = get_application()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""mongo database"""
database = settings.MONGO_DB

@app.get("/api/v2/")
def read_root():
    return {"message":"Fastapi microservice is up and running"}


# @app.get("/api/v2/project/")
# def province_list():
#     query_data = database.project.find({},{'_id':0})
#     print(query_data)
