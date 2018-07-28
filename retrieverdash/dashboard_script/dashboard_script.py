import json
import os
from multiprocessing import Pool
from shutil import rmtree
from tempfile import mkdtemp

from filelock import FileLock
from retriever import datasets
from retriever import download

from status_dashboard_tools import get_dataset_md5
from status_dashboard_tools import diff_generator
from status_dashboard_tools import create_dirs
from status_dashboard_tools import dataset_type

file_location = os.path.dirname(os.path.realpath(__file__))

json_datasets = ['macroalgal-communities', 'species-exctinction-rates', 'veg-plots-sdl', 'wine-quality', 'airports',
                 'bupa-liver-disorders', 'mammal-diet', 'breed-bird-survey-nlcd', 'gdp', 'biodiversity-response',
                 'nla', 'breast-cancer-wi', 'plant-comp-ok', 'iris', 'mammal-metabolic-rate', 'leaf-herbivory',
                 'nd-gain', 'harvard-forests', 'mapped-plant-quads-co', 'fish-parasite-hosts',
                 'forest-plots-michigan', 'fray-jorge-ecology', 'bioclim', 'nyc-tree-count',
                 'community-abundance-misc', 'plant-occur-oosting', 'mammal-life-hist', 'abalone-age',
                 'tree-canopy-geometries', 'mapped-plant-quads-id', 'car-eval', 'mt-st-helens-veg',
                 'streamflow-conditions', 'plant-taxonomy-us', 'mapped-plant-quads-mt', 'macrocystis-variation',
                 'nematode-traits', 'chytr-disease-distr', 'turtle-offspring-nesting', 'biotime',
                 'mammal-community-db', 'bird-migration-data', 'forest-biomass-china', 'mapped-plant-quads-ks',
                 'croche-vegetation-data', 'mammal-masses', 'antarctic-breed-bird', 'elton-traits', 'home-ranges',
                 'butterfly-population-network', 'partners-in-flight', 'forest-fires-portugal', 'bird-size',
                 'mediter-basin-plant-traits', 'ngreatplains-flowering-dates', 'great-basin-mammal-abundance',
                 'phytoplankton-size', 'portal', 'dicerandra-frutescens', 'predator-prey-body-ratio',
                 'wine-composition', 'globi-interaction', 'marine-recruitment-data', 'portal-dev', 'poker-hands']


def check_dataset(dataset):
    os.chdir(os.path.join(file_location))
    md5 = None
    status = None
    reason = None
    diff = None
    try:
        try:
            dataset_detail = json.load(open('dataset_details.json', 'r'))
        except FileNotFoundError:
            with open("dataset_details.json", 'w') as json_file:
                dataset_detail = dict()
                json.dump(dataset_detail, json_file)

        if dataset_type(dataset) == 'spatial':
            workdir = None
            try:
                workdir = mkdtemp(dir=file_location)
                os.chdir(workdir)
                download(dataset)
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
        os.chdir(os.path.join(file_location))
        with FileLock('dataset_details.json.lock'):
            dataset_details_read = open('dataset_details.json', 'r')
            json_file_details = json.load(dataset_details_read)
            json_file_details[dataset.name] = {
                "md5": md5,
                "status": status,
                "reason": reason,
                "diff": diff}
            dataset_details_write = open('dataset_details.json', 'w')
            json.dump(json_file_details, dataset_details_write,
                      sort_keys=True, indent=4)


def run():
    create_dirs()
    pool = Pool(processes=3)
    pool.map(check_dataset, [dataset for dataset in datasets() if dataset.name in json_datasets])


if __name__ == '__main__':
    run()
