# tests/test_user_profile.py

import pytest
from agentic_skeleton.core import user_profile

# Define mock data for testing
TEST_USER_PROFILES = {
    "user_beginner": {"skill_level": "BEGINNER"},
    "user_intermediate": {"skill_level": "INTERMEDIATE"},
    "user_expert": {"skill_level": "EXPERT"},
    "user_lowercase": {"skill_level": "beginner"}, # Test case insensitivity
    "user_whitespace": {"skill_level": "  EXPERT  "}, # Test whitespace stripping
    "user_no_skill": {"other_data": "some_value"}, # Test missing skill_level key
    "user_invalid_skill": {"skill_level": "MASTER"}, # Test invalid skill level value
    "user_none_skill": {"skill_level": None}, # Test None skill level value
}

TEST_SKILL_LEVELS = ('BEGINNER', 'INTERMEDIATE', 'EXPERT') # Valid skill levels for tests

@pytest.fixture(autouse=True)
def mock_user_profile_settings(monkeypatch):
    """Mocks the settings used by the user_profile module."""
    monkeypatch.setattr(user_profile, 'MOCK_USER_PROFILES', TEST_USER_PROFILES)
    monkeypatch.setattr(user_profile, 'SKILL_LEVELS', TEST_SKILL_LEVELS)
    # Ensure the default is one of the valid test levels
    monkeypatch.setattr(user_profile, 'DEFAULT_SKILL_LEVEL', 'BEGINNER')

# --- Test Cases for get_user_skill_level ---

def test_get_skill_level_beginner():
    """Test retrieving a valid BEGINNER skill level."""
    assert user_profile.get_user_skill_level("user_beginner") == "BEGINNER"

def test_get_skill_level_intermediate():
    """Test retrieving a valid INTERMEDIATE skill level."""
    assert user_profile.get_user_skill_level("user_intermediate") == "INTERMEDIATE"

def test_get_skill_level_expert():
    """Test retrieving a valid EXPERT skill level."""
    assert user_profile.get_user_skill_level("user_expert") == "EXPERT"

def test_get_skill_level_case_insensitive():
    """Test that skill level retrieval is case-insensitive."""
    assert user_profile.get_user_skill_level("user_lowercase") == "BEGINNER"

def test_get_skill_level_strips_whitespace():
    """Test that skill level retrieval strips leading/trailing whitespace."""
    assert user_profile.get_user_skill_level("user_whitespace") == "EXPERT"

def test_get_skill_level_user_not_found():
    """Test that the default skill level is returned for an unknown user ID."""
    assert user_profile.get_user_skill_level("unknown_user") == "BEGINNER"

def test_get_skill_level_missing_key():
    """Test that the default skill level is returned when 'skill_level' key is missing."""
    assert user_profile.get_user_skill_level("user_no_skill") == "BEGINNER"

def test_get_skill_level_invalid_value():
    """Test that the default skill level is returned for an invalid skill level value."""
    assert user_profile.get_user_skill_level("user_invalid_skill") == "BEGINNER"

def test_get_skill_level_none_value():
    """Test that the default skill level is returned when skill_level is None."""
    assert user_profile.get_user_skill_level("user_none_skill") == "BEGINNER"

def test_get_skill_level_empty_user_id():
    """Test that the default skill level is returned for an empty user ID string."""
    assert user_profile.get_user_skill_level("") == "BEGINNER"

def test_get_skill_level_none_user_id():
    """Test that the default skill level is returned for a None user ID."""
    # The function expects a string, but let's test None defensively
    assert user_profile.get_user_skill_level(None) == "BEGINNER"
