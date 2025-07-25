Contributing
============

We welcome pull requests, issues, and feature suggestions from the community.
Before contributing, please take a moment to review our contribution guidelines and code of conduct.

Setting Up the Project
-----------------------

Setting up the project is pretty simple:

.. code-block:: bash

    docker build -t pytest-html-plus .
    docker run -it pytest-html-plus /bin/bash
    poetry install --dev

    poetry run pytest tests/
