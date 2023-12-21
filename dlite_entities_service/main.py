"""The main application module."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path as sysPath
from typing import TYPE_CHECKING, Annotated

from fastapi import FastAPI, HTTPException, Path, status

from dlite_entities_service import __version__
from dlite_entities_service.models import VersionedSOFTEntity, get_uri
from dlite_entities_service.service.backend import get_backend
from dlite_entities_service.service.config import CONFIG
from dlite_entities_service.service.logger import setup_logger

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any


LOGGER = logging.getLogger("dlite_entities_service")


# Application lifespan function
@asynccontextmanager
async def lifespan(_: FastAPI):
    """Add lifespan events to the application."""
    # Initialize logger
    setup_logger()

    LOGGER.debug("Starting service with config: %s", CONFIG)

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
)


# Setup routes
SEMVER_REGEX = (
    r"^(?P<major>0|[1-9]\d*)(?:\.(?P<minor>0|[1-9]\d*))?(?:\.(?P<patch>0|[1-9]\d*))?"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
"""Semantic Versioning regular expression.

Slightly changed version of the one found at https://semver.org.
The changed bits pertain to `minor` and `patch`, which are now both optional.
"""


@APP.get(
    "/{version}/{name}",
    response_model=VersionedSOFTEntity,
    response_model_by_alias=True,
    response_model_exclude_unset=True,
)
async def get_entity(
    version: Annotated[
        str,
        Path(
            title="Entity version",
            pattern=SEMVER_REGEX,
            description=(
                "The version part must be a semantic version, following the schema "
                "laid out by SemVer.org."
            ),
        ),
    ],
    name: Annotated[
        str,
        Path(
            title="Entity name",
            pattern=r"(?i)^[A-Z]+$",
            description=(
                "The name part is without any white space. It is conventionally "
                "written in PascalCase."
            ),
        ),
    ],
) -> dict[str, Any]:
    """Get a SOFT entity."""
    uri = f"{CONFIG.base_url}/{version}/{name}"
    entity = get_backend(CONFIG.backend).read(uri)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find entity: uri={uri}",
        )
    return entity


@APP.post(
    "/_admin/create",
    response_model=VersionedSOFTEntity,
    response_model_by_alias=True,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_entity(entity: VersionedSOFTEntity) -> dict[str, Any]:
    """Create a SOFT entity."""
    created_entity = get_backend(CONFIG.backend).create([entity])
    if created_entity is None or isinstance(created_entity, list):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Could not create entity: uri={get_uri(entity)}",
        )
    return created_entity


@APP.post(
    "/_admin/create_many",
    response_model=list[VersionedSOFTEntity],
    response_model_by_alias=True,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_entities(entities: list[VersionedSOFTEntity]) -> list[dict[str, Any]]:
    """Create a SOFT entity."""
    created_entities = get_backend(CONFIG.backend).create(entities)
    if created_entities is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not create entities.",
        )

    if not isinstance(created_entities, list):
        created_entities = [created_entities]

    return created_entities
