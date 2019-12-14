import json
import os
from datetime import datetime, timezone
from json.decoder import JSONDecodeError
from shutil import rmtree
from tempfile import mkdtemp

from retriever import reload_scripts, dataset_names
from retriever import download
from retriever.lib.engine_tools import getmd5

from .status_dashboard_tools import get_dataset_md5
from .status_dashboard_tools import diff_generator
from .status_dashboard_tools import create_dirs
from .status_dashboard_tools import dataset_type

file_location = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))

IGNORE_LIST = ['prism-climate', 'mammal-super-tree', 'forest-inventory-analysis',
               'biotime', 'predicts', 'breed-bird-survey', 'predicts', 'usgs-elevation',
               'vertnet', 'vertnet-amphibians', 'vertnet-birds', 'vertnet-fishes',
               'vertnet-mammals', 'vertnet-reptiles', 'NPN'
               ]

TEST_ONLY = ["iris",
              "mammal-masses",
             "wine-composition", "wine-quality"]


NEW_IGNORE = list(set(dataset_names()['online'] + dataset_names()['offline']) - set(TEST_ONLY))

IGNORE_LIST = IGNORE_LIST + NEW_IGNORE

def check_dataset(dataset):
    md5 = None
    status = None
    reason = None
    diff = None
    dataset_detail = None
    try:
        try:
            with open(os.path.join(file_location, "dataset_details.json"), 'r') as json_file:
                dataset_detail = json.load(json_file)
        except (OSError, JSONDecodeError):
            dataset_detail = dict()
            dataset_detail['dataset_details'] = {}

        if dataset_type(dataset) == 'spatial':
            workdir = None
            try:
                workdir = mkdtemp(dir=file_location)
                download(dataset.name, path=workdir)
                md5 = getmd5(workdir, data_type='dir')
            except Exception:
                raise
            finally:
                if workdir:
                    rmtree(workdir)
        else:
            md5 = get_dataset_md5(dataset)
            if dataset.name not in dataset_detail \
                    or md5 != dataset_detail[dataset.name]['md5']:
                diff = diff_generator(dataset)
        status = True
    except Exception as e:
        reason = str(e)
        status = False
    finally:
        json_file_details = dataset_detail
        json_file_details["dataset_details"][dataset.name] = {
            "md5": md5,
            "status": status,
            "reason": reason,
            "diff": diff}
        json_file_details["last_checked_on"] = datetime.now(timezone.utc).strftime("%d %b %Y")
        dataset_details_write = open(os.path.join(file_location, 'dataset_details.json'), 'w')
        json.dump(json_file_details, dataset_details_write,
                  sort_keys=True, indent=4)
        dataset_details_write.close()


def run():
    create_dirs()
    datasets_to_check = [script for script in reload_scripts() if
                         script.name not in IGNORE_LIST]
    for dataset in datasets_to_check:
        check_dataset(dataset)


if __name__ == '__main__':
    run()
