import os
import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase, RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

import factory
from selenium.webdriver.phantomjs.webdriver import WebDriver

from post.models import Post
from post.views import PostList


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# pragma pylint: disable=R0903
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
    title = 'raw title'
    body = 'raw body'
    is_commentable = False
    published = timezone.now()


# pragma pylint: enable=R0903


class PostTests(TestCase):
    def test_post_create(self):
        post = PostFactory()
        self.assertEqual(1, Post.objects.count())
        self.assertEqual('raw title', post.title)


class BlogViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_no_posts_in_context(self):
        request = self.factory.get('/')
        request.user = UserFactory(password=random_string_generator())
        response = PostList.as_view()(request)
        self.assertEqual(
            list(response.context_data['latest']),
            [],
        )

    def test_posts_in_context(self):
        request = self.factory.get('/')
        post = PostFactory()
        request.user = post.user
        response = PostList.as_view()(request)
        self.assertEqual(
            list(response.context_data['latest']),
            [post],
        )


class IntegrationTests(LiveServerTestCase):
    selenium = None

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver(
            executable_path=os.path.join(
                os.path.dirname(settings.BASE_DIR), 'node_modules', 'phantomjs-prebuilt', 'lib', 'phantom', 'bin',
                'phantomjs')) if os.name == 'nt' else WebDriver()
        cls.password = random_string_generator()
        super(IntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(IntegrationTests, cls).tearDownClass()

    def setUp(self):
        # `user` creation placed in setUp() rather than setUpClass(). Because when `user` created in setUpClass then
        # `test_post_create` passed when executed separately, but failed when executed in batch
        # TODO: investigate this magic
        self.user = UserFactory(password=self.password)

    def test_post_list(self):
        response = self.client.get(reverse('post:list'))
        self.assertEqual(response.status_code, 200)

    def test_slash(self):
        response = self.client.get(reverse('home'))
        self.assertIn(response.status_code, (301, 302))

    def test_empty_create(self):
        response = self.client.get(reverse('post:create'))
        self.assertIn(response.status_code, (301, 302))

    def test_post_create(self):
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
                # it is needed for PhantomJS due to the issue "selenium.common.exceptions.WebDriverException:
                # Message: 'phantomjs' executable needs to be in PATH"
                'domain': '127.0.0.1'
            })
        self.selenium.refresh()  # need to update page for logged in user
        self.selenium.find_element_by_id('id_title').send_keys('post title')
        self.selenium.find_element_by_id('id_body').send_keys('post body')
        self.selenium.find_element_by_xpath('//*[@id="submit-id-save"]').click()
        self.assertEqual(1, Post.objects.count())
        self.assertEqual('post title', Post.objects.first().title)


# TODO: Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead
