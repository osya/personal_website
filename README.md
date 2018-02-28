# README

## Introduction

[![Build Status](https://travis-ci.org/osya/personal_website.svg)](https://travis-ci.org/osya/personal_website) [![Coverage Status](https://coveralls.io/repos/github/osya/personal_website/badge.svg?branch=master)](https://coveralls.io/github/osya/personal_website?branch=master)

Django-based personal website & blog created during the video series [Django Web Development with Python](https://www.youtube.com/playlist?list=PLQVvvaa0QuDeA05ZouE4OzDYLHY-XH-Nd)

The project has text editing feature in Markdown. It has Django Admin for user management. There is a CRUD management for blog posts.

Used technologies:

- Python & Django
- Authentication implemented based on `django-allauth`
- Testing: Selenium & Headless Chrome & Factory Boy
- Assets management: NPM & Webpack
- Travis CI
- Deployed at [Heroku](https://django-personal-website.herokuapp.com/)

## Installation

```shell
    git clone https://github.com/osya/personal_website
    cd personal_website
    pip install -r requirements.txt
    npm install
    npm run build
    python manage.py collectstatic
    python manage.py runserver
```

## Usage

## Tests

To run all tests, run

```shell
    python manage.py test
```
