import requests
from bs4 import BeautifulSoup


def help():
    print("Wordle is a game where you have to guess a 5-letter word in 6 tries.\n"
          "----------------------------------------------------------------------\n"
          "Input example:\n\n"
          "xxxxx r1 t2 ab -> letters 'r' and 't' are in the word, but not in the positions 1 and 2, respectively.\n"
          "\t\t  Used letters 'a' and 'b' but they are not in the word.\n\n"
          "xxtxx r2 cd -> letter 't' is in the correct position, letter 'r' is in the word, but not in the position 2.\n"
          "\t       Additionally used letter 'c' but it is also not in the word.\n"
          "----------------------------------------------------------------------\n")


def get_words(pattern, letters, used_letters):
    url = 'https://api.datamuse.com/words/'
    query_string = {
        'sp': pattern.replace('x', '?'), 
        'max': 10000
    }
    response = requests.get(url, params=query_string)
    response.raise_for_status()

    letters_dict = {int(element[1])-1: element[0] for element in letters}
    words = [entry['word'] for entry in response.json()]
    words = [word for word in words if match(word, letters_dict, used_letters)]
    return set(words)


def match(word, letters, used_letters):
    return all(word[position] != letter for position, letter in letters.items()) \
        and all(letter in word for letter in letters.values()) \
        and set(word) - set(used_letters) == set(word) \
        and len(word) == 5
    


if __name__ == '__main__':
    help()

    try:
        user_input = input('> ').split()
        pattern, letters, used_letters = user_input[0], user_input[1:-1], set([letter for letter in user_input[-1]])
        words = set()
        while pattern:
            result = get_words(pattern, letters, used_letters)
            words = words.intersection(result) if words else result
            print(words)
            user_input = input('> ').split()
            pattern, letters = user_input[0], user_input[1:-1]
            used_letters.update([letter for letter in user_input[-1]])
    except Exception:
        print('Game finished.')