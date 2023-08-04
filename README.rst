Review Bot
==========

|pyansys| |GH-CI| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |GH-CI| image:: https://github.com/ansys/review-bot/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/review-bot/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

Overview
--------

The ``review-bot`` package is a Python development tool for leveraging
the power of OpenAI to automatically generate suggestions for improving
GitHub pull requests. To generate suggestions for improvements, this tool
considers code style, logical errors, and other possible issues. Using
this tool makes the code review process smoother and more efficient,
ensuring that your code base is high quality, easy to maintain, and
adheres to best practices.

Install the ``review-bot`` package with this command:

.. code:: bash

   pip install review-bot


Installation
------------

Two installation modes are provided: user and developer.

For users
^^^^^^^^^

First, to make sure that you have the latest version of `pip`_,
run this command:

.. code:: bash

    python -m pip install -U pip

Then, to install the ``review-bot`` package, run this command:

.. code:: bash

    python -m pip install review-bot


Token configuration
-------------------

To use this tool to review GitHub pull requests, you must have two tokens for
accessing the bot functionalities:

- GitHub access token
- Azure OpenAI token

Subsequent sections explain how to obtain these tokens and set them up for your project.

Ensure that you keep your tokens confidential and do not share them publicly. Additionally,
always follow the best security practices to protect your project and data from unauthorized
access.


GitHub access token
^^^^^^^^^^^^^^^^^^^

A GitHub access token is required to access the GitHub API for certain features, such as
querying repositories, creating issues, and managing pull requests.

To obtain a GitHub access token, perform these steps:

1. **Create a GitHub account:** If you do not already have a GitHub account, sign up for one
   at https://github.com/signup.

2. **Generate a PAT (personal access token):** After signing into your GitHub account, go to
   `Personal access tokens (classic) <https://github.com/settings/tokens>`_ in your GitHub
   developer settings and click the **Generate a personal access token** link. Follow
   the prompts to configure your new token, choosing the scope of access required based on
   your project's needs.

4. **Copy the token:** After creating the token, GitHub displays it only once. Make sure
   that you copy the token to a secure location because you are not able to see it again.

5. **Set the token as an environment variable:** To use the project with your GitHub access
   token, set the token as an environment variable having this name: ``GITHUB_TOKEN``.

Azure OpenAI token
^^^^^^^^^^^^^^^^^^

The Azure OpenAI token is required to access the OpenAI API for utilizing the advanced AI
capabilities provided by `Microsoft Azure <https://portal.azure.com/>`_.

To obtain an Azure OpenAI token, perform these steps:

1. **Sign up for Azure:** If you do not already have an Azure account, sign up for a free
   account at https://azure.com/free.

2. **Create an OpenAI resource:** Once you have an Azure account, create an OpenAI resource
   in the Azure portal. This resource provides you with the necessary credentials to access
   the OpenAI API.

3. **Copy the token:** After creating the resource, Azure sends you a token (key) that
   grants you access to the OpenAI services. Make sure that you copy this token to a
   secure location.

4. **Set the token as an environment variable:** To use the project with your Azure OpenAI
   token, set the token as an environment variable having this name: ``OPEN_AI_TOKEN``.


Additional required environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to setting up environment variables for the GitHub access token and Azure OpenAI
token, you must set up some additional environment variables to customize the behavior of the
OpenAI project. The following variables allow you to fine tune various aspects of the OpenAI
model and the OpenAI API integration.

**OPENAI_API_BASE**

* Description: Specifies the base URL of the OpenAI Azure API. This environment variable
  allows you to set the API endpoint for making requests to the OpenAI services.
* Example: `https://your-api-name.openai.azure.com`

**OPENAI_API_TYPE**

* Description: Defines the type of the OpenAI API. This environment variable is used to
  specify that you are using the Azure version of OpenAI.
* Example: `azure`

**OPENAI_API_VERSION**

* Description: Indicates the version of the OpenAI API to use. This environment variable
  ensures compatibility with the specific version of the AI model.
* Example: `2023-05-15`

**OPENAI_MODEL**

* Description: Allows you to select a particular AI model or engine provided by your
  Azure OpenAI deployment. You can check your deployment to see the names of your models.
  Different models may have varying capabilities and performance.
* Example: `gpt-3.5-turbo-france` or `text-davinci-002`

With all these environment variables properly configured, you are ready to leverage the full
potential of the review bot.

Optionally, if you are using the review bot through CLI locally, you can set the Azure OpenAI
variables in a JSON configuration file as per this example:

.. code-block:: json

   {
      "OPEN_AI_TOKEN": "your-token",
      "OPENAI_MODEL": "gpt-4",
      "OPENAI_API_BASE": "https://your-api-base.openai.azure.com/",
      "OPENAI_API_VERSION": "2023-03-15-preview",
      "OPENAI_API_TYPE": "azure"
   }

CLI usage
---------

To use the CLI (command-line interface) of the review bot, run this command:

.. code:: bash

    reviewbot <-r path-to-repo> [-c path-to-openai-config]


``pre-commit``
--------------

The style checks take advantage of `pre-commit`_. Developers are encouraged to
install this tool by running this command:

.. code:: bash

    python -m pip install pre-commit && pre-commit install


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
