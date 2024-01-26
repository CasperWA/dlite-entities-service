"""Fixtures for the utils_cli tests."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from typer import Typer
    from typer.testing import CliRunner


def pytest_configure(config: pytest.Config) -> None:
    """Add custom markers to pytest."""
    config.addinivalue_line("markers", "no_token: mark test to not use an auth token")


@pytest.fixture()
def cli() -> CliRunner:
    """Fixture for CLI runner."""
    import os

    from typer.testing import CliRunner

    return CliRunner(mix_stderr=False, env=os.environ.copy())


@pytest.fixture(scope="session")
def config_app() -> Typer:
    """Return the config APP."""
    from dlite_entities_service.cli._utils.global_settings import global_options
    from dlite_entities_service.cli.config import APP

    # Add global options to the APP
    # This is done by the "main" APP, and should hence be done here manually to ensure
    # they can be used
    APP.callback()(global_options)

    return APP


@pytest.fixture()
def tmp_cache_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a temporary cache directory."""
    from dlite_entities_service.cli._utils import generics

    cache_dir = tmp_path / ".cache" / "entities-service"
    cache_dir.mkdir(parents=True)

    monkeypatch.setattr(generics, "CACHE_DIRECTORY", cache_dir)

    return cache_dir


@pytest.fixture()
def tmp_cache_file(tmp_cache_dir: Path) -> Path:
    """Create a temporary cache file."""
    return tmp_cache_dir / "oauth2_token_cache.json"


@pytest.fixture(autouse=True)
def _function_specific_cli_cache_dir(
    tmp_cache_file: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Set the CLI cache directory to a temporary one."""
    from httpx_auth import JsonTokenFileCache

    from dlite_entities_service.cli._utils import generics

    cache = JsonTokenFileCache(str(tmp_cache_file))
    cache.clear()

    monkeypatch.setattr(generics.OAuth2, "token_cache", cache)


@pytest.fixture()
def dotenv_file(tmp_path: Path) -> Path:
    """Create a path to a dotenv file in a temporary test folder."""
    from dlite_entities_service.service.config import CONFIG

    env_file = CONFIG.model_config["env_file"]

    assert isinstance(env_file, str)

    return tmp_path / env_file


@pytest.fixture(autouse=True)
def _reset_context(pytestconfig: pytest.Config) -> None:
    """Reset the context."""
    from dlite_entities_service.cli._utils.global_settings import CONTEXT
    from dlite_entities_service.service.config import CONFIG

    CONTEXT["dotenv_path"] = (
        pytestconfig.invocation_params.dir / str(CONFIG.model_config["env_file"])
    ).resolve()


@pytest.fixture(autouse=True)
def _mock_config_base_url(monkeypatch: pytest.MonkeyPatch, live_backend: bool) -> None:
    """Mock the base url if using a live backend."""
    if not live_backend:
        return

    import os

    from pydantic import AnyHttpUrl

    from dlite_entities_service.service.config import CONFIG

    host, port = os.getenv("ENTITY_SERVICE_HOST", "localhost"), os.getenv(
        "ENTITY_SERVICE_PORT", "8000"
    )

    live_base_url = f"http://{host}"

    if port:
        live_base_url += f":{port}"

    monkeypatch.setattr(CONFIG, "base_url", AnyHttpUrl(live_base_url))


@pytest.fixture()
def non_mocked_hosts(live_backend: bool) -> list[str]:
    """Return a list of hosts that are not mocked by 'pytest-httpx."""
    import os

    from dlite_entities_service.service.config import CONFIG

    if live_backend:
        host, port = os.getenv("ENTITY_SERVICE_HOST", "localhost"), os.getenv(
            "ENTITY_SERVICE_PORT", "8000"
        )

        localhost = host + (f":{port}" if port else "")
        hosts = [localhost, host]
        if CONFIG.base_url.host and CONFIG.base_url.host not in hosts:
            hosts.append(CONFIG.base_url.host)
        return hosts

    return []


@pytest.fixture()
def token_mock() -> str:
    """Return a mock token."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb290IiwiaXNzIjoiaHR0cDovL29udG8tbnMuY29tL21ldGEiLCJleHAiOjE3MDYxOTI1OTAsImNsaWVudF9pZCI6Imh0dHA6Ly9vbnRvLW5zLmNvbS9tZXRhIiwiaWF0IjoxNzA2MTkwNzkwfQ.FzvzWyI_CNrLkHhr4oPRQ0XEY8H9DL442QD8tM8dhVM"


# @pytest.fixture()
# def empty_token_cache(token_mock: str, monkeypatch: pytest.MonkeyPatch) -> None:
#     """Empty the token cache."""
#     import httpx_auth
#     from httpx_auth.errors import AuthenticationFailed


#     class MockTokenCache:

#         already_requested: bool = False

#         def get_token(self, *args, **kwargs) -> str:
#             if self.already_requested:
#                 return token_mock
#             self.already_requested = True
#             raise AuthenticationFailed()


#     monkeypatch.setattr(httpx_auth.OAuth2, "token_cache", MockTokenCache())
