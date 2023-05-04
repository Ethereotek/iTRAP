import unittest
import sys
sys.path.insert(0, '../')
import ttree_builder as tt

class TestTrie(unittest.TestCase):

    def setUp(self):
        self.trie = tt.Trie()
        self.trie.insert("/api/banana/app/architecture",{'GET': self.getAppArchitecture},'app.architecture')
        self.trie.insert("/api/banana/namedOp/<name>",{'GET': self.getNamedOp},'namedOp')
        self.trie.insert('/api/v1/users/<user_id>/posts', {'GET': 'get_user_posts', 'POST': 'create_user_post'}, 'users')
        self.trie.insert('/api/v1/posts/<post_id>', {'GET': 'get_post', 'PUT': 'update_post', 'DELETE': 'delete_post'}, 'posts')

    def test_find_existing_route(self):
        handler, params, scope = self.trie.find('/api/v1/users', 'GET')
        self.assertEqual(handler, 'get_users')
        self.assertEqual(params, {})
        self.assertEqual(scope, 'users')

    def test_find_existing_route_with_params(self):
        handler, params, scope = self.trie.find('/api/v1/users/123', 'GET')
        self.assertEqual(handler, 'get_user')
        self.assertEqual(params, {'user_id': '123'})
        self.assertEqual(scope, 'users')

    def test_find_existing_route_with_params_and_children(self):
        handler, params, scope = self.trie.find('/api/v1/users/123/posts', 'GET')
        self.assertEqual(handler, 'get_user_posts')
        self.assertEqual(params, {'user_id': '123'})
        self.assertEqual(scope, 'users')

    def test_find_nonexistent_route(self):
        handler, params, scope = self.trie.find('/api/v1/users/123/posts/456', 'GET')
        self.assertEqual(handler, None)
        self.assertEqual(params, {})
        self.assertEqual(scope, '')

if __name__ == '__main__':
    unittest.main()