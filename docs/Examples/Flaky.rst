Flaky Test Support
==================

`pytest-html-plus` integrates seamlessly with the [`pytest-rerunfailures`](https://github.com/pytest-dev/pytest-rerunfailures) plugin to identify and highlight **flaky tests**—tests that fail initially but pass upon re-run.

To get started, install the plugin:

.. code-block:: bash

    pip install pytest-rerunfailures

Then use the `--reruns` option while running your tests:

.. code-block:: bash

    pytest --reruns 2

Any test that **fails initially but passes in a rerun** will automatically get a **Flaky** badge in the HTML report.

📛 These flaky tests are:

- Marked with a "Flaky" badge in the results table
- Visibly distinguishable from consistently passing or failing tests
- Filterable using the **Show Flaky Tests** toggle at the top of the report

This helps teams isolate and address non-deterministic behavior, ensuring more stable test suites.
