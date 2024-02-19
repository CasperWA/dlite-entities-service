"""The main application module."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path as sysPath
from typing import TYPE_CHECKING, Annotated

from fastapi import FastAPI, HTTPException, Path, status

from entities_service import __version__
from entities_service.models import (
    Entity,
    EntityNameType,
    EntityVersionType,
)
from entities_service.service.backend import get_backend
from entities_service.service.config import CONFIG
from entities_service.service.logger import setup_logger
from entities_service.service.routers import get_routers

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any


LOGGER = logging.getLogger("entities_service")


# Application lifespan function
@asynccontextmanager
async def lifespan(_: FastAPI):
    """Add lifespan events to the application."""
    # Initialize logger
    setup_logger()

    LOGGER.debug("Starting service with config: %s", CONFIG)

    # Initialize backend
    get_backend(CONFIG.backend, auth_level="write").initialize()

    # Run application
    yield


# Setup application
APP = FastAPI(
    title="Entities Service",
    version=__version__,
    description=(
        sysPath(__file__).resolve().parent.parent.resolve() / "README.md"
    ).read_text(encoding="utf8"),
    lifespan=lifespan,
    root_path=CONFIG.base_url.path if CONFIG.base_url.path != "/" else "",
)

# Add routers
for router in get_routers():
    APP.include_router(router)


@APP.get(
    "/{version}/{name}",
    response_model=Entity,
    response_model_by_alias=True,
    response_model_exclude_unset=True,
)
async def get_entity(
    version: Annotated[EntityVersionType, Path(title="Entity version")],
    name: Annotated[EntityNameType, Path(title="Entity name")],
) -> dict[str, Any]:
    """Get an entity."""
    uri = f"{str(CONFIG.base_url).rstrip('/')}/{version}/{name}"
    entity = get_backend().read(uri)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find entity: uri={uri}",
        )
    return entity
