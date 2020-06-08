===========
Derex Forum
===========


.. image:: https://dev.azure.com/abstract-technology/derex/_apis/build/status/Abstract-Tech.derex.forum?branchName=master
    :target: https://dev.azure.com/abstract-technology/derex.forum/_build


Derex Plugin to integrate Open edX Forum


Setup
-----

* Install this package inside a derex project environment
* Add to the project derex.config.yaml ::


    plugins:
      derex.forum: {}


* Add to the project Django settings ::

    COMMENTS_SERVICE_URL = 'http://forum:4567'
    COMMENTS_SERVICE_KEY = 'forumapikey'

    FEATURES["ENABLE_DISCUSSION_SERVICE"] = True


* Create the Elasticsearch index ::


    derex forum create-index


Development
-----------

* Install direnv_
* Allow direnv to create the virtualenv ::

    direnv allow

* Install with pip ::

    pip install -r requirements.txt
    pre-commit install --install-hooks


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _direnv: https://direnv.net/docs/installation.html
