import os
from shutil import rmtree
from tempfile import mkdtemp

from retriever.engines import engine_list
from retriever.lib.load_json import read_json
from retriever.lib.engine_tools import getmd5

from retrieverdash.dashboard_script.status_dashboard_tools import create_dirs
from retrieverdash.dashboard_script.status_dashboard_tools import diff_generator

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, \
csv_engine, download_engine, json_engine, xml_engine = engine_list
file_location = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
precalculated_md5 = '9f6c106f696451732fb763b3632bfd48'
modified_dataset_path = "dataset/modified/Portal_rodents_19772002.csv"
test_files_location = os.path.normpath(os.path.join(file_location, 'test_dir'))


def get_script_module(script_name):
    """Load a script module."""
    return read_json(os.path.join(file_location, script_name))


def test_status_dashboard():
    if not os.path.exists(os.path.join(file_location, 'test_dir')):
        os.makedirs(os.path.join(file_location, 'test_dir'))
        create_dirs(os.path.join(test_files_location))
        os.makedirs(os.path.join(file_location, 'test_dir', 'old', 'sample-dataset'))
    os.chdir(os.path.join(test_files_location, 'old', 'sample-dataset'))
    script_module = get_script_module('sample_dataset')
    sqlite_engine.opts = {'install': 'sqlite', 'file': 'test_db.sqlite3', 'table_name': '{db}_{table}'}
    sqlite_engine.use_cache = False
    script_module.download(engine=sqlite_engine)
    script_module.engine.final_cleanup()
    script_module.engine.to_csv()
    os.remove('test_db.sqlite3')

    # Finding the md5 of the modified dataset
    setattr(script_module.tables['main'], 'path', modified_dataset_path)
    workdir = mkdtemp(dir=test_files_location)
    os.chdir(workdir)
    sqlite_engine.use_cache = False
    script_module.download(engine=sqlite_engine)
    script_module.engine.final_cleanup()
    script_module.engine.to_csv()
    os.remove('test_db.sqlite3')
    calculated_md5 = getmd5(os.getcwd(), data_type='dir')
    rmtree(workdir)

    # If md5 of current dataset doesn't match with current
    # md5 we have to find the diff
    if calculated_md5 != precalculated_md5:
        os.chdir(os.path.join(test_files_location, 'current'))
        sqlite_engine.opts = {'install': 'sqlite', 'file': 'test_db_new.sqlite3', 'table_name': '{db}_{table}'}
        sqlite_engine.use_cache = False
        script_module.download(sqlite_engine)
        script_module.engine.final_cleanup()
        script_module.engine.to_csv()
        os.remove('test_db_new.sqlite3')
        diff_generator(script_module, location=test_files_location)

    diff_exist = True if os.path.isfile(
        os.path.join(test_files_location, 'diffs',
                     'sample_dataset_main.html')) else False
    csv_exist = True if os.path.isfile(
        os.path.join(test_files_location, 'old', 'sample-dataset',
                     'sample_dataset_main.csv')) else False
    os.chdir(file_location)
    rmtree(test_files_location)
    assert diff_exist == True
    assert csv_exist == True
