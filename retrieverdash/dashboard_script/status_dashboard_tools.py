import json
import os
from difflib import HtmlDiff
from shutil import rmtree, move
from tempfile import mkdtemp

from retriever import install_sqlite, datasets
from retriever.engines import engine_list
from retriever.lib.engine_tools import getmd5

sqlite_engine = [eng for eng in engine_list if eng.name == 'SQLite'][0]

file_location = os.path.dirname(os.path.realpath(__file__))

example_datasets = ['bird-size', 'mammal-masses', 'airports', 'portal']


def get_dataset_md5(dataset, use_cache=False, debug=True):
    """
    Parameters
    ----------
    dataset : dataset script object

    Returns
    -------
    str : The md5 value of a particular dataset.

    Example
    -------
    >>> for dataset in datasets():
    ...     if dataset.name=='aquatic-animal-excretion':
    ...         print(get_dataset_md5(dataset))
    ...
    683c8adfe780607ac31f58926cf1d326
    """
    db_name = '{}_sqlite.db'.format(dataset.name.replace('-', '_'))
    workdir = mkdtemp(dir=file_location)
    os.chdir(workdir)
    install_sqlite(dataset.name, use_cache=use_cache,
                   file=os.path.join(file_location, db_name),
                   debug=debug)
    engine_obj = dataset.checkengine(sqlite_engine)
    engine_obj.to_csv()
    current_md5 = getmd5(os.getcwd(), data_type='dir')
    os.chdir(file_location)
    os.remove(db_name)
    rmtree(workdir)
    return current_md5


def create_diff(csv1, csv2, diff_file, context, numlines):
    """
    Parameters
    ----------
    csv1 : The first csv file.
    csv2 : The second csv file.
    diff_file : The diff_file that is to be generated.

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
            diff_lines = html_diff.make_file(file1, file2,
                                             context=context,
                                             numlines=numlines)
            file3.writelines(diff_lines)
    except IOError:
        pass


def create_dirs():
    """
    Creates directories required for creating diffs.
    """
    if not os.path.exists(os.path.join(file_location, 'old')):
        os.makedirs(os.path.join(file_location, 'old'))
    if not os.path.exists(os.path.join(file_location, 'current')):
        os.makedirs(os.path.join(file_location, 'current'))
    if not os.path.exists(os.path.join(file_location, 'diffs')):
        os.makedirs(os.path.join(file_location, 'diffs'))


def dataset_to_csv(dataset):
    """
    Parameters
    ----------
    dataset : dataset script object

    Creates a temporary database and converts
    tables of a particular dataset to csv.
    """
    db_name = '{}_sqlite.db'.format(dataset.name.replace('-', '_'))
    install_sqlite(dataset.name, use_cache=False,
                   file=os.path.join(file_location, db_name))
    engine_obj = dataset.checkengine(sqlite_engine)
    engine_obj.to_csv(sort=False)
    os.remove(os.path.join(file_location, db_name))


def diff_generator(dataset):
    """
    Generates the diff and moves file from
    current directory to old directory.
    """
    for keys in dataset.tables:
        file_name = '{}_{}'.format(dataset.name.replace('-', '_'), keys)
        csv_file_name = '{}.csv'.format(file_name)
        html_file_name = '{}.html'.format(file_name)
        create_diff(os.path.join(file_location, 'old', csv_file_name),
                    os.path.join(file_location, 'current', csv_file_name),
                    os.path.join(file_location, 'diffs', html_file_name),
                    context=True, numlines=1)
        move(os.path.join(file_location, 'current', csv_file_name),
             os.path.join(file_location, 'old', csv_file_name))
        os.chdir(os.path.join(file_location))


def create_json(path="dataset_details.json"):
    """
    This function creates a json file with md5 values
    of all(currently those in example_datasets) datasets.
    """
    data = {}
    for dataset in datasets():
        if dataset.name in example_datasets:
            data[dataset.name] = {"md5": get_dataset_md5(dataset)}
        with open(path, 'w') as json_file:
            json.dump(data, json_file, sort_keys=True, indent=4)
