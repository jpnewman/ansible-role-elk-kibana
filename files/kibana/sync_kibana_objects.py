#!/usr/bin/env python

"""This script downloads and import Kibana objects."""

import argparse
import urllib2
import fnmatch
import codecs
import json
import sys
import os
import re

FOLDER_OBJECT_KEY_DICT = {
    "dashboards": {
        "index": ".kibana",
        "type": "dashboard",
        "include": [
            "^artifactory$",
            "^redis$"
        ]
    },
    "searches": {
        "index": ".kibana",
        "type": "search",
        "include": [
            "^Errors$",
            "^Gerrit-.*$",
            "^artifactory_.*$",
            "^grokparsefailure$"
        ]
    },
    "visualizations": {
        "index": ".kibana",
        "type": "visualization",
        "include": [
            "^artifactory_.*$",
            "^redis-.*$"
        ]
    },
    "templates": {
        "index": "_template",
        "type": "",
        "command": "",
        "exclude": [
            "^filebeat$",
            "^packetbeat$",
            "^topbeat$",
            "^triggered_watches$",
            "^watch_history$",
            "^watches$"
        ]
    }
}

# http://blog.mathieu-leplatre.info/colored-output-in-console-with-python.html
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def __has_colors(stream, allow_piping=False):
    """Check if Console Has Color."""
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():   # not being piped or redirected
        return allow_piping  # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False


# Has Color Init
has_colors = __has_colors(sys.stdout, True)


# Support methods
def colorText(text, color=WHITE):
    """Color Text."""
    if has_colors:
        return "\x1b[1;%dm" % (30 + color) + str(text) + "\x1b[0m"

    return text


def print_color_text(msg, color=WHITE):
    """Print Color Text."""
    print(colorText(msg, color))


def header(msg, overline_char='=', underline_char='='):
    """Print Header."""
    print_color_text(overline_char * 80, CYAN)
    print_color_text(msg, CYAN)
    print_color_text(underline_char * 80, CYAN)


def sub_header(msg, overline_char='-', underline_char='-'):
    """Print Sub-Header."""
    header(msg, overline_char, underline_char)


def get_local_files(folder, file_filter='*.json'):
    """Get local Objects."""
    found_files = []
    for root, dirs, files in os.walk(folder):
        for filename in fnmatch.filter(files, file_filter):
            found_files.append(os.path.join(root, filename))

    return found_files


# Kibana API
def kibana_api_request(url, method='GET', filename=None):
    """Kibana API request."""
    data = {}

    if filename:
        curl_url = "curl -X%s %s -T %s" % (method, url, filename)
    else:
        curl_url = "curl -X%s %s" % (method, url)

    print_color_text(curl_url, MAGENTA)

    opener = urllib2.build_opener(urllib2.HTTPHandler)

    if filename:
        with open(filename) as f:
            file_data = f.read()

        request = urllib2.Request(url,
                                  data=file_data)

        request.add_header('Content-Type', 'application/json')
    else:
        request = urllib2.Request(url)

    request.get_method = lambda: method

    try:
        response = opener.open(request)

        data = json.loads(response.read())

        report_api_response(data)

    except urllib2.HTTPError as err:
        if err.code == 404:
            print("WARN: File not found: %s" % url)
        else:
            raise

    return data


def report_api_response(json_data):
    """Report API response."""
    output_data_name_dict = {
        "_version": "Version",
        "created": "Created",
        "acknowledged": "Acknowledged"
    }

    response_arr = []
    for json_name, name in output_data_name_dict.iteritems():
        if json_name in json_data:
            response_arr.append("%s: %r" % (name,
                                            json_data[json_name]))

    print('\t'.join(response_arr))

    if '_shards' in json_data and json_data['_shards']['failed']:
        print("ERROR: Upload failed!")


# Download methods
def download_via_api(es_url_data,
                     elasticsearch_host,
                     max_size,
                     folder):
    """Download from kibana."""
    if not os.path.isdir(folder):
        os.makedirs(folder)

    es_url = '/'.join([elasticsearch_host,
                      es_url_data['index'],
                      es_url_data['type']])
    es_url = es_url.rstrip('/')

    es_command = False
    if re.match('^_', es_url_data['index']):
        url = es_url
        es_command = True
    else:
        url = "%s/_search" % (es_url)

    # url += '?pretty=true' # NOTE: pretty output is done by 'json.dumps' in function 'save_objects'
    url += "?size=%s" % max_size

    data = kibana_api_request(url, 'GET')

    if es_command:
        save_templates(es_url_data, data, folder)
    else:
        save_objects(es_url_data, data, folder)


def should_save_data(es_url_data, test_string):
    """Filter Data."""
    if 'include' not in es_url_data and 'exclude' not in es_url_data:
        sys.stdout.write('+ ')
        return True

    if 'include' in es_url_data:
        combined_include = "(" + ")|(".join(es_url_data['include']) + ")"
        if re.match(combined_include, test_string):
            sys.stdout.write('+ ')
            return True

    if 'exclude' in es_url_data:
        combined_exclude = "(" + ")|(".join(es_url_data['exclude']) + ")"
        if re.match(combined_exclude, test_string):
            sys.stdout.write('- ')
            return False
    else:
        sys.stdout.write('- ')
        return False

    sys.stdout.write('+ ')
    return True


def save_objects(es_url_data, data, folder):
    """Save Objects."""
    print("Total '%s' objects found: %s" % (colorText(es_url_data['type'], WHITE),
                                            colorText(data['hits']['total'], WHITE)))

    for obj in data['hits']['hits']:
        if should_save_data(es_url_data, obj['_id']):
            print_color_text(obj['_id'], GREEN)

            ouput_file_path = os.path.join(folder, obj['_id']) + '.json'

            file = codecs.open(ouput_file_path, "w", "utf-8")
            file.write(json.dumps(obj['_source'], indent=4, sort_keys=False))
            file.close()
        else:
            print(obj['_id'])


def save_templates(es_url_data, data, folder):
    """Save Templates."""
    print("Total templates found: %d" % len(data))

    for template, template_data in data.iteritems():
        if should_save_data(es_url_data, template):
            print_color_text(template, GREEN)
            ouput_file_path = os.path.join(folder, template) + '.json'

            file = codecs.open(ouput_file_path, "w", "utf-8")
            file.write(json.dumps(template_data, indent=4, sort_keys=False))
            file.close()
        else:
            print(template)


# Upload methods
def upload_via_api(es_url_data, elasticsearch_host, folder):
    """Upload to kibana."""
    sub_header("Uploading...")

    files = get_local_files(folder)

    for filename in files:
        file_title = os.path.basename(os.path.splitext(filename)[0])
        print(file_title)

        es_url = '/'.join([elasticsearch_host,
                          es_url_data['index'],
                          es_url_data['type']])
        es_url = es_url.rstrip('/')

        url = "%s/%s" % (es_url,
                         file_title)

        kibana_api_request(url, 'PUT', filename)


# Delete methods
def delete_via_api(es_url_data, elasticsearch_host, folder):
    """Delete found local objects from kibana."""
    sub_header("Deleting...")

    files = get_local_files(folder)

    for filename in files:
        file_title = os.path.basename(os.path.splitext(filename)[0])
        print(file_title)

        es_url = '/'.join([elasticsearch_host,
                          es_url_data['index'],
                          es_url_data['type']])
        es_url = es_url.rstrip('/')

        url = "%s/%s" % (es_url,
                         file_title)

        kibana_api_request(url, 'DELETE')


# Main
def main():
    """Main."""
    parser = argparse.ArgumentParser(description='Get Kibana Templates')
    parser.add_argument('elasticsearch_host',
                        nargs='?',
                        default='http://10.10.10.10:9200',
                        help='Elasticsearch Host')
    parser.add_argument('--upload',
                        action='store_true',
                        default=False,
                        help='Upload objects and templates to kibana')
    parser.add_argument('--delete',
                        action='store_true',
                        default=False,
                        help='Delete objects and templates from kibana')
    parser.add_argument('--max_size',
                        type=int,
                        default='1024',
                        help='Elasticsearch Max Hit Size')
    args = parser.parse_args()

    args.elasticsearch_host = args.elasticsearch_host.rstrip('/')

    header('Sync Kibana Objects and Templates\n' +
           args.elasticsearch_host)

    for folder, es_url_data in FOLDER_OBJECT_KEY_DICT.iteritems():
        sub_header(folder)

        if args.upload:
            upload_via_api(es_url_data,
                           args.elasticsearch_host,
                           folder)
        elif args.delete:
            delete_via_api(es_url_data,
                           args.elasticsearch_host,
                           folder)
        else:
            download_via_api(es_url_data,
                             args.elasticsearch_host,
                             args.max_size,
                             folder)


if __name__ == "__main__":
    main()
