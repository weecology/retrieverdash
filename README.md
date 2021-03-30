[![Build Status](https://travis-ci.org/weecology/retrieverdash.svg?branch=master)](https://travis-ci.org/weecology/retrieverdash)
[![Documentation Status](https://readthedocs.org/projects/retrieverdash/badge/?version=latest)](https://retrieverdash.readthedocs.io/?badge=latest)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/weecology/retriever/main/LICENSE)
<a href="https://numfocus.org/sponsored-projects">
<img alt="NumFOCUS"
   src="https://i0.wp.com/numfocus.org/wp-content/uploads/2019/06/AffiliatedProject.png" width="100" height="18">
</a>

# retriever-dashboard

This django project serves as a status server and dashboard where maintainers and users can see the status of datasets available
through [retriever](https://github.com/weecology/retriever) i.e. whether the datasets are installing properly or not and the 
changes that have been made to the dataset.

## Running the dashboard locally

To run Data Retriever Dashboard locally from source, you’ll need Python 3.4+.

Steps to run the dashboard from source
--------------------------------------

1. Clone the repository.
2. Install dependencies. There are two options for doing this:
   1. Using `pip`: from the `retrieverdash` directory (containing `manage.py`) run `pip install -r requirements.txt`
   2. Using `conda`: from the root directory of the repository (containing `environment.yml`) run `conda env create -f environment.yml` and then `conda activate retrieverdash`
3. Ensure that you are in the `retrieverdash` directory (containing `manage.py`)
4. `python manage.py crontab add` to add the cron job for running the script that would check the installation of datasets.
5. `python manage.py runserver` to start the server for the dashboard.
6. Open a browser and load the url 127.0.0.1:8000 . This is the dashboard.

**Note**

Initially you won't see anything on the dashboard because the script has been set to run on every Sunday at 12:00 AM.
To run it immediately go to the directory where manage.py is and run the command `python manage.py crontab show`.
Now copy the hash of the cron from here. Now write the command `python manage.py crontab run hash_of_the_cron`.
Now the script will run immediately. Open another terminal and start the dashboard server.
The dashboard will start displaying the details now.

## Documentation

For more information visit https://retrieverdash.readthedocs.io/ .