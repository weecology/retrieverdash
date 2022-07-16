import json
import os
from difflib import HtmlDiff
from shutil import rmtree, move, copytree
from tempfile import mkdtemp

from retriever import reload_scripts
from retriever.engines import engine_list, postgres
from retriever.lib.defaults import HOME_DIR
from retriever.lib.engine_tools import getmd5


def join_path(values):
    """Join and normalize paths"""
    values = [str(values[0]).strip()] + [str(v).strip("/") for v in values[1:]]
    return os.path.normpath(os.path.join(*values))


sqlite_engine = [eng for eng in engine_list if eng.name == 'SQLite'][0]
file_location = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
temp_file_location = join_path([file_location, 'temp_files'])
example_datasets = ['bird-size', 'mammal-masses', 'airports', 'portal']


def get_dataset_md5(dataset, use_cache=False, debug=True, location=temp_file_location):
    """
    Parameters
    ----------
    dataset : dataset script object
    use_cache : True to use cached data or False to download again
    debug: True to raise error or False to fail silently
    location: path where temporary files are to be created for finding md5

    Returns
    -------
    str : The md5 value of a particular dataset.

    Example
    -------
    >>> for dataset in reload_scripts():
    ...     if dataset.name=='aquatic-animal-excretion':
    ...         print(get_dataset_md5(dataset))
    ...
    683c8adfe780607ac31f58926cf1d326
    """
    try:
        db_name = '{}_sqlite.db'.format(dataset.name.replace('-', '_'))
        workdir = mkdtemp(dir=location)
        os.chdir(workdir)
        engine = sqlite_engine.__new__(sqlite_engine.__class__)
        engine.script_table_registry = {}
        args = {
            'command': 'install',
            'dataset': dataset,
            'file': os.path.join(workdir, db_name),
            'table_name': '{db}_{table}',
            'data_dir': '.'
        }
        engine.opts = args
        engine.use_cache = use_cache
        dataset.download(engine=engine, debug=debug)
        engine.to_csv(sort=False)
        engine.final_cleanup()
        try:
            os.remove(join_path([workdir, db_name]))
        except OSError as error:
            print("There was an error.")
        current_md5 = getmd5(workdir,
                             data_type='dir',
                             encoding=dataset.encoding)

        ds = os.path.join(file_location, 'current', dataset.name)
        try:
            if os.path.exists(ds):
                rmtree(ds)
        except OSError as error:
            print(error)
            exit()
        os.makedirs(ds)
        for file in os.listdir(workdir):
            try:
                move(os.path.join(workdir, file), ds)
            except OSError as error:
                print(error)
                exit()
    finally:
        if os.path.isfile(db_name):
            os.remove(db_name)
        if os.path.exists(os.path.join(HOME_DIR, 'raw_data', dataset.name)):
            rmtree(os.path.join(HOME_DIR, 'raw_data', dataset.name))
        os.chdir(os.path.dirname(file_location))
        rmtree(workdir)
    return current_md5


def create_diff(csv1, csv2, diff_file, context, numlines):
    """
    Parameters
    ----------
    csv1 : The first csv file.
    csv2 : The second csv file.
    diff_file : The diff_file that is to be generated.
    context : set to True for contextual differences (defaults to False
            which shows full differences i.e. the whole file. Lines that
            have changes and also those that don't have any changes).
    numlines : number of context lines. When context is set to True,
            controls number of lines(extra lines) displayed before
            and after the lines where the changes have been made.
            When context is False, controls the number of lines to place
            the "next" link anchors before the next change in the diff html
            file (so click of "next" link jumps to just before the change).
            It basically is used to position the "next" anchor tag a particular
            number of lines before the change.

    Returns
    -------
    None: Just creates a html source code file with diff details.

    Example
    -------
    >>> create_diff('file1.csv', 'file2.csv', 'differ.html')
    """
    html_diff = HtmlDiff()
    try:
        with open(csv1, 'r', encoding="ISO-8859-1") as file1, \
                open(csv2, 'r', encoding="ISO-8859-1") as file2, \
                open(diff_file, 'w') as file3:
            diff_lines = html_diff.make_file(file1, file2, context=context, numlines=numlines)
            file3.writelines(diff_lines)
            return True
    except IOError:
        print(IOError, "Ddidid not write diff")
        return IOError


def create_dirs(location=file_location):
    """
    Creates directories required for creating diffs.
    """
    required_dirs = ['temp_files', 'old', 'current', 'diffs']
    for dir_name in required_dirs:
        if not os.path.exists(os.path.join(location, dir_name)):
            os.makedirs(os.path.join(location, dir_name))


def diff_generator(dataset, location=file_location):
    """
    Generates the diff and moves file from
    current directory to old directory.
    """
    tables = {}

    for keys in dataset.tables:
        file_name = '{}_{}'.format(dataset.name.replace('-', '_'), keys)
        csv_file_name = '{}.csv'.format(file_name)
        html_file_name = '{}.html'.format(file_name)
        old_pathsl = os.path.join(location, 'old', dataset.name, csv_file_name)
        current_pathl = os.path.join(location, 'current', dataset.name,  csv_file_name)
        diff_pathl = os.path.join(location, 'diffs',  html_file_name)

        if not os.path.exists(os.path.dirname(diff_pathl)):
            os.makedirs(os.path.dirname(diff_pathl))

        if create_diff(old_pathsl, current_pathl, diff_pathl, context=True, numlines=1):
            tables[keys] = html_file_name
        # try:
        #     h = os.path.exists(os.path.join(location, 'old', dataset.name))
        #     k = os.path.join(location, 'old', dataset.name)
        #     if not h:
        #         os.makedirs(k)
        #     move(current_pathl, old_pathsl)
        # except IOError as e:
        #     print(e, "kkkkkllllllllllllllcccc")
        #     pass
    return tables


def create_json(path="dataset_details.json"):
    """
    This function creates a json file with md5 values
    of all(currently those in example_datasets) datasets.
    """
    data = {}
    for dataset in reload_scripts():
        if dataset.name in example_datasets:
            data[dataset.name] = {"md5": get_dataset_md5(dataset)}
        with open(path, 'w') as json_file:
            json.dump(data, json_file, sort_keys=True, indent=4)


def dataset_type(dataset):
    """
    Parameters
    ----------
    dataset : dataset script object

    Returns
    -------
    str : The type of dataset.

    Example
    -------
    >>> for dataset in reload_scripts():
    ...     if dataset.name=='aquatic-animal-excretion':
    ...         print(dataset_type(dataset))
    ...
    tabular
    """
    for _, table_obj in dataset.tables.items():
        if hasattr(table_obj, 'dataset_type') and table_obj.dataset_type in \
                ["RasterDataset", "VectorDataset"]:
            return "spatial"
    return "tabular"


def install_postgres(dataset):
    """
    Install dataset into local instance of the postgres
    required_opts = [
    ("user", "Enter your PostgreSQL username", "postgres"),
    ("password", "Enter your password", ""),
    ("host", "Enter your PostgreSQL host", "localhost"),
    ("port", "Enter your PostgreSQL port", 5432),
    ("database", "Enter your PostgreSQL database name", "postgres"),
    ("database_name", "Format of schema name", "{db}"),
    ("table_name", "Format of table name", "{db}.{table}"),
    ]
    """

    args = {
        "user": 'retrieverdash',
        "password": "Password12!",
        "host": "localhost",
        "port": 5432,
        "command": 'install',
        "database": "retrieverdash",
        "dataset": dataset,
        "database_name": "{db}",
        "table_name": "{db}.{table}",
    }
    test_engine = postgres.engine()
    test_engine.opts = args
    dataset.download(engine=test_engine, debug=True)

    folder_save_location = os.path.normpath(
        os.path.join(file_location, 'current', dataset.name))
    if not os.path.exists(folder_save_location):
        os.makedirs(folder_save_location)
    test_engine.to_csv(path=folder_save_location)
    test_engine.final_cleanup()

    if os.path.exists(os.path.join(HOME_DIR, 'raw_data', dataset.name)):
        rmtree(os.path.join(HOME_DIR, 'raw_data', dataset.name))


def diff_generator_spatial(dataset, location=file_location):
    """
    Generates the diff and moves file from
    current directory to old directory. This function is specialized for spatial datasets because PostgreSQL has special rules for table naming.
    """
    tables = {}

    for keys in dataset.tables:
        file_name = '{}.{}'.format(dataset.name.replace('-', '_'), keys)
        csv_file_name = '{}.csv'.format(file_name)
        html_file_name = '{}.html'.format(file_name)

        old_path = os.path.join(location, 'old', dataset.name, csv_file_name)
        curr_path = os.path.join(location, 'current', dataset.name, csv_file_name)
        diff_path = os.path.join(location, 'diffs', html_file_name)

        if create_diff(old_path, curr_path, diff_path, context=True, numlines=1):
            tables[keys] = html_file_name
        # try:
        #     if not os.path.exists(os.path.join(location, 'old', dataset.name)):
        #         os.makedirs(os.path.join(location, 'old', dataset.name))
        #     move(curr_path,
        #          os.path.join(location, 'old', dataset.name, csv_file_name))
        # except IOError:
        #     print(IOError, "jjjjjjjjjjjjjjjjj")
        #     exit()

    return tables


def data_shift(dataset, is_spatial=False):
    """
    Shift data from the current directory to the old directory
    """
    for keys in dataset.tables:
        file_name = '{}_{}'.format(
            dataset.name.replace('-', '_'), keys)
        if is_spatial:
            file_name = '{}.{}'.format(dataset.name.replace('-', '_'), keys)
        csv_file_name = '{}.csv'.format(file_name)
        csv_path = os.path.join(file_location, 'current', dataset.name, csv_file_name)
        old_path = os.path.join(file_location, 'old', dataset.name)
        try:
            if not os.path.exists(old_path):
                os.makedirs(old_path)
            move(csv_path,
                 os.path.join(old_path, csv_file_name))
        except IOError as e:
            print(e, "vvvvvvvvvvvvv")
            pass
