#!/usr/bin/env python

import glob
import json
import urllib2
import codecs
import os

elasticsearch_host = 'http://10.10.10.10:9200'
templates_path = "./templates"

print ('=' * 80)
print 'Templates'
print ('=' * 80)

os.chdir(templates_path)
for filename in glob.glob("*.json"):
    file_title = os.path.splitext(filename)[0]
    print file_title

    full_path = os.path.abspath(filename)

    url = "%s/_template/%s?pretty=true" % (elasticsearch_host, file_title)
    json_data = urllib2.urlopen(url).read()
    data = json.loads(json_data)

    tempate_data = data.values()[0]

    file = codecs.open(full_path, "w", "utf-8-sig")
    file.write(json.dumps(tempate_data, indent=4, sort_keys=False))
    file.close()
