import requests
from bs4 import BeautifulSoup
import re
import argparse

parser = argparse.ArgumentParser(description='Get the words for the New York Times Spelling Bee')
parser.add_argument('--center_letter', type=str, help='The center letter for the spelling bee')
parser.add_argument('--letters', type=str, nargs='+', help='The letters for the spelling bee')


def get_letters(): 
    # TODO: Fix this to get the letters from the NYT website
    url = "https://www.nytimes.com/puzzles/spelling-bee"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the letters
    center_letter = soup.find('svg', class_='hive-cell center').text
    outer_letters = [letter.text for letter in soup.find_all('svg', class_='hive-cell outer')]

    letters = [center_letter] + outer_letters

    return center_letter, letters


def get_words(center_letter, letters):
    url = 'https://wordsapiv1.p.rapidapi.com/words/'

    letter_pattern = r'^[' + ''.join(letters) + r']*' + re.escape(center_letter) + r'[' + ''.join(letters) + r']*$'  # regex pattern to match words
    query_string = {'letterPattern': letter_pattern}

    headers = {
        "x-rapidapi-key": open('wordsAPI_key.txt').read().strip(),
	    "x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=query_string)
    response.raise_for_status()

    words = response.json()['results']['data']
    return [word for word in words if len(word) >= 4]


if __name__ == '__main__':
    args = parser.parse_args()
    # center_letter, letters = get_letters()
    center_letter = args.center_letter
    letters = [letter for letter in args.letters]
    words = get_words(center_letter, letters)
    print(words)

    