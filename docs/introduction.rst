============
Introduction
============


An automated testing tool and dashboard for datasets available through Data Retriever
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This django project serves as a status server and dashboard where maintainers and users can see
the status of datasets i.e. whether the datasets are installing properly or not and the changes
that have been made to the dataset.


Features of Data Retriever Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Data Retriever Dashboard performs a number of tasks including:
 #. Runs a script periodically that checks each and every dataset by installing it.
 #. Finds the changes in subsequent versions of datasets.
 #. Displays details of datasets and the changes on the dashboard.

Running the dashboard locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Required packages**

To run Data Retriever Dashboard locally from source, you’ll need Python 3.3+
with the following packages installed:

-  django
-  retriever
-  django-crontab
-  pytest-django


**Steps to run the dashboard from source**

1. Clone the repository.
2. From the directory containing manage.py, run the following command:
   ``pip install -r requirements.txt`` to install the requirements for the dashboard.
3. ``python manage.py crontab add`` to add the cron job for running the script that would check the installation of datasets.
4. ``python manage.py runserver`` to start the server for the dashboard.
5. Open a browser and load the url 127.0.0.1:8000 . This is the dashboard.

**Note**

Initially you won't see anything on the dashboard because the script has been set to run on every Sunday at 12:00 AM.
To run it immediately go to the directory where manage.py is and run the command ``python manage.py crontab show``.
Now copy the hash of the cron from here. Now write the command ``python manage.py crontab run hash_of_the_cron``.
Now the script will run immediately. Open another terminal and start the dashboard server.
The dashboard will start displaying the details now.

Acknowledgments
~~~~~~~~~~~~~~~

This project was developed by Apoorva Pandey as part of Google Summer of Code 2018.
