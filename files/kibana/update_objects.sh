#!/bin/bash

printf '=%.0s' {1..80}
echo

echo Objects

printf '=%.0s' {1..80}
echo

elasticsearch_host=http://10.10.10.10:9200
folders=(dashboards visualizations)

for d in "${folders[@]}";
do
  IFS=$'\n'
  for f in $(find ./$d -name '*.json');
  do
    filename=$(basename "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"

    echo "curl -s -X GET $elasticsearch_host/.kibana/${d%?}/$filename/_source?pretty=true > $f"
    curl -s -X GET $elasticsearch_host/.kibana/${d%?}/$filename/_source?pretty=true > $f
  done
done

python ./get_templates.py
