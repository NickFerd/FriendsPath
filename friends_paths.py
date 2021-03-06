import os
import requests
from tqdm import tqdm
from collections import deque
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from time import sleep


def main():
    """Script for building paths of friends from one VK user to another using VK_Api.
    Uses breadth-first search algorithm."""

    # Safe storage of API_TOKEN as environmental variable
    load_dotenv()
    access_token = os.getenv('API_TOKEN')  # use service token (only applied for open accounts)

    start_id = get_id(access_token, 'id20067703')
    finish_id = get_id(access_token, 'keyaaa')

    # Build path if possible
    friends_path, distance = bfs(access_token, start_id=start_id, finish_id=finish_id)

    # Result output
    visualize_path(access_token, friends_path)
    print(f'You are {distance} handshakes away from this person!')


def get_friends_list(token, user_id, offset=0):
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
        print(f"{resp['error']['error_code']} - {resp['error']['error_msg']}, User ID - {user_id}")
        return []


def bfs(token, start_id, finish_id):
    """Breadth-first algorithm
    Builds path if successful."""

    # BFS search
    distances = {start_id: 0}
    parents = {start_id: None}
    queue = deque([start_id])
    offset = 0
    while finish_id not in distances and queue:
        current_user = queue.popleft()
        if offset:
            friends_list = get_friends_list(token, current_user, offset)
        else:
            friends_list = get_friends_list(token, current_user)
        offset = 0
        #sleep(0.25)
        if len(friends_list) != 0:
            for user in tqdm(friends_list):
                if user not in distances:
                    distances[user] = distances[current_user] + 1
                    parents[user] = current_user
                    queue.append(user)
            if len(friends_list) == 5000:
                queue.appendleft(current_user)
                offset = 5000

    # Build path
    path = [finish_id]
    try:
        parent = parents[finish_id]
    except KeyError:
        return None
    else:
        while parent is not None:
            path.append(parent)
            parent = parents[parent]
        return path[::-1], distances[finish_id]


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
        return None


def get_user_info(token, user_id):
    """Get user info"""

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


def visualize_path(token, path: list):
    """Man-readable representation of friends path
            (first_name, last_name and link)"""

    count = 1
    for user in path:
        info = get_user_info(token, user)
        first_name = info['response'][0]['first_name']
        last_name = info['response'][0]['last_name']
        domain = info['response'][0]['domain']

        print(f'{count}. {first_name} {last_name}')
        print(f'https://vk.com/{domain}')
        print()
        count += 1


def make_request(url, params=None):
    """Make Http Request"""
    try:
        resp = requests.get(url, params)

        # raise exceptions if error occurs
        resp.raise_for_status()
    except HTTPError as http_err:
        print('HTTP error occurred: ', http_err)
    except Exception as err:
        print('Other error occurred', err)
    else:
        return resp


if __name__ == '__main__':
    main()

