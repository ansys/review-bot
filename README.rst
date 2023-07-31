GitHub Reviewer bot
===================

|pyansys| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |codecov| image:: https://codecov.io/gh/ansys/review-bot/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/review-bot
   :alt: Codecov

.. |GH-CI| image:: https://github.com/ansys-internal/review-bot/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys-internal/review-bot/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

Overview
--------

``review-bot`` is a Python library that allows users to automatically generate
suggestions and improvements for patches in GitHub pull requests by leveraging
the power of OpenAI. The library generates suggestions for patch improvements,
considering different aspects such as code style, logical errors, and other
possible issues. This makes the code review process smoother and more
efficient, ensuring that your codebase remains high-quality, maintainable, and
adheres to best practices.

Install with:

.. code:: bash

   pip install review-bot


Installation - Details
----------------------

At two installation modes are provided: user and developer.

For users
^^^^^^^^^

In order to install ``review-bot``, make sure you
have the latest version of `pip`_. To do so, run:

.. code:: bash

    python -m pip install -U pip

Then, you can simply execute:

.. code:: bash

    python -m pip install review-bot


Token Configuration
===================

In order to use the AI project, you will need two tokens: a GitHub access token and an Azure OpenAI token. These tokens are essential for accessing the bot functionalities. 
Here are the links to the respective webpages for obtaining the required tokens:

- GitHub Access Token: [GitHub Token Page](https://github.com/settings/tokens)
- Azure OpenAI Token: [Azure Portal](https://portal.azure.com/)

Please ensure that you keep your tokens confidential and avoid sharing them publicly. Additionally, always follow the best security practices to protect your project and data from unauthorized access.

Below, we outline the steps to obtain each token and how to set them up for your project.

GitHub Access Token
-------------------

A GitHub access token is required to access the GitHub API for certain features, such as querying repositories, creating issues, and managing pull requests. Follow the steps below to obtain a GitHub access token:

1. **Create a GitHub Account:** If you do not have one already, sign up for a GitHub account at https://github.com/signup.

2. **Generate a Personal Access Token:** Once you have a GitHub account, navigate to your account settings by clicking on your profile picture in the top-right corner of the GitHub homepage and selecting "Settings" from the dropdown menu. In the settings page, navigate to "Developer settings" > "Personal access tokens."

3. **Generate a New Token:** Click on the "Generate new token" button and follow the prompts to configure your token. You can choose the scope of access required based on your project's needs.

4. **Copy the Token:** After creating the token, GitHub will display it only once. Make sure to copy the token to a safe place, as you won't be able to see it again.

5. **Configure the Token:** To use the project with your GitHub access token, you should set it as an environment variable with the following name: `GITHUB_TOKEN`.

Azure OpenAI Token
------------------

The Azure OpenAI token is necessary to access the OpenAI API for utilizing advanced AI capabilities provided by the platform. Follow the steps below to obtain an Azure OpenAI token:

1. **Sign Up for Azure:** If you don't have an Azure account, sign up for a free account at https://azure.com/free.

2. **Create an OpenAI Resource:** Once you have an Azure account, create an OpenAI resource in the Azure portal. This will provide you with the necessary credentials to access the OpenAI API.

3. **Obtain the Token:** After creating the resource, you'll receive an API key or token. Make sure to copy and keep it secure, as it will grant you access to the OpenAI services.

4. **Configure the Token:** To use the project with your Azure OpenAI token, you should set it as an environment variable with the following name: `OPEN_AI_TOKEN`.

Additional Required Environment Variables
-----------------------------------------

Apart from the GitHub access token and Azure OpenAI token, there are some additional environment variables that you need to set up to customize the behavior of the AI project. These variables allow you to fine-tune various aspects of the AI model and the OpenAI API integration. Below are the environment variables that need to be configured:

1. **OPENAI_API_BASE:**
   - Description: This variable specifies the base URL of the OpenAI Azure API. It allows you to set the API endpoint for making requests to the OpenAI services.
   - Example: `https://your-api-name.openai.azure.com`

2. **OPENAI_API_TYPE:**
   - Description: This variable defines the type of the OpenAI API. It is used to specify that you are using the Azure version of OpenAI.
   - Example: `azure`


3. **OPENAI_API_VERSION:**
   - Description: This variable indicates the version of the OpenAI API to be used. It ensures compatibility with the specific version of the AI model.
   - Example: `2023-05-15`

4. **OPENAI_MODEL:**
   - Description: This variable allows you to select a particular AI model or engine provided by your Azure OpenAI deployment. You can check your deployment to see the names of your models. Different models may have varying capabilities and performance.
   - Example: `gpt-3.5-turbo-france` or `text-davinci-002`


With all of the environment variables properly configured, you're all set to leverage the full potential of the review bot!

Optionally, if you are using the bot through CLI in local, you can set the Azure OpenAI variables in a JSON configuration file as in the following example.

.. code-block:: json

   {
      "OPEN_AI_TOKEN": "your-token",
      "OPENAI_MODEL": "gpt-4",
      "OPENAI_API_BASE": "https://your-api-base.openai.azure.com/",
      "OPENAI_API_VERSION": "2023-03-15-preview",
      "OPENAI_API_TYPE": "azure"
   }

Usage
-----

To use the CLI of the tool:

.. code:: bash

    reviewbot <-r path-to-repo> [-c path-to-openai-config] 


A note on pre-commit
^^^^^^^^^^^^^^^^^^^^

The style checks take advantage of `pre-commit`_. Developers are encouraged to
install this tool via:

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