"""Helping functions for interactions with VK API"""

import requests


def make_request(url, params=None):
    """Make Http Request"""
    try:
        resp = requests.get(url, params)

        # raise exceptions if error occurs
        resp.raise_for_status()
    except requests.HTTPError as http_err:
        print('HTTP error occurred: ', http_err)
    except Exception as err:
        print('Other error occurred', err)
    else:
        return resp


def get_user_info(token, user_id) -> dict:
    """Get user info from API"""

    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': user_id,
        'fields': 'domain',
        'access_token': token,
        'v': 5.122
    }
    resp = make_request(url, params)
    resp = resp.json()
    return resp


def get_id(token, screen_name):
    """Getting user id by screen_name (domain name)"""

    url = 'https://api.vk.com/method/utils.resolveScreenName'
    params = {
        'screen_name': screen_name,
        'access_token': token,
        'v': 5.122
    }
    resp = make_request(url, params)
    resp = resp.json()
    if 'object_id' in resp['response']:
        return resp['response']['object_id']
    else:
        print("Can't resolve this user screen name - ", screen_name)
        return None


def get_friends_list(token, user_id, offset=0) -> list:
    """Returns a list of user's friends IDs if account is open,
    Else returns empty list."""

    url = 'https://api.vk.com/method/friends.get'
    params = {'user_id': user_id,
              'access_token': token,
              'v': 5.122,
              'offset': offset}

    resp = make_request(url, params)
    resp = resp.json()

    if 'response' in resp:  # check for correct response
        return resp['response']['items']
    elif 'error' in resp:
        print(f"{resp['error']['error_code']} - {resp['error']['error_msg']}, "
              f"User ID - {user_id}")
        return []
