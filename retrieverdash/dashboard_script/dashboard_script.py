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

TEST_ONLY = [
"abalone-age",
"acton-lake",
"airports",
"amniote-life-hist",
"aquatic-animal-excretion",
"biodiversity-response",
"biomass-allometry-db",
"biotimesql",
"bird-size",
"boston-buildbps",
"breast-cancer-wi",
"breed-bird-survey-nlcd",
"bupa-liver-disorders",
"butterfly-population-network",
"car-eval",
"catalogos-dados-brasil",
"chytr-disease-distr",
"community-abundance-misc",
"croche-vegetation-data",
"dicerandra-frutescens",
"ecoregions-us",
"elton-traits",
"fao-global-capture-product",
"felix-riese-hyperspectral-soilmoisture",
"fernow-air-temperature",
"fernow-biomass",
"fernow-forest-streamflow",
"fernow-nadp-rain-chemistry",
"fernow-precipitation",
"fernow-precipitation-chemistry",
"fernow-soil-productivity",
"fernow-stream-chemistry",
"fernow-watershed-acidification",
"fia-alabama",
"fia-alaska",
"fia-american-samoa",
"fia-arizona",
"fia-arkansas",
"fia-california",
"fia-colorado",
"home-ranges",
"intertidal-abund-me",
"iris",
"jornada-lter-rodent",
"la-selva-trees",
"lakecats-final-tables",
"leaf-herbivory",
"macroalgal-communities",
"macrocystis-variation",
"mammal-community-db",
"mammal-diet",
"mammal-life-hist",
"mammal-masses",
"mammal-metabolic-rate",
"mammal-super-tree",
"mapped-plant-quads-co",
"mapped-plant-quads-id",
"mapped-plant-quads-ks",
"mapped-plant-quads-mt",
"marine-recruitment-data",
"mediter-basin-plant-traits",
"mt-st-helens-veg",
"nadp-precipitation-chemistry",
"nd-gain",
"noaa-fisheries-trade",
"north-carolina-piedmont-mapped-foreset",
"north-carolina-piedmont-permanent-plots",
"north-carolina-piedmont-seedlng-sampling",
"north-carolina-piedmont_seedlng_sampling",
"usda-agriculture-plants-database",
"usda-dietary-supplement-ingredient-data",
"usda-mafcl-fooddatacenteral-alldatatypes",
"usda-mafcl-fooddatacenteral-brandedfoods",
"usda-mafcl-fooddatacenteral-fndds",
"usda-mafcl-fooddatacenteral-foundationfoods",
"usda-mafcl-fooddatacenteral-srlegacy",
"usda-mafcl-fooddatacenteral-supportingdata",
"ushio-maizuru-fish-community",
"veg-plots-sdl",
"virgin-islands-coral-decadal-scale",
"virgin-islands-coral-diadema-antillarum",
"virgin-islands-coral-geography",
"virgin-islands-coral-juvenile",
"virgin-islands-coral-landscape-scale",
"virgin-islands-coral-octocorals-count",
"virgin-islands-coral-physical-measurements",
"virgin-islands-coral-population-projections",
"virgin-islands-coral-recruitment-tiles",
"virgin-islands-coral-scleractinian-corals",
"virgin-islands-coral-taxonomy",
"virgin-islands-coral-yawzi-transects",
"white-clay-creek-avondale-soil",
"white-clay-creek-boulton-chemistry",
"white-clay-creek-chlorophyll",
"white-clay-creek-christina-chemistry",
"white-clay-creek-christina-sediment*",
"white-clay-creek-christina-temperatures",
"white-clay-creek-streamflow",
"white-clay-creek-swrc-meteorology",
"white-clay-creek-waterlevels",
"white-clay-dissolved-carbon",
"white-clay-dissolved-carbon",
"wine-composition",
"wine-quality",
"zipcodes"]


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
