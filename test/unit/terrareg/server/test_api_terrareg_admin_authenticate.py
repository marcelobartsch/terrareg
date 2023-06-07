
import unittest.mock

import terrareg.audit_action
from test.unit.terrareg import (
    TerraregUnitTest, mock_models
)
from test import client


class TestApiTerraregAdminAuthenticate(TerraregUnitTest):

    def test_authenticated(self, client, mock_models):
        """Test endpoint when user is authenticated."""
        cookie_expiry_mins = 5
        mock_auth_method = unittest.mock.MagicMock()
        mock_auth_method.is_built_in_admin = unittest.mock.MagicMock(return_value=True)
        mock_auth_method.get_username.return_value = 'unittestadminuser'
        mock_get_current_auth_method = unittest.mock.MagicMock(return_value=mock_auth_method)
        with unittest.mock.patch('terrareg.auth.AuthFactory.get_current_auth_method', mock_get_current_auth_method), \
                unittest.mock.patch('terrareg.config.Config.SECRET_KEY', 'averysecretkey'), \
                unittest.mock.patch('terrareg.config.Config.ADMIN_SESSION_EXPIRY_MINS', cookie_expiry_mins), \
                unittest.mock.patch('terrareg.audit.AuditEvent.create_audit_event') as mock_create_audit_event, \
                unittest.mock.patch('terrareg.models.Session.cleanup_old_sessions', create=True) as cleanup_old_sessions_mock:
            # Update real app secret key
            self.SERVER._app.secret_key = 'averysecretkey'

            res = client.post('/v1/terrareg/auth/admin/login')

            assert res.status_code == 200
            assert res.json == {'authenticated': True}

            mock_auth_method.is_built_in_admin.assert_called_once_with()

            cleanup_old_sessions_mock.assert_called_once()

            with client.session_transaction() as session:
                assert session['is_admin_authenticated'] == True
                assert 'session_id' in session
                assert session['session_id']
                assert len(session['csrf_token']) == 40

            mock_create_audit_event.assert_called_with(
                action=terrareg.audit_action.AuditAction.USER_LOGIN,
                object_type=None,
                object_id=None,
                old_value=None,
                new_value=None)

    def test_authenticated_without_secret_key(self, client, mock_models):
        """Test endpoint and ensure session is not provided"""
        mock_auth_method = unittest.mock.MagicMock()
        mock_auth_method.is_built_in_admin = unittest.mock.MagicMock(return_value=True)
        mock_get_current_auth_method = unittest.mock.MagicMock(return_value=mock_auth_method)
        with unittest.mock.patch('terrareg.auth.AuthFactory.get_current_auth_method', mock_get_current_auth_method), \
                unittest.mock.patch('terrareg.config.Config.SECRET_KEY', ''), \
                unittest.mock.patch('terrareg.audit.AuditEvent.create_audit_event') as mock_create_audit_event, \
                unittest.mock.patch('terrareg.models.Session.cleanup_old_sessions', create=True) as cleanup_old_sessions_mock:
            # Update real app secret key with fake value,
            # otherwise an error would be received when checking the session.
            self.SERVER._app.secret_key = 'test'

            res = client.post('/v1/terrareg/auth/admin/login')

            mock_auth_method.is_built_in_admin.assert_called_once_with()

            assert res.status_code == 403
            assert res.json == {'message': 'Sessions not enabled in configuration'}
            cleanup_old_sessions_mock.assert_not_called()
            mock_create_audit_event.assert_not_called()
            with client.session_transaction() as session:
                # Assert that no session cookies were provided
                assert 'session_id' not in session
                assert 'is_admin_authenticated' not in session
                assert 'csrf_token' not in session

            # Update server secret to empty value and ensure a 403 is still received.
            # The session cannot be checked
            self.SERVER._app.secret_key = ''
            res = client.post('/v1/terrareg/auth/admin/login')

            assert res.status_code == 403
            assert res.json == {'message': 'Sessions not enabled in configuration'}
            mock_create_audit_event.assert_not_called()

    def test_unauthenticated(self, client, mock_models):
        """Test endpoint when user is authenticated."""
        mock_auth_method = unittest.mock.MagicMock()
        mock_auth_method.is_built_in_admin = unittest.mock.MagicMock(return_value=False)
        mock_get_current_auth_method = unittest.mock.MagicMock(return_value=mock_auth_method)
        with unittest.mock.patch('terrareg.auth.AuthFactory.get_current_auth_method', mock_get_current_auth_method), \
            unittest.mock.patch('terrareg.audit.AuditEvent.create_audit_event') as mock_create_audit_event:

            res = client.post('/v1/terrareg/auth/admin/login')

            assert res.status_code == 403
            assert res.json == {'message': "You don't have the permission to access the requested resource. "
                                           "It is either read-protected or not readable by the server."}

            mock_create_audit_event.assert_not_called()