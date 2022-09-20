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

***I want them both.***
