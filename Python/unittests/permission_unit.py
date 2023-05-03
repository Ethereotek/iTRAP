import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, '../')
import permissions as perm

config = {
    "admin": {
        "scopes": [
            "app.*",
            "project.*",
            "namedOp.*",
            "monitors.*",
            "project.*",
            "ui.*",
            "namedPars.*"
        ],
        "exclusions": [
            "monitors.write",
            "project.*.delete"
        ],
        "key": "ec3c304e-e937-11ed-8bc6-9cfce837ddb7"
    }
}


class TestPermission(unittest.TestCase):

    def test_validatePermission(self):
        user = 'admin'
        permission = perm.Permission(user, config)

        # Test with a permitted scope
        givenScope = 'app.architecture.put'
        self.assertTrue(permission.validatePermission(givenScope))

        # Test with an excluded scope
        givenScope = 'monitors.write'
        self.assertFalse(permission.validatePermission(givenScope))

        # Test with a scope excluded with a wildcard
        givenScope = 'project.design.delete'
        self.assertFalse(permission.validatePermission(givenScope))

        # Test with an invalid user
        user = 'invalid_user'
        with self.assertRaises(KeyError):
            permission = perm.Permission(user, config)
if __name__ == '__main__':
    unittest.main()