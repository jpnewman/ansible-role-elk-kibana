# jpnewman.elk-kibana

[![Ansible Role](https://img.shields.io/ansible/role/9589.svg?maxAge=2592000)](https://galaxy.ansible.com/jpnewman/elk-kibana/)
[![Build Status](https://travis-ci.org/jpnewman/ansible-role-elk-kibana.svg?branch=master)](https://travis-ci.org/jpnewman/ansible-role-elk-kibana)

This is a Ansible role to installs [kibana](https://www.elastic.co/products/kibana)

This role is based on role ```kibana``` <https://github.com/rueian/ansible-elk-example> by Rueian

For more information look at the following readme: -

- ```./files/kibana/README.md```
- ```./files/kibana/NOTES.md```

## Requirements

Ansible 2.x

## Role Variables

|Variable|Description|Default|
|---|---|---|
|```kibana_version```||5.3.0|
|```kibana_platform```||linux-x86_64|
|```kibana_package```||```kibana-{{ kibana_version }}-{{ kibana_platform }}```|
|```kibana_package_ext```||tar.gz|
|```kibana_download_url```||```"https://artifacts.elastic.co/downloads/kibana/{{ kibana_package }}.{{ kibana_package_ext }}"```|
|```kibana_beats_dashboard_version```||1.3.1|
|```kibana_beats_dashboard_file_title```||```"beats-dashboards-{{ kibana_beats_dashboard_version }}"```|
|```kibana_beats_dashboard_file_ext```||zip|
|```kibana_beats_dashboard_url```||```"https://download.elastic.co/beats/dashboards/{{ kibana_beats_dashboard_file_title }}.{{ kibana_beats_dashboard_file_ext }}"```|
|```kibana_elasticsearch_url```||'http://elk-server:9200'|
|```apt_cache_valid_time```||600|
|```kibana_dashboards_folder```||kibana/dashboards/*.json|
|```kibana_searches_folder```||kibana/searches/*.json|
|```kibana_visaulizations_folder```||kibana/visualizations/*.json|
|```kibana_elasticsearch_templates```||```kibana/templates/*.json```|
|```kibana_init_script_url```||```https://gist.githubusercontent.com/thisismitch/8b15ac909aed214ad04a/raw/bce61d85643c2dcdfbc2728c55a41dab444dca20/kibana4```|

## Dependencies

  - jpnewman.nginx
  - jpnewman.json

## Example Playbook

    - hosts: servers
      roles:
         - { role: jpnewman.elk-kibana, tags: ["kibana"] }

## License

MIT / BSD

## Author Information

John Paul Newman
