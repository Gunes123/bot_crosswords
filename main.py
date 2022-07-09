"""bot_crosswords"""
import json
import logging
import requests
from bs4 import BeautifulSoup

def save_records(arr):
    """append arr element to file"""
    with open('clues.json', 'r+') as json_file,open('clues.json', 'w') as json_file_w:
        try:
            json_data = json.loads(json_file)
            for rec in arr:
                json_data.append(rec)
            json.dump(json_data, json_file_w)
        except TypeError:
            json.dump(arr, json_file_w)
        return


def get_default(mod):
    """return default clue obj"""
    if mod == 0:
        return {'Group': 'Across', 'Number': '', 'String': ''}
    return {'Group': 'Down', 'Number': '', 'String': ''}


def get_clue():
    """get clue data"""
    try:
        url = "https://www.nytimes.com/crosswords/game/mini"
        _r = requests.get(url)
        soup = BeautifulSoup(_r.content, "html.parser")
        article_element = soup.find("section", attrs={"class": "Layout-clueLists--10_Xl"})
        title_sep = "div[class=ClueList-wrapper--3m-kd] > h3"
        title_arr = article_element.select(title_sep)
        counter = 0
        json_arr = []

        for i in range(len(title_arr)):
            print("=== " + title_arr[i].text + " ===")
            count = len(article_element.select("div:nth-child(" + str(i + 1) + ")>ol>li>span"))
            num_arr = article_element.select("div:nth-child(" + str(i + 1) + ")>ol>li>span")
            clue=get_default(i)
            for j in range(count):
                if counter % 2 == 0:
                    clue['Number'] = num_arr[j].text
                else:
                    clue['String'] = num_arr[j].text
                    print(str(clue['Number']) + ". " + clue['String'])
                    json_arr.append(clue)
                    clue=get_default(i)
                counter += 1
        save_records(json_arr)
        logging.info("SUCCESS!!")
    except OSError as err:
        logging.error("ERROR: %s",err)
    except ValueError as err:
        logging.error("ERROR: %s",err)
    except Exception as err:
        logging.error("ERROR: %s",err)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_clue()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
