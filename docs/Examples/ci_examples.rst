CI/CD Integration
=================

GitHub Actions
--------------

.. code-block:: yaml

   - name: Run tests with default parameters
     run: pytest
   - name: Run smoke Tests with custom file names
     run: pytest --html-output smoke_html --json-report smoke.json --generate-xml --xml-report smokeresults.xml
   - name: Run regression Tests with custom file names
     run: pytest --html-output regression_html --json-report regression.json --generate-xml --xml-report regressionresults.xml


   - name: Upload HTML Report
     uses: actions/upload-artifact@v3
     with:
       name: test-report
       path: |
        smoke_html/
        regression_html/


GitLab CI
---------

.. code-block:: yaml

   test:
     script:
       - pytest --json-report --generate-xml --xml-report junit.xml
     artifacts:
       paths:
         - html/
         - junit.xml