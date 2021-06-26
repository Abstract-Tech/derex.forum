# Derex Forum

[![Github Actions](https://github.com/Abstract-Tech/derex.forum/actions/workflows/daily.yml/badge.svg?branch=master)](https://github.com/Abstract-Tech/derex.forum/actions/workflows/daily.yml)

Derex Plugin to integrate Open edX Forum

## Setup

- Install this package inside a derex project environment
- Add to the project derex.config.yaml ::

  plugins:
  derex.forum: {}

- Add to the project Django settings ::

  COMMENTS_SERVICE_URL = 'http://forum:4567'
  COMMENTS_SERVICE_KEY = 'forumapikey'

  FEATURES["ENABLE_DISCUSSION_SERVICE"] = True

- Create the Elasticsearch index ::

  derex forum create-index

## Development

- Install direnv\_
- Allow direnv to create the virtualenv ::

  direnv allow

- Install with pip ::

  pip install -r requirements.txt
  pre-commit install --install-hooks

## Credits

This package was created with Cookiecutter* and the `audreyr/cookiecutter-pypackage`* project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. \_direnv: https://direnv.net/docs/installation.html
