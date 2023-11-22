#!/usr/bin/env python3
"""Run tests for the service."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import requests
import yaml
from dlite import Instance
from fastapi import status
from pymongo import MongoClient

if TYPE_CHECKING:
    from typing import Any, Literal


def _get_test_data() -> list[dict[str, Any]]:
    """Return the test data from tests folder."""
    static_dir = (
        Path(__file__).resolve().parent.parent.parent / "tests" / "static"
    ).resolve()

    if not static_dir.exists():
        error_message = f"Could not find static directory {static_dir!r}."
        raise RuntimeError(error_message)

    test_entities = static_dir / "entities.yaml"

    if not test_entities.exists():
        error_message = f"Could not find test entities file {test_entities!r}."
        raise RuntimeError(error_message)

    try:
        return yaml.safe_load(test_entities.read_text())
    except yaml.error.YAMLError as error:
        error_message = f"Could not load test entities from {test_entities!r}."
        raise RuntimeError(error_message) from error


def add_testdata() -> None:
    """Add MongoDB test data."""
    mongodb_user = os.getenv("ENTITY_SERVICE_MONGO_USER")
    mongodb_pass = os.getenv("ENTITY_SERVICE_MONGO_PASSWORD")
    mongodb_uri = os.getenv("ENTITY_SERVICE_MONGO_URI")
    if any(_ is None for _ in (mongodb_user, mongodb_pass, mongodb_uri)):
        error_message = (
            "ENTITY_SERVICE_MONGO_URI, ENTITY_SERVICE_MONGO_USER, and "
            "ENTITY_SERVICE_MONGO_PASSWORD environment variables MUST be specified."
        )
        raise ValueError(error_message)

    client = MongoClient(mongodb_uri, username=mongodb_user, password=mongodb_pass)
    collection = client.dlite.entities
    collection.insert_many(_get_test_data())


def _get_version_name(uri: str) -> tuple[str, str]:
    """Return the version and name part of a uri."""
    match = re.match(
        r"^http://onto-ns\.com/meta/(?P<version>[^/]+)/(?P<name>[^/]+)$", uri
    )
    if match is None:
        error_message = (
            f"Could not retrieve version and name from {uri!r}. "
            "URI must be of the form: "
            "http://onto-ns.com/meta/{version}/{name}"
        )
        raise RuntimeError(error_message)
    return match.group("version") or "", match.group("name") or ""


def _get_uri(entity: dict[str, Any]) -> str:
    """Return the uri for an entity."""
    namespace = entity.get("namespace")
    version = entity.get("version")
    name = entity.get("name")
    if any(_ is None for _ in (namespace, version, name)):
        error_message = (
            "Could not retrieve namespace, version, and/or name from test entities."
        )
        raise RuntimeError(error_message)
    return f"{namespace}/{version}/{name}"


def run_tests() -> None:
    """Test the service."""
    host = os.getenv("DOCKER_TEST_HOST", "localhost")
    port = os.getenv("DOCKER_TEST_PORT", "8000")

    for test_entity in _get_test_data():
        uri = test_entity.get("uri")

        if uri is None:
            uri = _get_uri(test_entity)

        if not isinstance(uri, str):
            error_message = f"uri must be a string. Got {type(uri)}."
            raise TypeError(error_message)

        version, name = _get_version_name(uri)
        response = requests.get(f"http://{host}:{port}/{version}/{name}", timeout=5)

        assert response.ok, (
            f"Test data {uri!r} not found! (Or some other error).\n"
            f"Response:\n{json.dumps(response.json(), indent=2)}"
        )

        entity = response.json()
        assert entity == test_entity
        Instance.from_dict(entity)

    # Test that the service returns a Not Found (404) for non existant URIs
    version, name = _get_version_name("http://onto-ns.com/meta/0.3/EntitySchema")
    response = requests.get(f"http://{host}:{port}/{version}/{name}", timeout=5)

    assert not response.ok, "Non existant (valid) URI returned an OK response!"
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Response:\n\n{json.dumps(response.json(), indent=2)}"

    # Test that the service raises a pydantic ValidationError and returns an
    # Unprocessable Entity (422) for invalid URIs
    version, name = _get_version_name("http://onto-ns.com/meta/Entity/1.0")
    response = requests.get(f"http://{host}:{port}/{version}/{name}", timeout=5)

    assert not response.ok, "Invalid URI returned an OK response!"
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Response:\n\n{json.dumps(response.json(), indent=2)}"


def main(args: list[str] | None = None) -> None:
    """Entrypoint for docker CI tests."""
    parser = argparse.ArgumentParser(
        prog="docker_test.py",
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "job",
        choices=["add-testdata", "run-tests"],
        default="run_tests",
    )

    job: Literal["add-testdata", "run-tests"] = parser.parse_args(args).job

    if job == "add-testdata":
        add_testdata()
    elif job == "run-tests":
        run_tests()
    else:
        error_message = f"Invalid job {job!r}."
        raise ValueError(error_message)


if __name__ == "__main__":
    main(sys.argv[1:])
