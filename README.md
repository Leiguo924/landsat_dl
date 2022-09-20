# landsat_dl

Landsat images download from USGS or Google Cloud Storage.

This tool were modified based the work of *landsatxplore* (https://github.com/yannforget/landsatxplore)

## Why repeat the wheel?
* *landsatxplore* has been outdated a while, there are a few critial issue：<br>
<tab>1. only the entire archived file could be downloaded through the USGS api<br>
<tab>2. the api used in this package changed frequently<br>
<tab>3. I want only one or two band of Landsat in my hardrive<br>

* All existed python module that fetch landsat from Google are using the index file(index.tgr.gz) for searching.
* However, it's incomplete with large gaps, and of course is out of date.

## What's different?
* Seach image list through the USGS web api
* Allow individual band downloading from Google<br>

***Yes, I want them both.***

## How to install?
  - `cd /usr/local`  
  - `git clone https://github.com/TristanBlus/landsat_dl.git`  
  - `cd landsat_dl`<br>
  
  install this package in the editable mode with option `-e`  
  - `pip install -e .`<br>
  
  finally, set the parameters of USGS account in the env_path file `~/.bashrc`
  
  
  `export LANDSATXPLORE_USERNAME=TristanBlus`
  
  `export LANDSATXPLORE_PASSWORD=W0gieVy3f8A6`
  
 ## Usage
  ```
  landsat_dl [OPTIONS] COMMAND [ARGS]...
  Commands:
    dl-google  Download one or several scenes.
    dl-usgs    Download one or several scenes.
    search     Search for scenes.
  ```
  
  * Search
  ```
  Usage: landsat_dl search [OPTIONS]

  Search for scenes.

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
  Usage: landsat_dl dl-usgs [OPTIONS] [SCENES]...

Options:
  -u, --username TEXT    EarthExplorer username.
  -p, --password TEXT    EarthExplorer password.
  -d, --dataset TEXT     Dataset
  -o, --output PATH      Output directory.
  -t, --timeout INTEGER  Download timeout in seconds.
  --skip
  --list FILENAME        Identifier list to download
  --help                 Show this message and exit.
  ```
  * Download from Google Storage
  ```
  Usage: landsat_dl dl-google [OPTIONS] [SCENES]...

Options:
  -d, --dataset TEXT     Dataset
  -b, --bands TEXT       Band
  -o, --output PATH      Output directory
  -t, --timeout INTEGER  Download timeout in seconds
  --skip
  --list FILENAME        Identifier list (.csv) to download
  --help                 Show this message and exit
  ```
  
 ## Example
  * First, save the search result to a csv file (default: tmp.csv)
  
  `landsat_dl search -d landsat_8_c1 -l 38.9 72.3 -s 2018-07-15 -e 2018-09-15 -o csv`
  
  * Then, use the results list as identifiers to download data from Google
  
  `landsat_dl dl-google --list tmp.csv -o ./test`
