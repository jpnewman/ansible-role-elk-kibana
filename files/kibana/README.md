# Sync Kibana Objects

Script ```sync_kibana_objects.py``` can be used to download, upload, and delete the following Kibana objects: -

- Dashboards
- Visualizations
- Searches
- Templates

Objects can be filtered by adding ```include``` and ```exclude``` array of regular expression to the ```FOLDER_OBJECT_KEY_DICT``` values within script ```sync_kibana_objects.py```.

## Install python requirements

~~~bash
pip install -r requirements.txt
~~~

## Arguments

It has the following positional arguments: -

|Variables|Description|Default|
|---|---|---|
|```elasticsearch_host```|Elasticsearch Host|http://10.10.10.10:9200|
|```--upload```|Uploads to kibana|false|
|```--delete```|Delete from kibana|false|
|```--max_size```|Elasticsearch Max Hit Size|1024|

### Download
Downloads objects and templates from remote kibana to local.

~~~
python ./sync_kibana_objects.py http://elk-server:9200
~~~

### Upload
Uploads local objects and templates to remote kibana.

~~~
python ./sync_kibana_objects.py http://elk-server:9200 --upload
~~~

### Delete
Deletes local objects and templates from remote kibana.

~~~
python ./sync_kibana_objects.py http://elk-server:9200 --delete
~~~
