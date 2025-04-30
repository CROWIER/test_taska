from litestar import Litestar, Router
from litestar.openapi import OpenAPIConfig
from litestar.config.cors import CORSConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin, SQLAlchemyAsyncConfig

from src.api import user_router
from src.config.settings import settings
from src.api.dependencies import common_dependencies
from src.config.database import create_tables, engine

api_router = Router(
    path="/api/v1",
    route_handlers=[user_router],
)

sqlalchemy_plugin = SQLAlchemyPlugin(
    config=SQLAlchemyAsyncConfig(
        engine_instance=engine,
        before_send_handler=create_tables
    )
)

cors_config = CORSConfig(
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
)

openapi_config = OpenAPIConfig(
    title="Litestar Example",
    description="Example of litestar",
    version="0.0.1",
    render_plugins=[SwaggerRenderPlugin()],
    path="/docs",
)

app = Litestar(
    route_handlers=[api_router],
    openapi_config=openapi_config,
    plugins=[sqlalchemy_plugin],
    cors_config=cors_config,
    debug=True,
    dependencies=common_dependencies,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
