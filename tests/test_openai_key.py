import pytest
from unittest.mock import patch, MagicMock
from patterns.decorators import SingletonMeta
from infrastructure.api.openai_key import OpenAIKey


@pytest.fixture
def mock_env(monkeypatch):
    """
    Fixture to set a mock environment variable for the OpenAI API key.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")


@patch("infrastructure.api.openai_key.os.getenv", return_value="test-api-key")
@patch("infrastructure.api.openai_key.OpenAI")
def test_openai_key_initialization(mock_openai, mock_getenv):
    """
    Test the initialization of OpenAIKey with a valid environment variable.
    """
    # Reset the singleton instance cache
    SingletonMeta.reset_instances()

    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.models.list.return_value = ["mock-model"]

    # Instantiate OpenAIKey
    openai_key_instance = OpenAIKey()

    # Verify API key and client are initialized
    assert openai_key_instance.api_key == "test-api-key"
    assert openai_key_instance.client == mock_client
    mock_client.models.list.assert_called_once()


@patch("infrastructure.api.openai_key.os.getenv", return_value=None)
def test_openai_key_missing_env(mock_getenv):
    """
    Test the behavior when the API key is missing in the environment.
    """
    # Reset the singleton instance cache
    SingletonMeta.reset_instances()

    # Instantiating OpenAIKey should trigger the missing key error
    with pytest.raises(ValueError, match="API key is missing. Please set it in .env or provide it explicitly."):
        OpenAIKey()


@patch("infrastructure.api.openai_key.OpenAI")
def test_openai_key_client_initialization_failure(mock_openai):
    """
    Test the behavior when OpenAI client initialization fails.
    """
    # Reset the singleton instance cache
    SingletonMeta.reset_instances()

    # Mock failure during client validation
    mock_openai.return_value.models.list.side_effect = Exception("Client initialization error")

    with pytest.raises(ValueError, match="Failed to initialize OpenAI client: Client initialization error"):
        OpenAIKey()


@patch("infrastructure.api.openai_key.OpenAI")
@patch("infrastructure.api.openai_key.os.getenv", return_value="test-api-key")
def test_openai_key_get_client(mock_getenv, mock_openai):
    """
    Test the get_client method of the OpenAIKey class.
    """
    # Reset the singleton instance cache
    SingletonMeta.reset_instances()

    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    # Instantiate OpenAIKey
    openai_key_instance = OpenAIKey()

    # Verify that get_client returns the same client
    assert openai_key_instance.get_client() == mock_client
