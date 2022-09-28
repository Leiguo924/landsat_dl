"""Handle login and downloading from the EarthExplorer portal."""

import os
import re

import requests
import time
from tqdm import tqdm

from landsat_dl.api import API
from landsat_dl.errors import EarthExplorerError, LandsatxploreError
import landsat_dl.util as util


EE_URL = "https://earthexplorer.usgs.gov/"
EE_LOGIN_URL = "https://ers.cr.usgs.gov/login/"
EE_LOGOUT_URL = "https://earthexplorer.usgs.gov/logout"
EE_DOWNLOAD_URL = (
    "https://earthexplorer.usgs.gov/download/{data_product_id}/{entity_id}/EE/"
)
GG_DOWNLOAD_URL = (
    "http://storage.googleapis.com/gcp-public-data-landsat/{data_product_id}/01/{path}/{row}/{display_id}"
)

# IDs of GeoTIFF data product for each dataset
DATA_PRODUCTS = {
    "landsat_tm_c1": "5e83d08fd9932768",
    "landsat_etm_c1": "5e83a507d6aaa3db",
    "landsat_8_c1": "5e83d0b84df8d8c2",
    "landsat_tm_c2_l1": "5e83d0a0f94d7d8d",
    "landsat_etm_c2_l1": "5e83d0d08fec8a66",
    "landsat_ot_c2_l1": "5e81f14f92acf9ef",
    "landsat_tm_c2_l2": "5e83d11933473426",
    "landsat_etm_c2_l2": "5e83d12aed0efa58",
    "landsat_ot_c2_l2": "5e83d14fec7cae84",
    "sentinel_2a": "5e83a42c6eba8084",
}

DATA_PRODUCTS_GG = {
    "landsat_8_c1": "LC08",
    "landsat_tm_c1": "LT05",
    "landsat_etm_c1": "LE07",
}


def _get_tokens(body):
    """Get `csrf_token` and `__ncforminfo`."""
    csrf = re.findall(r'name="csrf" value="(.+?)"', body)[0]
    # ncform = re.findall(r'name="__ncforminfo" value="(.+?)"', body)[0]

    if not csrf:
        raise EarthExplorerError("EE: login failed (csrf token not found).")
    # if not ncform:
    #     raise EarthExplorerError("EE: login failed (ncforminfo not found).")

    return csrf #, ncform

class EarthExplorer(object):
    """Access Earth Explorer portal."""

    def __init__(self, username, password):
        """Access Earth Explorer portal."""
        self.session = requests.Session()
        self.login(username, password)
        self.api = API(username, password)

    def logged_in(self):
        """Check if the log-in has been successfull based on session cookies."""
        eros_sso = self.session.cookies.get("EROS_SSO_production_secure")
        return bool(eros_sso)

    def login(self, username, password):
        """Login to Earth Explorer."""
        rsp = self.session.get(EE_LOGIN_URL)
        # csrf, ncform = _get_tokens(rsp.text)
        csrf = _get_tokens(rsp.text)
        payload = {
            "username": username,
            "password": password,
            "csrf": csrf,
            # "__ncforminfo": ncform,
        }
        rsp = self.session.post(EE_LOGIN_URL, data=payload, allow_redirects=True)

        if not self.logged_in():
            raise EarthExplorerError("EE: login failed.")

    def logout(self):
        """Log out from Earth Explorer."""
        self.session.get(EE_LOGOUT_URL)

    def _download(self, url, output_dir, timeout, chunk_size=1024, skip=False):
        """Download remote file given its URL."""
        # Check availability of the requested product
        # EarthExplorer should respond with JSON
        with self.session.get(
            url, allow_redirects=False, stream=True, timeout=timeout
        ) as r:
            r.raise_for_status()
            error_msg = r.json().get("errorMessage")
            if error_msg:
                raise EarthExplorerError(error_msg)
            download_url = r.json().get("url")

        try:
            # setting headers and the exception to handle the request error while batch downloading
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
            for i in range(10):
                try:
                    r = self.session.get(download_url, stream=True, allow_redirects=True, timeout=timeout, headers=headers)
                except Exception:
                    if i < 9:
                        time.sleep(0.5)
                else:
                    break
                
            file_size = int(r.headers.get("Content-Length"))
            with tqdm(
                total=file_size, unit_scale=True, unit="B", unit_divisor=1024
            ) as pbar:
                local_filename = r.headers["Content-Disposition"].split("=")[-1]
                local_filename = local_filename.replace('"', "")
                local_filename = os.path.join(output_dir, local_filename)
                print(os.path.basename(local_filename))
                if os.path.exists(local_filename):
                    if os.path.getsize(local_filename) == file_size:
                        skip = True                
                if skip:
                    print('File already exist.')
                    return local_filename
                with open(local_filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(chunk_size)
        except requests.exceptions.Timeout:
            raise EarthExplorerError(
                "Connection timeout after {} seconds.".format(timeout)
            )
        return local_filename

    def download(self, identifier, output_dir, dataset=None, timeout=300, skip=False, landsatlook=False):
        """Download a Landsat scene.

        Parameters
        ----------
        identifier : str
            Scene Entity ID or Display ID.
        output_dir : str
            Output directory. Automatically created if it does not exist.
        dataset : str, optional
            Dataset name. If not provided, automatically guessed from scene id.
        timeout : int, optional
            Connection timeout in seconds.
        skip : bool, optional
            Skip download, only returns the remote filename.

        Returns
        -------
        filename : str
            Path to downloaded file.
        """
        
        if not dataset:
            dataset, path, row = util.guess_dataset(identifier)
        
        output_dir = os.path.join(output_dir, path+row)
        os.makedirs(output_dir, exist_ok=True)
        
        if util.is_display_id(identifier):
            entity_id = self.api.get_entity_id(identifier, dataset)
        else:
            entity_id = identifier
            
        if not landsatlook:
            data_product_id=DATA_PRODUCTS[dataset]
        else:
            r = self.api.request("dataset-download-options", params={"datasetName": dataset})
            for data_product in r:
                if data_product["productName"] == "LandsatLook Images with Geographic Reference":
                    data_product_id = data_product["productId"]
                    break
        
        url = EE_DOWNLOAD_URL.format(data_product_id=data_product_id, entity_id=entity_id)
        filename = self._download(url, output_dir, timeout=timeout, chunk_size=1024, skip=skip)
        
        return filename


class Google_download(object):
    
    def _download(self, url, output_dir, timeout, chunk_size=1024, skip=False):
        """Download remote file given its URL."""
        # Check availability of the requested product
        # EarthExplorer should respond with JSON
        session = requests.Session()
        with session.get(url, allow_redirects=False, stream=True, timeout=timeout
        ) as r:
            r.raise_for_status()
            if "google" not in url:
                error_msg = r.json().get("errorMessage")
                if error_msg:
                    raise EarthExplorerError(error_msg)
                download_url = r.json().get("url")
            else:
                download_url = url

        try:
            with session.get(
                download_url, stream=True, allow_redirects=True, timeout=timeout
            ) as r:
                file_size = int(r.headers.get("Content-Length"))
                
                local_filename = download_url.split("/")[-1]                    
                
                local_filename = os.path.join(output_dir, local_filename)
                print(os.path.basename(local_filename))
                
                if os.path.exists(local_filename):
                    if os.path.getsize(local_filename) == file_size:
                        skip = True                
                if skip:
                    print('File already exist.')
                    return local_filename
                else:
                    with tqdm(
                        total=file_size, unit_scale=True, unit="B", unit_divisor=1024) as pbar:
                        with open(local_filename, "wb") as f:
                            for chunk in r.iter_content(chunk_size=chunk_size):
                                if chunk:
                                    f.write(chunk)
                                    pbar.update(chunk_size)
        except requests.exceptions.Timeout:
            raise EarthExplorerError(
                "Connection timeout after {} seconds.".format(timeout)
            )
        return local_filename
    

    def download(self, identifier, output_dir, dataset, bands, timeout=300, skip=False):
        
        if not dataset:
            dataset,path,row = util.guess_dataset(identifier)
        
        output_dir = os.path.join(output_dir, path+row)
        os.makedirs(output_dir, exist_ok=True)
        
        if util.is_entity_id(identifier):
            raise LandsatxploreError("ERROR: Display ID should be input for google download!")
        else:
            display_id = identifier
            
        root_url = GG_DOWNLOAD_URL.format(
            data_product_id=DATA_PRODUCTS_GG[dataset], path=path, row=row, display_id=display_id
        )
        
        img = root_url.split("/")[-1]
        if bands[0] == 'all':
            bands = util.band_map(dataset)
        elif bands[0] == 'single':
            bands = util.default_single_band(dataset)
        else:
            bands = util.band_check(dataset, bands)
        
        filename=[]
        for band in bands:
            complete_url = root_url + "/" + img + "_" + band
            dst_file = self._download(complete_url, output_dir, timeout, chunk_size=1024, skip=False)
            filename.append(dst_file)
                        
        return filename
