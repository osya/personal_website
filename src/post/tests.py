import os
import random
import string

import factory
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, LiveServerTestCase, RequestFactory, TestCase
from django.utils import timezone
from selenium.webdriver.phantomjs.webdriver import WebDriver

from post.models import Post
from post.views import PostList


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'Agent %03d' % n)
    email = factory.LazyAttributeSequence(lambda o, n: f'{o.username}{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password')


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory, password=random_string_generator())
    title = 'MyTitle'
    body = 'MyBody'
    is_commentable = False
    published = timezone.now()


class PostTests(TestCase):
    def test_str(self):
        post = PostFactory()
        self.assertEqual(str(post), 'MyTitle')


class BlogViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_no_posts_in_context(self):
        request = self.factory.get('/')
        request.user = UserFactory(password=random_string_generator())
        response = PostList.as_view()(request)
        self.assertEquals(list(response.context_data['latest']), [], )

    def test_posts_in_context(self):
        request = self.factory.get('/')
        post = PostFactory()
        request.user = post.user
        response = PostList.as_view()(request)
        self.assertEquals(list(response.context_data['latest']), [post], )


class CreatePostIntegrationTest(LiveServerTestCase):
    selenium = None

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver(
            executable_path=os.path.join(os.path.dirname(settings.BASE_DIR), 'node_modules', 'phantomjs-prebuilt',
                                         'lib', 'phantom', 'bin', 'phantomjs')
        ) if 'nt' == os.name else WebDriver()
        cls.password = random_string_generator()
        cls.user = UserFactory(password=cls.password)
        cls.client = Client()
        super(CreatePostIntegrationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CreatePostIntegrationTest, cls).tearDownClass()

    def test_create_post(self):
        self.assertTrue(self.client.login(username=self.user.username, password=self.password))
        cookie = self.client.cookies[settings.SESSION_COOKIE_NAME]
        # Replace `localhost` to 127.0.0.1 due to the WinError 10054 according to the
        # https://stackoverflow.com/a/14491845/1360307
        self.selenium.get(f'{self.live_server_url}{reverse("post:create")}'.replace('localhost', '127.0.0.1'))
        if cookie:
            self.selenium.add_cookie({
                'name': settings.SESSION_COOKIE_NAME,
                'value': cookie.value,
                'secure': False,
                'path': '/',
                'domain': '127.0.0.1'  # it is needed for PhantomJS due to the issue
                # "selenium.common.exceptions.WebDriverException: Message: 'phantomjs' executable needs to be in PATH"
            })
        self.selenium.refresh()  # need to update page for logged in user
        self.selenium.find_element_by_id('id_title').send_keys('MyTitle')
        self.selenium.find_element_by_id('id_body').send_keys('MyContent')
        self.selenium.find_element_by_xpath('//*[@id="submit-id-save"]').click()
        self.assertEqual(Post.objects.first().title, 'MyTitle')