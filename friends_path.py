"""Simple script for building path of friends in VK"""

import os
from collections import deque
from time import sleep

from dotenv import load_dotenv
from tqdm import tqdm
import click

from api_utils import (
    get_user_info,
    get_friends_list,
    get_id
)


@click.command()
@click.option('--start', '-s', required=True,
              prompt='Insert starting person screen name',
              help='Start screen name.')
@click.option('--finish', '-f', required=True,
              prompt="Insert ",
              help='Finish screen name.')
def main(start: str, finish: str):
    """CLI script for building paths of friends from one VK user to another
    using VK_Api.
    Uses breadth-first search algorithm."""

    # Safe storage of API_TOKEN as environmental variable
    load_dotenv()
    access_token = os.getenv('API_TOKEN')  # (only applied for open accounts)

    start_id = get_id(access_token, start)
    finish_id = get_id(access_token, finish)

    # Build path if possible
    friends_path, distance = bfs(access_token, start_id=start_id,
                                 finish_id=finish_id)

    # Result output
    visualize_path(access_token, friends_path)
    print(f'These people {distance} handshakes away from each other!')


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
        sleep(0.4)  # VK API has limit of 3 requests per second

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
        return [], {}
    else:
        while parent is not None:
            path.append(parent)
            parent = parents[parent]
        return path[::-1], distances[finish_id]


def visualize_path(token, path: list):
    """Man-readable representation of friends path
            (first_name, last_name and link)"""

    for index, user in enumerate(path, start=1):
        info = get_user_info(token, user)
        first_name = info['response'][0]['first_name']
        last_name = info['response'][0]['last_name']
        domain = info['response'][0]['domain']

        print(f'{index}. {first_name} {last_name}')
        print(f'https://vk.com/{domain}')


if __name__ == '__main__':
    main()

