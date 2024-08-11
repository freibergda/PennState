'''User Story: As a User, I want to confirm that the User 
Path 2 stories have been tested by the developer. The 
purpose of this task was for the developer to create a test 
suite for the User Path 2 Stories which cover the Sprint 3 
and 4 code.  
Unit Tests: Attached.
System Test:
Acceptance Criteria: When the “main” module is executed, 
the Pytest unit tests are run and generate both a text 
report and an html coverage report 
(https://coverage.readthedocs.io/en/latest/index.html ).  
Given: the BirdSites database and User Path 2 software
When: the user wants to verify that the developer has 
created tests that reflect the code requirements and that 
the tests have run correctly.
Then: the tests run and generate a .txt file report and an 
.html coverage report.
Variables:
Parameters: '''

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

import streamlit as st

# Insert src directory to the system path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app import set_role
from pages.check_password import check_password
from pages.admin import display_structure, location_records, group_records, location_group_records

@pytest.fixture(scope='function')
def mock_streamlit():
    with patch('pages.check_password.st.secrets', {'passwords': {'admin': 'admin_pass', 'user': 'user_pass'}}):
        with patch('pages.check_password.st.session_state', {}) as mock_session:
            mock_session.update({'role': 'user'})
            yield mock_session

def reset_session_state():
    keys = list(st.session_state.keys())
    for key in keys:
        del st.session_state[key]

### Test: check_password function
def test_password_check_correct(mock_streamlit):
    reset_session_state()
    st.session_state.update({'username': 'admin', 'password': 'admin_pass'})
    assert check_password() is True

def test_password_check_incorrect(mock_streamlit):
    reset_session_state()
    st.session_state.update({'username': 'admin', 'password': 'wrong_pass'})
    assert check_password() is False

### Test: set_role function
def test_set_role_admin():
    reset_session_state()
    st.session_state._role = "admin"
    set_role()
    assert st.session_state.role == "admin"

def test_set_role_user():
    reset_session_state()
    st.session_state._role = "user"
    set_role()
    assert st.session_state.role == "user"

### Test: display_structure function
def test_display_structure():
    with patch('importlib.util.spec_from_file_location') as mock_spec_from_file_location:
        mock_spec = MagicMock()
        mock_spec.loader = MagicMock()
        mock_spec_from_file_location.return_value = mock_spec
        display_structure()
        mock_spec.loader.exec_module.assert_called_once()

### Test: location_records function
def test_location_records():
    with patch('pages.admin.locations.main') as mock_locations_main:
        location_records()
        mock_locations_main.assert_called_once()

### Test: group_records function
def test_group_records():
    with patch('pages.admin.groups.main') as mock_groups_main:
        group_records()
        mock_groups_main.assert_called_once()

### Test: location_group_records function
def test_location_group_records():
    with patch('pages.admin.locations_groups.main') as mock_locations_groups_main:
        location_group_records()
        mock_locations_groups_main.assert_called_once()

### Mock Streamlit specific functions that require a session context.
@patch('pages.admin.menu_with_redirect')
def test_admin_page(mock_menu_with_redirect):
    mock_menu_with_redirect.return_value = None
    with patch('streamlit.st.session_state') as mock_session:
        mock_session.return_value = {'role': 'admin'}
        from pages import admin
        assert admin.administrator_menu() is None