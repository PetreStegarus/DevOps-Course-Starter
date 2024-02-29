import json
import requests
import os

TRELLO_HEADERS = {"Accept": "application/json"}
TRELLO_URL_BASE = "https://api.trello.com/1"
TRELLO_AUTH_QUERY = (
    f"key={os.environ.get('TRELLO_API_KEY')}&token={os.environ.get('TRELLO_API_TOKEN')}"
)
TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
TRELLO_LIST_ID_TO_DO = os.environ.get('TRELLO_LIST_ID_TO_DO')
TRELLO_LIST_ID_DOING = os.environ.get('TRELLO_LIST_ID_DOING')
TRELLO_LIST_ID_DONE = os.environ.get('TRELLO_LIST_ID_DONE')
TRELLO_LIST_ID_TO_TEXT = {
    TRELLO_LIST_ID_TO_DO: "Todo",
    TRELLO_LIST_ID_DOING: "Doing",
    TRELLO_LIST_ID_DONE: "Done",
}
TRELLO_TEXT_TO_LIST_ID = {
    "Todo": TRELLO_LIST_ID_TO_DO,
    "Doing": TRELLO_LIST_ID_DOING,
    "Done": TRELLO_LIST_ID_DONE,
}


def trello_item_to_item(trello_item):
    return {
        "id": trello_item["id"],
        "title": trello_item["name"],
        "status": TRELLO_LIST_ID_TO_TEXT[trello_item["idList"]],
    }


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    response = requests.request(
        "GET",
        f"{TRELLO_URL_BASE}/boards/{TRELLO_BOARD_ID}/cards",
        headers=TRELLO_HEADERS,
        params=f"{TRELLO_AUTH_QUERY}",
    )

    return [trello_item_to_item(item) for item in json.loads(response.text)]


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    response = requests.request(
        "POST",
        f"{TRELLO_URL_BASE}/cards",
        headers=TRELLO_HEADERS,
        params=f"{TRELLO_AUTH_QUERY}&idList={TRELLO_LIST_ID_TO_DO}&name={title}",
    )

    return response.text


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    item_id = item["id"]
    item_status = TRELLO_TEXT_TO_LIST_ID[item["status"]]
    response = requests.request(
        "PUT",
        f"{TRELLO_URL_BASE}/cards/{item_id}",
        headers=TRELLO_HEADERS,
        params=f"{TRELLO_AUTH_QUERY}&idList={item_status}",
    )

    return response.text
