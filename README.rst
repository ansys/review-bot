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


Usage
-----

To use the CLI of the tool:

.. code:: bash

    reviewbot <-r path-to-repo> [-c path-to-openai-config] 

An example of the OpenAI config file::
   {
      "MODEL": "gpt-4",
      "API_BASE": "https://your-api-base.openai.azure.com/",
      "API_VERSION": "2023-03-15-preview",
      "API_TYPE": "azure"
   }



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
