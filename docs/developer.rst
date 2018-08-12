=================
Developer's guide
=================

About
=====
The Data Retriever Dashboard is divided into two parts:

1. The Helper Script
2. The Dashboard

**The Helper Script**

The script(dashboard_script.py in retrieverdash/retrieverdash/dashboard_script/ directory) is run regularly based on the cron job specification. It generates a
dataset_details.json file containing the details of the datasets and the diff files(html files showing side by side diffs in the tables of a dataset if there is any
change).

**The Dashboard**

The dashboard provides an interface where maintainers and users can see the details of datasets(whether it is
installing successfully or not using retriever and the diffs).

Setting up locally
==================

Before starting to make contributions to Data Retriever Dashboard you first have to set it up
locally on your machine. You’ll need Python 3.4+. You have to run the script first so that you
get the details of datasets generated to show on the dashboard.

**Steps to run Data Retriever Dashboard locally:**

1. Clone the repository.
2. From the directory containing manage.py, run the following command:
   ``pip install -r requirements.txt`` to install the requirements for the dashboard.

   `To set up the dashboard and attach a cron job:`

3. ``python manage.py makemigrations`` to make migrations.
4. ``python manage.py migrate`` to migrate.
5. ``python manage.py crontab add`` to add the cron job for running the script
   that would check the installation of datasets.

   `To setup the dashboard and start running the job regardless of the set cron configuration:`

6. To run the cron for script immediately write the command ``python manage.py crontab show``.
   Copy the hash for cron job. Then write ``python manage.py crontab run hash_of_the_cron_job``. The script will start running
   immediately.
7. Wait for the script to complete checking all datasets or open another terminal and go to directory
   where manage.py is and write ``python manage.py runserver`` to start the server for the dashboard.
   The default url is ``127.0.0.1:8000``. For using another port write ``python manage.py runserver port_number``.
8. Open a browser and load the url that was provided when you run ``python manage.py runserver`` . This is the dashboard.


Style Guide for Python Code
===========================

Run ``pep8`` on the given file to make sure the file follows the right style.
In some cases we do tend to work outside the ``pep8`` requirements.
The compromise on ``pep8``  may be a result of enforcing better code readability.
In some cases ``pep`` shows errors for long lines, but that can be ignored.

``pep8 pythonfile.py``

Testing
=======

Follow these instructions to run a complete set of tests for any branch
Clone the branch you want to test. Go where setup.py is located.

Install in development mode.

.. code-block:: bash

  $  python setup.py develop


Running tests locally
^^^^^^^^^^^^^^^^^^^^^

To run tests we use pytest.
From the retrieverdash directory where manage.py is. Run:

.. code-block:: sh

  $   pytest -v

This will discover the tests and run it.

Continuous Integration
^^^^^^^^^^^^^^^^^^^^^^

The main GitHub repository runs test on the Travis (Linux) continuous integration platform.

Pull requests submitted to the repository will automatically be tested using
these systems and results reported in the ``checks`` section of the pull request
page.

Documentation
=============

We are using `Sphinx`. for the documentation.
Sphinx uses reStructuredText as its markup language.

**Update Documentation**

The documentation is automatically updated for changes with in the dashboard_script.py and status_dashboard_tools.py.
However, the documentation should be updated after addition of new modules.
Make sure you check the changes and edit if necessary to ensure that only what is required is updated.
Commit and push the new changes.

**Test Documentation locally**

.. code-block:: bash

  cd  docs  # go the docs directory
  make html # Run

  Note:
  Do not commit the build directory after making html.

Collaborative Workflows with GitHub
===================================

**Submitting issues**

Categorize the issues based on labels. For example (Bug, Important, Feature Request and etc..)
Explain the issue explicitly with all details, giving examples and logs where applicable.

**Commits**

From your local branch of retrieverdash, commit to your origin.
Once tests have passed you can then make a pull request to the retriever master (upstream)
For each commit, add the issue number at the end of the description with the tag ``fixes #[issue_number]``.

Example::

  Add more details to the dashboard

  Skip a line and add more explanation if needed
  fixes #3

**Clean histroy**

We try to make one commit for each issue.
As you work on an issue, try adding all the commits into one general commit rather than several commits.

Use ``git commit --amend`` to add new changes to a branch.

Use ``-f`` flag to force pushing changes to the branch. ``git push -f origin [branch_name]``
