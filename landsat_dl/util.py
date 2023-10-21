"""Utility functions."""
import re
from landsat_dl.errors import LandsatxploreError


def _is_landsat_product_id(id):
    return len(id) == 40 and id.startswith("L")


def _is_landsat_scene_id(id):
    return len(id) == 21 and id.startswith("L")


def _is_sentinel_display_id(id):
    return len(id) == 34 and id.startswith("L")


def _is_sentinel_entity_id(id):
    return len(id) == 8 and id.isdecimal()


def is_display_id(id):
    return _is_landsat_product_id(id) or _is_sentinel_display_id(id)


def is_entity_id(id):
    return _is_landsat_scene_id(id) or _is_sentinel_entity_id(id)


def is_product_id(identifier):
    """Check if a given identifier is a product identifier
    as opposed to a legacy scene identifier.
    """
    return len(identifier) == 40 and identifier.startswith("L")


def parse_product_id(product_id):
    """Retrieve information from a product identifier.

    Parameters
    ----------
    product_id : str
        Landsat product identifier (also referred as Display ID).

    Returns
    -------
    meta : dict
        Retrieved information.
    """
    elements = product_id.split("_")
    return {
        "product_id": product_id,
        "sensor": elements[0][1],
        "satellite": elements[0][2:4],
        "processing_level": elements[1],
        "path": elements[2][0:3],
        "row": elements[2][3:6],
        "acquisition_date": elements[3],
        "processing_date": elements[4],
        "collection_number": elements[5],
        "collection_category": elements[6],
    }


def parse_scene_id(scene_id):
    """Retrieve information from a scene identifier.

    Parameters
    ----------
    scene_id : str
        Landsat scene identifier (also referred as Entity ID).

    Returns
    -------
    meta : dict
        Retrieved information.
    """
    return {
        "scene_id": scene_id,
        "sensor": scene_id[1],
        "satellite": scene_id[2],
        "path": scene_id[3:6],
        "row": scene_id[6:9],
        "year": scene_id[9:13],
        "julian_day": scene_id[13:16],
        "ground_station": scene_id[16:19],
        "archive_version": scene_id[19:21],
    }


def landsat_dataset(satellite, collection="c2", level="l1"):
    """Get landsat dataset name."""
    if satellite < 5:
        sensor = "mss"
    elif satellite == 5:
        sensor = "tm"
    elif satellite == 7:
        sensor = "etm"
    elif satellite == 8 or satellite == 9:
        sensor = "ot"
    else:
        raise LandsatxploreError("Failed to guess dataset from identifier.")
    dataset = f"landsat_{sensor}_{collection}"
    if collection == "c2":
        dataset += f"_{level}"
    return dataset


def guess_dataset(identifier):
    """Guess data set based on a scene identifier."""
    # Landsat Product Identifier
    if _is_landsat_product_id(identifier):
        meta = parse_product_id(identifier)
        satellite = int(meta["satellite"])
        collection = "c" + meta["collection_number"][-1]
        level = meta["processing_level"][:2].lower()
        return landsat_dataset(satellite, collection, level), meta["path"], meta["row"]
    elif _is_landsat_scene_id(identifier):
        meta = parse_scene_id(identifier)
        satellite = int(meta["satellite"])
        return landsat_dataset(satellite), meta["path"], meta["row"]
    elif _is_sentinel_display_id(identifier) or _is_sentinel_entity_id(identifier):
        return "sentinel_2a"
    else:
        raise LandsatxploreError("Failed to guess dataset from identifier.")


def title_to_snake(src_string):
    """Convert title string to snake_case."""
    return src_string.lower().replace(" ", "_").replace("/", "-")


def camel_to_snake(src_string):
    """Convert camelCase string to snake_case."""
    dst_string = [src_string[0].lower()]
    for c in src_string[1:]:
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            dst_string.append("_")
            dst_string.append(c.lower())
        else:
            dst_string.append(c)
    return "".join(dst_string)

def band_map(dataset):
    if "landsat_tm" in dataset :
        bands = ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF',
                          'B6.TIF', 'B7.TIF', 'GCP.txt', 'VER.txt', 'VER.jpg',
                          'ANG.txt', 'BQA.TIF', 'MTL.txt']
    elif "landsat_8" in dataset :
        bands = ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF',
                          'B6.TIF', 'B7.TIF', 'B8.TIF', 'B9.TIF', 'B10.TIF',
                          "B11.TIF", 'ANG.txt', 'BQA.TIF', 'MTL.txt']
    elif "landsat_etm" in dataset :
        bands = ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF',
                          'B6_VCID_1.TIF', 'B6_VCID_2.TIF', 'B7.TIF',
                          'B8.TIF', 'ANG.txt', 'BQA.TIF', 'MTL.txt']
    else:
        bands = ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF',
                          'B6.TIF', 'B6_VCID_1.TIF', 'B6_VCID_2.TIF', 'B7.TIF',
                          'B8.TIF', 'B9.TIF', 'ANG.txt', 'BQA.TIF', 'MTL.txt']
    return bands

def band_check(dataset, bands_in):
    all_bands = band_map(dataset)
    band_orig = []
    for band_in in bands_in:
        for band in all_bands:
            if re.findall(r'\d', band_in) == re.findall(r'\d', band):
                band_orig.append(all_bands[all_bands.index(band)])
    if len(band_orig) == 0:
        raise LandsatxploreError("Wrong input of band name.")
    else:
        return band_orig  

def default_single_band(dataset):
    if "landsat_tm" in dataset :
        bands = ['B4.TIF']
    elif "landsat_8" in dataset :
        bands = ['B8.TIF']
    elif "landsat_9" in dataset :
        bands = ['B8.TIF']
    elif "landsat_etm" in dataset :
        bands = ['B8.TIF']
    else:
        bands = ['B8.TIF']
    return bands                