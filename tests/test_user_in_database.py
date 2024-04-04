import unittest
import os
from app.database import add_user, verify_user


class TestUser(unittest.TestCase):

    def test_add_user(self):
        username = "test_user"
        password = "test_password"
        add_user(username, password)

        # Verify user can be logged in with correct credentials
        self.assertTrue(verify_user(username, password))

        # Verify user cannot be logged in with incorrect credentials (wrong password)
        self.assertFalse(verify_user(username, "incorrect_password"))

    def tearDown(self):
        # Clean up after each test by deleting the test user
        # You'll need to implement get_user_id or a similar function to find the test user's ID
        # delete_user(user_id)  # Implement this function if needed
        pass

if __name__ == "__main__":
    unittest.main()
