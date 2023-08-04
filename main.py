import http.client as http_client
import json
import logging
import re
import time
from pathlib import Path

import click
import requests
from bs4 import BeautifulSoup


def validate_url(url):
    if not re.match(r"(http(s){0,1}:\/\/(www\.)*)([\w.#-])+(\/[\w.#-]+)*", url):
        raise click.BadParameter(message="Given url doesn't match HTTP(s) url pattern")
    return url


def validate_method(method):
    return method.upper()


def validate_headers(headers):
    # TODO, check headers :)
    if not headers:
        return None

    headers_dict = {}
    items = re.findall(r'[\w]+:[\w]+', str(headers))
    for item in items:
        key, value = item.split(':')
        key = key.lower()
        if key in headers_dict:
            print("Warning: Duplicate header: Header key {} is entered more than once".format(key))
        headers_dict.update({key: value})

    return headers_dict


def validate_queries(queries):
    if not queries:
        return None

    queries_dict = {}
    items = re.findall(r'[\w]+=[\w]+', str(queries))
    for item in items:
        key, value = item.split('=')
        key = key.lower()
        if key in queries_dict:
            print("Warning: Duplicate query param: Query param {} is entered more than once".format(key))
        queries_dict.update({key: value})

    return queries_dict


def validate_data(data, headers):
    if not data:
        return None

    content_type = None
    if headers is not None:
        content_type = headers.get('content-type')

    if content_type is None or content_type == "application/x-www-form-urlencoded":
        if not re.match(r"^([\w]+=[\w]+&)*([\w]+=[\w]+)$", data):
            print(
                "Warning: Bad formatted data: Given Data format doesn't match application/x-www-form-urlencoded pattern"
            )

    return data


def validate_json(json_str):
    if json_str is None:
        return None

    try:
        json.loads(json_str)
    except ValueError as e:
        print("Warning: Bad formatted json: Given JSON string format is not valid")

    return json_str


def validate_file_path(file_path):
    if file_path is None:
        return None
    with open(file_path, 'rb') as f:
        file_name = Path(file_path).name
        file_dict = {file_name: f.read()}
        return file_dict


def validate_timeout(timeout):
    if timeout is None:
        return None
    if timeout < 0:
        raise click.BadParameter(message="Timeout cannot be negative")
    return timeout


def update_headers(headers, data, json, file):
    if headers is None:
        headers = dict()

    if 'Content-Type' not in headers:
        parts = []
        if data is not None:
            parts.append('data')
        if json is not None:
            parts.append('json')
        if file is not None:
            parts.append('file')

        if len(parts) == 1:
            if parts[0] == 'data':
                headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
            if parts[0] == 'json':
                headers.update({'Content-Type': 'application/json'})
            if parts[0] == 'file':
                headers.update({'Content-Type': 'application/octet-stream'})

        elif len(parts) > 1:
            headers.update({'Content-Type': 'multipart/form-data'})
            raise click.BadArgumentUsage(
                message="HTTP request cannot contain `--data`, `--json` & `--file` arguments simultaneously"
            )

    return headers


def pprint_response(response):
    if response is None:
        print('Client did not receive any response')
        return

    # HEADERS
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print()

    # BODY
    date = response.headers.get('Date')
    content_length = int(response.headers.get('Content-Length', 0))
    content_type = response.headers.get('Content-Type')

    if content_type is None:
        print(response.content)
        return

    media_type, media_subtype = content_type.split('/')
    media_subtype = media_subtype.split('+')[0].split(';')[0]

    content = b""
    with open(f"./saved/file_{date}.{media_subtype}", 'wb') as f:
        with click.progressbar(length=content_length, label='Downloading') as bar:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                content += data
                bar.update(len(data))
                time.sleep(0.1)

    if media_type == "text" and media_subtype == 'html':
        print(BeautifulSoup(content, 'html.parser').prettify())
    # elif media_type == "text" or media_subtype == 'json':
    #     print(content)


@click.command()
@click.argument('url')
@click.option('-M', '--method',
              type=click.Choice(['GET', 'POST', 'PATCH', 'DELETE', 'PUT'], case_sensitive=False),
              default='GET')
@click.option('-H', '--headers', multiple=True)
@click.option('-Q', '--queries', multiple=True)
@click.option('-D', '--data')
@click.option('--json', 'json_str')
@click.option('--file', 'file_path', type=click.Path(exists=True))
@click.option('--timeout', type=int)
def main(url, method, headers, queries, data, json_str, file_path, timeout):
    url = validate_url(url)
    method = validate_method(method)
    headers = validate_headers(headers)
    queries = validate_queries(queries)
    data = validate_data(data, headers)
    json_str = validate_json(json_str)
    file_dict = validate_file_path(file_path)
    timeout = validate_timeout(timeout)

    headers = update_headers(headers, data, json_str, file_dict)

    response = requests.request(method=method, url=url, headers=headers,
                                params=queries, data=data, json=json_str,
                                files=file_dict, timeout=timeout, stream=True)

    pprint_response(response)


if __name__ == "__main__":
    debug = False
    if debug:
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

        logging.disable(logging.CRITICAL)

    main()
