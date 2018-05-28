import os
import unittest
from shutil import rmtree
from unittest import TestCase

from retriever import datasets
from retriever.engines import engine_list

from status_dashboard_tools import create_dirs
from status_dashboard_tools import dataset_to_csv
from status_dashboard_tools import diff_generator
from status_dashboard_tools import get_dataset_md5

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = engine_list
file_location = os.path.dirname(os.path.realpath(__file__))
precalculated_md5 = '9f6c106f696451732fb763b3632bfd48'
modified_dataset_url = 'https://raw.githubusercontent.com/apoorvaeternity' \
                       '/sample-dataset/master/modified/' \
                       'Portal_rodents_19772002.csv'
test_files_location = os.path.join(file_location, 'test_dir')


class TestDashboard(TestCase):
    def test_status_dashboard(self):
        if not os.path.exists(os.path.join(file_location, 'test_dir')):
            os.makedirs(os.path.join(file_location, 'test_dir'))
        create_dirs(os.path.join(test_files_location))
        os.chdir(os.path.join(test_files_location, 'old'))
        dataset = [dataset for dataset in datasets() if dataset.name == 'sample-dataset'][0]
        dataset_to_csv(dataset)
        setattr(dataset.tables['main'], 'url', modified_dataset_url)
        calculated_md5 = get_dataset_md5(dataset,
                                         location=os.path.join(
                                             test_files_location,
                                             'temp_files'))
        if calculated_md5 != precalculated_md5:
            # If md5 of current dataset doesn't match with current
            # md5 we have to find the diff
            os.chdir(os.path.join(test_files_location, 'current'))
            dataset_to_csv(dataset)
            diff_generator(dataset, location=test_files_location)

        diff_exist = True if os.path.isfile(
            os.path.join(test_files_location, 'diffs',
                         'sample_dataset_main.html')) else False
        csv_exist = True if os.path.isfile(
            os.path.join(test_files_location, 'old',
                         'sample_dataset_main.csv')) else False
        self.assertEqual(diff_exist, True, "diff not found")
        self.assertEqual(csv_exist, True, "csv not found")
        os.chdir(file_location)
        rmtree(test_files_location)


if __name__ == '__main__':
    unittest.main()
