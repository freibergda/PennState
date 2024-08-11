'''Jira Task S8S4-61, S8S4-178, S8S4-176, S8S4-63
User Story: As a User, I want the BirdSites database to create
a drop down box of states, for optional selection by the
User, alternatively, to display a drop down list of migratory 
flyways for User selection.  I want to display the results in a 
dashboard, filtered also by the current season if the user chose
a flyway.
Unit Tests:
System Test:
Acceptance Criteria:
Given: A user wants to travel within the next 24 hours
When:  The user selects the User Path from the Menu (User Path 2)
Then:  The system creates a drop down box of all states in
the BirdSites database, and counties in the state, if selected
Variables: none
Parameters: none'''

import streamlit as st
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path


# Insert src directory to the system path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


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

# Mock `st.switch_page` to prevent NoSessionContext error
def mock_switch_page(page_name):
    pass


### Mock the execution control and session_state warning functions to run tests smoothly
def test_patch(*args, value=None, **kwargs):
    return MagicMock()


with patch('streamlit.experimental_rerun', test_patch), patch('streamlit.session_state', dict()), patch('streamlit._is_running_with_streamlit', MagicMock(return_value=True)), patch('streamlit.commands.execution_control.switch_page', mock_switch_page):

    from app import set_role
    from pages.check_password import check_password
    from pages.admin import display_structure, location_records, group_records, location_group_records

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