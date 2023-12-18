import requests
from requests import Response
from dotenv import load_dotenv
import os


def fetchInput(url: str) -> Response:
    load_dotenv()
    headers = {
        'cookie': f'session={os.environ["SESSION"]}'
    }
    page = requests.get(url, headers=headers)
    return page


def loadInputFile(name: str) -> str:
    with open(f"inputs/{name}", 'r') as f:
        return f.read()
