> JSON files should be in UTF-8 format, without a BOM.

# Export Kibana data

## Export new searches

~~~
curl -s -X GET http://10.10.10.10:9200/.kibana/search/Error/_source > ./searches/Errors.json
~~~

## Export new visualization

~~~
curl -s -X GET http://10.10.10.10:9200/.kibana/visualization/CPU-usage/_source > ./visualizations/CPU-usage.json
~~~

**NOTE: -**

- **10.10.10.10:9200** is the elasticsearch server ip and port

## Export new dashboard

~~~
curl -s -X GET http://10.10.10.10:9200/.kibana/dashboard/Packetbeat-Dashboard/_source > ./dashboards/Packetbeat-Dashboard.json
~~~

**NOTE: -**

- **10.10.10.10:9200** is the elasticsearch server ip and port

## Update Kibana visualizations and dashboards from elasticsearch

Dashboards and visualizations edited in the Kibana Web UI can be updated here if they already exist.

~~~
chmod u+x update_objects.sh
./update_objects.sh
~~~
