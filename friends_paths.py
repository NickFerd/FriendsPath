import os
import requests
from tqdm import tqdm
from collections import deque
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from time import sleep


def main():
    """Script for building paths of friends from one VK user to another with VK_Api.
    Uses breadth-first search algorithm."""

    # Safe storage of API_TOKEN as environmental variable
    load_dotenv()
    access_token = os.getenv('API_TOKEN')  # use service token (applied for open accounts)

    #friends_path, distance = bfs(access_token, start_id='20067703', finish_id=16109999)
    #print(*friends_path)
    #print(f'You are {distance} handshakes away from this person')
    print(get_id(access_token, 'carrillo230502'))
    print(type(get_id(access_token, 'olgabzova')))



def get_friends_list(token, user_id):
    """Returns a list of user's friends IDs if account is open,
    Else returns empty list."""

    url = 'https://api.vk.com/method/friends.get'
    params = {'user_id': user_id,
              'access_token': token,
              'v': 5.122}

    resp = make_request(url, params)
    resp = resp.json()
    if 'response' in resp:  # check for correct response
        return resp['response']['items']
    else:
        return []


def bfs(token, start_id, finish_id):
    """Breadth-first algorithm
    Builds path if successful."""

    # BFS search
    distances = {start_id: 0}
    parents = {start_id: None}
    queue = deque([start_id])
    while finish_id not in distances and queue:
        current_user = queue.popleft()
        friends_list = get_friends_list(token, current_user)
        sleep(0.25)
        for user in tqdm(friends_list):
            if user not in distances:
                distances[user] = distances[current_user] + 1
                parents[user] = current_user
                queue.append(user)

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
    """Getting user id by his screen_name (domain name)"""

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


def visualize_path(path):
    """Man-understandable representation of friends path
            (first_name, last_name and link)"""


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

