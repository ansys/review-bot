# Contributing 

### Installation

Installing in developer mode allows you to modify the source and enhance it.

Before contributing to the project, please refer to the [PyAnsys Developer's guide](https://dev.docs.pyansys.com/). You will
need to follow these steps:

1. Start by cloning this repository:

   ```bash
   git clone https://github.com/ansys-internal/review-bot
   ```

2. Create a fresh-clean Python environment and activate it:

   ```bash
   # Create a virtual environment
   python -m venv .venv

   # Activate it in a POSIX system
   source .venv/bin/activate

   # Activate it in Windows CMD environment
   .venv/Scripts/Activate.bat

   # Activate it in Windows Powershell
   .venv/Scripts/Activate.ps1
   ```

3. Install the project in editable mode:

   ```bash
   python -m pip install -e .
   ```

# Raw testing

If required, you can always call the style commands ([black](https://black.readthedocs.io/en/stable/), [isort](https://pycqa.github.io/isort/),
[flake8](https://flake8.pycqa.org/en/latest/)) or unit testing ones ([pytest](https://docs.pytest.org/en/stable/)) from the command line. However,
this does not guarantee that your project is being tested in an isolated
environment, which is the reason why tools like [tox](https://tox.readthedocs.io/en/latest/) exist.
```
