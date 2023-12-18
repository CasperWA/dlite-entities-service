"""SOFT models."""
from __future__ import annotations

import re
from typing import get_args

from pydantic import ValidationError

from .soft5 import SOFT5Entity
from .soft7 import SOFT7Entity

VersionedSOFTEntity = SOFT7Entity | SOFT5Entity

URI_REGEX = re.compile(
    r"^(?P<namespace>https?://[^/]+)/(?P<version>[^/]+)/(?P<name>[^/#?]+)$"
)
"""Regular expression to parse a SOFT entity URI."""


def soft_entity(
    *args, return_errors: bool = False, **kwargs
) -> VersionedSOFTEntity | list[ValidationError]:
    """Return the correct version of the SOFT Entity."""
    errors = []
    for versioned_entity_cls in get_args(VersionedSOFTEntity):
        try:
            new_object = versioned_entity_cls(*args, **kwargs)
            break
        except ValidationError as exc:
            errors.append(exc)
            continue
    else:
        if return_errors:
            return errors

        raise ValueError(
            "Cannot instantiate entity. Errors:\n"
            + "\n".join(str(error) for error in errors)
        )
    return new_object  # type: ignore[return-value]


def get_uri(entity: VersionedSOFTEntity) -> str:
    """Return the URI of the entity."""
    if entity.uri is not None:
        return str(entity.uri)

    return f"{entity.namespace}/{entity.version}/{entity.name}"


def get_version(entity: VersionedSOFTEntity) -> str:
    """Return the version of the entity."""
    if entity.version is not None:
        return entity.version

    if (match := URI_REGEX.match(str(entity.uri))) is not None:
        return str(match.group("version"))

    raise ValueError("Cannot parse URI to get version.")


def get_updated_version(entity: VersionedSOFTEntity) -> str:
    """Return the updated version of the entity."""
    current_version = get_version(entity)

    # Do simple logic, expecting version to be either:
    #  - MAJOR
    #  - MAJOR.MINOR
    #  - MAJOR.MINOR.PATCH
    split_version = current_version.split(".")

    major_length = 1
    minor_length = 2
    patch_length = 3

    # If version is just MAJOR, add and increment MINOR by 1
    # If version is MAJOR.MINOR, add and increment PATCH by 1
    # If version is MAJOR.MINOR.PATCH, increment PATCH by 1

    if len(split_version) == major_length:
        return f"{split_version[0]}.1"

    if len(split_version) == minor_length:
        return f"{split_version[0]}.{split_version[1]}.1"

    if len(split_version) == patch_length:
        return f"{split_version[0]}.{split_version[1]}.{int(split_version[2]) + 1}"

    raise ValueError(
        "Cannot parse version to get updated version. Expecting version to be a "
        "simple MAJOR, MAJOR.MINOR, or MAJOR.MINOR.PATCH styling."
    )
