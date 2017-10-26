[![Build Status](https://travis-ci.org/osya/personal_website.svg)](https://travis-ci.org/osya/personal_website)

Django-based personal website & blog created during the video series [Django Web Development with Python](https://www.youtube.com/playlist?list=PLQVvvaa0QuDeA05ZouE4OzDYLHY-XH-Nd)

The project has text editing feature in Markdown. Authentication implemented based on `django-allauth`. It has Django Admin for user management. There is a CRUD management for blog posts.

Used technologies:
- Testing: Selenium & PhantomJS & Factory Boy
- Assets management: NPM & Webpack
- Travis CI
- Deployed at [Heroku](https://django-personal-website.herokuapp.com/)

Installation
```
    git clone https://github.com/osya/personal_website
    cd personal_website
    pip install -r requirements.txt
    npm install
    node node_modules/webpack/bin/webpack.js
    python manage.py collectstatic
    python manage.py runserver
``` 
