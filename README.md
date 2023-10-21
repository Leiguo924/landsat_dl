# landsat_dl

Command-line tool for Landsat Collection 2 images downloading from USGS EarthExplore.

This tool was modified based on the work of ***landsatxplore*** (https://github.com/yannforget/landsatxplore)

The following datasets are supported (and theorically all datasets on EarthExplore):

| Dataset Name | Dataset ID |
|-|-|
| Landsat 5 TM Collection 2 Level 1 | `landsat_tm_c2_l1` |
| Landsat 5 TM Collection 2 Level 2 | `landsat_tm_c2_l2` |
| Landsat 7 ETM+ Collection 2 Level 1 | `landsat_etm_c2_l1` |
| Landsat 7 ETM+ Collection 2 Level 2 | `landsat_etm_c2_l2` |
| Landsat 8/9 Collection 2 Level 1 | `landsat_ot_c2_l1` |
| Landsat 8/9 Collection 2 Level 2 | `landsat_ot_c2_l2` |


## Why repeat the wheel?
* *landsatxplore* has been outdated a while, there are a few critial issue：<br>
<tab>1. only the entire archived file could be downloaded through the USGS api<br>
<tab>2. the api used in this package changed frequently<br>
<tab>3. individual band downloading is not allowed<br>

## What's different?
* Seach image list through the USGS web API
* no need to update the productID benifit from the new API
* Allow individual band downloading for all landsat Collection 2 products
* Potential to extend the library to all USGS products
* we add a specifed option for *landsatlook* images download

***Yes, this should be much eaiser***


## How to install?
  - `cd /usr/local`  
  - `git clone https://github.com/TristanBlus/landsat_dl.git`  
  - `cd landsat_dl`<br>
  
  install this package in the editable mode with option `-e`  
  - `pip install -e .`<br>
  
  finally, set the parameters of USGS account in the env_path file `~/.bashrc`
  
  **Note:** You need to apply for the M2M access prior to install this package!!!
  
  `export LANDSATXPLORE_USERNAME=Username`
  
  `export LANDSATXPLORE_PASSWORD=Password`
  
 ## Usage
  ```
  landsat_dl [OPTIONS] COMMAND [ARGS]...
  Commands:
    download    Download one or several scenes.
    search      Search for scenes.
  ```
  
  * Search
  ```
  Usage: landsat_dl search [OPTIONS]

Options:
  -u, --username TEXT             EarthExplorer username.
  -p, --password TEXT             EarthExplorer password.
  -d, --dataset [landsat_tm_c1|landsat_etm_c1|landsat_8_c1|landsat_tm_c2_l1|landsat_tm_c2_l2|landsat_etm_c2_l1|landsat_etm_c2_l2|landsat_ot_c2_l1|landsat_ot_c2_l2|sentinel_2a]
                                  Dataset.
  -l, --location FLOAT...         Point of interest (latitude, longitude).
  -b, --bbox FLOAT...             Bounding box (xmin, ymin, xmax, ymax).
  -c, --clouds INTEGER            Max. cloud cover (1-100).
  -s, --start TEXT                Start date (YYYY-MM-DD).
  -e, --end TEXT                  End date (YYYY-MM-DD).
  -o, --output [entity_id|display_id|json|csv]
                                  Output format.
  -m, --limit INTEGER             Max. results returned.
  --help                          Show this message and exit.
  ```
  * Download from USGS
  ```
  Usage: landsat_dl download [OPTIONS] [SCENES]...

Options:
  -u, --username TEXT    EarthExplorer username
  -p, --password TEXT    EarthExplorer password
  -d, --dataset TEXT     Dataset
  -o, --output PATH      Output directory
  --landsatlook          Flag for downloading Landsatlook image
  -b, --bands TEXT       Band
  -t, --timeout INTEGER  Download timeout in seconds
  --skip
  --list FILENAME        Identifier list(.csv) to download
  --help                 Show this message and exit.
  ```
  
  
 ## Example
  * First, save the search result to a csv file (default: tmp.csv)
  
  `landsat_dl search -d landsat_ot_c2_l1 -l 38.9 72.3 -s 2018-07-15 -e 2018-09-15 -o csv`
  
  * Then, use the results list as identifiers to download product, only the 'B8.TIF' band file will be downloaded.
  
  `landsat_dl download --list tmp.csv -b 8 -o ./test`

  ## To do
  * USGS download error handling?
  * parallel downloading with Aria2?
