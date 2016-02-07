"""
This module contains tools for extracting issue data from e-mail messages and
sending issues to github via the github api.

"""

import json
import logging
import os.path

import yaml


CONFIG_FILE = 'config.yaml'


def get_config():
    config_path = os.path.join(os.path.split(__file__)[0], CONFIG_FILE)
    with open(config_path) as f:
        config = yaml.load(f)
    return config


def create_issue(message, config, fetcher, method):
    title = extract_issue_title(message)
    body = extract_issue_body(message)
    payload = create_payload(title, body)
    url = create_url(config)
    headers = create_headers(config)
    result = fetcher(url=url, payload=json.dumps(payload), method=method, headers=headers)
    log_result(result)
    return


def extract_issue_title(message):
    """Extract issue title from the message."""
    return message.subject


def extract_issue_body(message):
    """Extract issue title and body from the message."""
    bodies = [body.decode() for _, body in message.bodies('text/plain')]
    return u''.join(bodies)


def create_payload(title, body):
    """Create payload mapping for the github api request."""
    return {
        'title': title,
        'body': body
    }


def create_url(config):
    """Create github api url."""
    return '{base_url}/repos/{repo_owner}/{repo_name}/issues'.format(**config)


def create_headers(config):
    """Create headers for github api request."""
    return {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token {}'.format(config['auth_token']),
        'Content-Type': 'application/json',
        'User-Agent': config['user_agent_string']
    }


def log_result(result):
    if 200 <= result.status_code <= 299:
        logging.info('Issue created succesfully: %s', json.loads(result.content))
    else:
        logging.error('Unexpected status code: %d.', result.status_code)
        logging.error('Response: %s', json.loads(result.content))
    return
