"""Configuration and fixtures for all pytest tests."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from fastapi.testclient import TestClient
    from pymongo.collection import Collection


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add the command line option to run the tests with a live backend."""
    parser.addoption(
        "--live-backend",
        action="store_true",
        default=False,
        help="Run the tests with a live backend (real MongoDB).",
    )


@pytest.fixture(scope="session")
def live_backend(request: pytest.FixtureRequest) -> bool:
    """Return whether to run the tests with a live backend."""
    import os

    required_environment_variables = (
        "ENTITY_SERVICE_MONGO_USER",
        "ENTITY_SERVICE_MONGO_PASSWORD",
    )

    value = request.config.getoption("--live-backend")

    if value:
        # Check certain environment variables are set
        assert not any(os.getenv(_) is None for _ in required_environment_variables), (
            "All required environment variables were not found to be set. "
            "Please set the following environment variables: "
            f"{', '.join(required_environment_variables)}"
        )

    return value


@pytest.fixture(scope="session")
def static_dir() -> Path:
    """Return the path to the static directory."""
    from pathlib import Path

    return (Path(__file__).parent / "static").resolve()


@pytest.fixture(scope="session")
def mongo_test_collection(static_dir: Path, live_backend: bool) -> Collection | None:
    """Add MongoDB test data, returning the MongoDB collection."""
    import yaml

    if live_backend:
        from dlite_entities_service.service.backend import ENTITIES_COLLECTION

        # TODO: Handle authentication properly
        ENTITIES_COLLECTION.insert_many(
            yaml.safe_load((static_dir / "entities.yaml").read_text())
        )

        return None

    # else
    from mongomock import MongoClient

    from dlite_entities_service.service.config import CONFIG

    client_kwargs = {
        "username": CONFIG.mongo_user,
        "password": CONFIG.mongo_password.get_secret_value()
        if CONFIG.mongo_password is not None
        else None,
    }
    for key, value in list(client_kwargs.items()):
        if value is None:
            client_kwargs.pop(key, None)

    MOCK_ENTITIES_COLLECTION = MongoClient(
        str(CONFIG.mongo_uri), **client_kwargs
    ).dlite.entities

    MOCK_ENTITIES_COLLECTION.insert_many(
        yaml.safe_load((static_dir / "entities.yaml").read_text())
    )

    return MOCK_ENTITIES_COLLECTION


@pytest.fixture(autouse=True)
def _mock_backend_entities_collection(
    monkeypatch: pytest.MonkeyPatch, mongo_test_collection: Collection | None
) -> None:
    if mongo_test_collection is None:
        return

    from dlite_entities_service.service import backend

    monkeypatch.setattr(backend, "ENTITIES_COLLECTION", mongo_test_collection)


@pytest.fixture()
def client(live_backend: bool) -> TestClient:
    """Return the test client."""
    import os

    from fastapi.testclient import TestClient

    from dlite_entities_service.main import APP
    from dlite_entities_service.service.config import CONFIG

    if live_backend:
        host, port = os.getenv("ENTITY_SERVICE_HOST", "localhost"), os.getenv(
            "ENTITY_SERVICE_PORT", "8000"
        )

        return TestClient(
            app=APP,
            base_url=f"http://{host}:{port}",
        )

    return TestClient(
        app=APP,
        base_url=str(CONFIG.base_url),
    )
