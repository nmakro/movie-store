import unittest
import flask_testing
from requests.auth import _basic_auth_str
from app import create_app
from unittest.mock import patch, Mock


class TestRoutes(flask_testing.TestCase):

    def create_app(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["DEBUG"] = True
        return self.app

    def setUp(self):
        patcher1 = patch("app.api.users.request")
        patcher2 = patch("app.api.users.User")

        self.mock_flask_request = patcher1.start()
        self.mock_user = patcher2.start()

    def tearDown(self):
        self.mock_flask_request.stop()
        self.mock_user.stop()

    def testListUsersUnauthorized(self):
        with self.app.test_client() as c:
            r = c.get("/api/v1/users")
            self.assertEqual(r.status_code, 401)

    def testListUsersAuthorized(self):
        with self.app.test_client() as c:
            self.mock_flask_request.args.get.side_effect = [1, 4, 5, 5]
            attrs = {'user_dict.return_value': {"id": 5, "username": "Bob"}}
            self.mock_user.query.filter_by.return_value.first.return_value = Mock(id=5, username="Bob", **attrs)
            r = c.get("/api/v1/users", headers={
                'Authorization': _basic_auth_str("admin", "admin_pass")
            })
            self.assertEqual(r.json["username"], "Bob")
            self.assertEqual(r.status_code, 200)

    def testListUsersAuthorizedUserNotFound(self):
        with self.app.test_client() as c:
            self.mock_flask_request.args.get.side_effect = [1, 4, 5, 5]
            self.mock_user.query.filter_by.return_value.first.return_value = None
            r = c.get("/api/v1/users", headers={
                'Authorization': _basic_auth_str("admin", "admin_pass")
            })
            self.assertEqual(r.json["error"], "User not found!")
            self.assertEqual(r.status_code, 404)

    def testListUsersAuthorizedNoUsersFound(self):
        with self.app.test_client() as c:
            self.mock_flask_request.args.get.side_effect = [1, 4, None]
            attrs = {'user_dict.return_value': {"id": 5, "username": "Bob"}}
            u1 = Mock(**attrs)
            attrs = {'user_dict.return_value': {"id": 6, "username": "Alice"}}
            u2 = Mock(**attrs)
            self.mock_user.query.order_by.return_value.paginate.return_value = Mock(items=[u1, u2])
            r = c.get("/api/v1/users", headers={
                'Authorization': _basic_auth_str("admin", "admin_pass")
            })
            self.assertEqual(r.json["Users"][0]["id"], 5)
            self.assertEqual(r.json["Users"][0]["username"], "Bob")
            self.assertEqual(r.json["Users"][1]["id"], 6)
            self.assertEqual(r.json["Users"][1]["username"], "Alice")
            self.assertEqual(r.status_code, 200)

    def testUpdateUsers(self):
        with self.app.test_client() as c:
            self.mock_user.query.filter_by.return_value.first.return_value = None
            r = c.patch("/api/v1/users/5", headers={
                'Authorization': _basic_auth_str("admin", "admin_pass")
            })
            self.assertEqual(r.status_code, 404)

        self.mock_user.reset_mock()

        with self.app.test_client() as c:
            self.mock_user.query.filter_by.return_value.first.return_value = None
            r = c.patch("/api/v1/users/5", headers={
                'Authorization': _basic_auth_str("Chris", "test_user_pass")
            })
            self.assertEqual(r.status_code, 401)

        self.mock_user.reset_mock()

        with self.app.test_client() as c:
            self.mock_user.query.filter_by.return_value.first.return_value = Mock(id=5, username="Bob")
            self.mock_flask_request.args.get.side_effect = "username"
            r = c.patch("/api/v1/users/5", headers={
                'Authorization': _basic_auth_str("Chris", "test_user_pass")
            })
            self.assertEqual(r.status_code, 401)

        self.mock_user.reset_mock()
        self.mock_flask_request.reset_mock()

        with self.app.test_client() as c:
            self.mock_user.query.filter_by.return_value.first.side_effect = [Mock(id=5, username="Chris"), None]
            self.mock_flask_request.args.get.side_effect = [5, " "]
            r = c.patch("/api/v1/users/5", headers={
                'Authorization': _basic_auth_str("Chris", "test_user_pass")
            })
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json["message"], "You cannot have an empty username.")

        self.mock_user.reset_mock()
        self.mock_flask_request.reset_mock()

        with self.app.test_client() as c:
            self.mock_user.query.filter_by.return_value.first.side_effect = [Mock(id=5, username="Chris"), Mock(id=7, username="John")]
            self.mock_flask_request.args.get.side_effect = [5, "John"]
            r = c.patch("/api/v1/users/5", headers={
                'Authorization': _basic_auth_str("Chris", "test_user_pass")
            })
            self.assertEqual(r.status_code, 409)
            self.assertEqual(r.json["message"], "Username John is used by another user. Please user another username.")

        self.mock_user.reset_mock()
        self.mock_flask_request.reset_mock()

        with self.app.test_client() as c:
            self.mock_user.query.filter_by.return_value.first.side_effect = [Mock(id=5, username="Chris"), None]
            self.mock_flask_request.args.get.side_effect = [5, "John"]
            r = c.patch("/api/v1/users/5", headers={
                'Authorization': _basic_auth_str("Chris", "test_user_pass")
            })
            self.assertEqual(r.status_code, 204)

    def testListUserOrders(self):
        with self.app.test_client() as c:
            self.mock_user.query.filter_by.return_value.first.return_value = Mock(id=5, username="Bob")
            r = c.get("/api/v1/users/5/orders", headers={
                'Authorization': _basic_auth_str("Chris", "test_user_pass")
            })
            self.assertEqual(r.status_code, 401)

        self.mock_user.reset_mock()

        with self.app.test_client() as c:
            self.mock_user.query.filter_by.return_value.first.return_value = None
            r = c.get("/api/v1/users/5/orders", headers={
                'Authorization': _basic_auth_str("Chris", "test_user_pass")
            })
            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.json["message"], "The user_id provided does not match a user in the database.")


if __name__ == '__main__':
    unittest.main()
