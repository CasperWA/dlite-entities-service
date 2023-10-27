"""SOFT5 models."""
# pylint: disable=duplicate-code
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.networks import AnyHttpUrl

from dlite_entities_service.service.config import CONFIG


class SOFT5Dimension(BaseModel):
    """The defining metadata for a SOFT5 Entity's dimension."""

    name: str = Field(..., description="The name of the dimension.")
    description: str = Field(
        ..., description="A human-readable description of the dimension."
    )


class SOFT5Property(BaseModel):
    """The defining metadata for a SOFT5 Entity's property."""

    name: str | None = Field(
        None,
        description=("The name of the property."),
    )
    type_: str = Field(
        ...,
        alias="type",
        description="The type of the described property, e.g., an integer.",
    )
    ref: AnyHttpUrl | None = Field(
        None,
        alias="$ref",
        definition=(
            "Formally a part of type. `$ref` is used together with the `ref` type, "
            "which is a special datatype for referring to other instances."
        ),
    )
    dims: list[str] | None = Field(
        None,
        description=(
            "The dimension of multi-dimensional properties. This is a list of "
            "dimension expressions referring to the dimensions defined above. For "
            "instance, if an entity have dimensions with names `H`, `K`, and `L` and "
            "a property with shape `['K', 'H+1']`, the property of an instance of "
            "this entity with dimension values `H=2`, `K=2`, `L=6` will have shape "
            "`[2, 3]`."
        ),
    )
    unit: str | None = Field(None, description="The unit of the property.")
    description: str = Field(
        ..., description="A human-readable description of the property."
    )


class SOFT5Entity(BaseModel):
    """A SOFT5 Entity returned from this service."""

    name: str | None = Field(None, description="The name of the entity.")
    version: str | None = Field(None, description="The version of the entity.")
    namespace: AnyHttpUrl | None = Field(
        None, description="The namespace of the entity."
    )
    uri: AnyHttpUrl | None = Field(
        None,
        description=(
            "The universal identifier for the entity. This MUST start with the base "
            "URL."
        ),
    )
    meta: AnyHttpUrl = Field(
        AnyHttpUrl("http://onto-ns.com/meta/0.3/EntitySchema"),
        description=(
            "URI for the metadata entity. For all entities at onto-ns.com, the "
            "EntitySchema v0.3 is used."
        ),
    )
    description: str = Field("", description="Description of the entity.")
    dimensions: list[SOFT5Dimension] = Field(
        [],
        description="A list of dimensions with name and an accompanying description.",
    )
    properties: list[SOFT5Property] = Field(..., description="A list of properties.")

    @field_validator("uri", "namespace")
    @classmethod
    def _validate_base_url(cls, value: AnyHttpUrl) -> AnyHttpUrl:
        """Validate `uri` starts with the current base URL for the service."""
        if not str(value).startswith(str(CONFIG.base_url)):
            raise ValueError(
                "This service only works with DLite/SOFT entities at "
                f"{CONFIG.base_url}."
            )
        return value

    @field_validator("meta")
    @classmethod
    def _only_support_onto_ns(cls, value: AnyHttpUrl) -> AnyHttpUrl:
        """Validate `meta` only refers to onto-ns.com EntitySchema v0.3."""
        if str(value) != "http://onto-ns.com/meta/0.3/EntitySchema":
            raise ValueError(
                "This service only works with DLite/SOFT entities using EntitySchema "
                "v0.3 at onto-ns.com as the metadata entity."
            )
        return value

    @model_validator(mode="before")
    @classmethod
    def _check_cross_dependent_fields(cls, data: Any) -> Any:
        """Check that `name`, `version`, and `namespace` are all set or all unset."""
        if isinstance(data, dict):
            if any(data.get(_) is None for _ in ("name", "version", "namespace")):
                if not all(
                    data.get(_) is None for _ in ("name", "version", "namespace")
                ):
                    raise ValueError(
                        "Either all of `name`, `version`, and `namespace` must be set "
                        "or all must be unset."
                    )
        return data
