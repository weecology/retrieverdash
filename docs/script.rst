=================
The Helper Script
=================
The dashboard_script.py is the main script which is used for checking the installation of datasets.
This script uses different functions available in status_dashboard_tools.py for performing it's task.
This script generates a dataset_details.json(containing details regarding installation) and the diffs of the tables of datasets.
This script is run using cron job.

Functions in dashboard_script.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: retrieverdash.dashboard_script.dashboard_script
   :members:
   :exclude-members: check_dataset
.. autofunction:: check_dataset(dataset)

Functions in status_dashboard_tools.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: retrieverdash.dashboard_script.status_dashboard_tools
   :members:
   :exclude-members: create_dirs, get_dataset_md5, diff_generator, create_json, install_postgres, diff_generator_spatial, data_shift
.. autofunction:: create_dirs(location)
.. autofunction:: get_dataset_md5(dataset, use_cache, debug, location)
.. autofunction:: diff_generator(dataset, location)
.. autofunction:: create_json(path)
.. autofunction:: install_postgres(dataset)
.. autofunction:: diff_generator_spatial(dataset, location=file_location)
.. autofunction:: data_shift(dataset, is_spatial=False)
