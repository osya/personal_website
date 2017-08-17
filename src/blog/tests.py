from django.test import TestCase
from blog.models import Post


class PostTests(TestCase):
    def test_str(self):
        p = Post(title='MyTitle', description='MyDescription', content='MyContent', is_commentable=False)
        self.assertEqual(str(p), 'MyTitle')
