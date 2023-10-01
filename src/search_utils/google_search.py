from time import time
from pprint import pprint
import requests
import sys
import pathlib
import asyncio
from bs4 import BeautifulSoup
import re
import os
from enum import Enum

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from common_utils import set_env


class GoogleLang(str, Enum):
    en = "en"
    es = "es"
    fr = "fr"
    de = "de"
    it = "it"
    pt = "pt"
    ru = "ru"
    zh = "zh"
    ja = "ja"
    ko = "ko"
    ar = "ar"
    hi = "hi"
    bn = "bn"


class GoogleSearcher:
    def __init__(
        self,
        search_word: str,
        session: requests.Session,
        lang: str = "en",
        num: int = 10,
    ):
        self.search_word = search_word
        self.session = session
        self.lang = lang
        self.num = num

        self.base_url = "https://www.google.com/search"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            )
        }
        self.session.headers.update(self.headers)
        self._response = None

    async def _google_search(self):
        params = {
            "q": self.search_word.strip(),
            "hl": self.lang,
            "gl": "GB",
            "num": self.num,
        }

        try:
            print("Searching...")
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            if response.status_code == 200:
                print("Search completed!")
            self._response = response
            print("Status code:", self._response.status_code)
            print("URL:", self._response.url)

        except requests.exceptions.HTTPError as e:
            print("HTTP Error:", e)

        except requests.exceptions.ConnectionError as e:
            print("Error Connecting:", e)

        except requests.exceptions.Timeout as e:
            print("Timeout Error:", e)

        except requests.exceptions.RequestException as e:
            print("Something Else:", e)
        except Exception as e:
            print("Something went wrong!", e)

    def _google_search_items(self) -> dict:
        if self.response is None:
            return None
        soup = BeautifulSoup(self.response.content, "html.parser")
        search_results = soup.find_all("div", class_="g")

        res = {}

        for idx, hit in enumerate(search_results):
            try:
                top_url = hit.find("a")["href"]
                top_title = hit.find("h3", class_="LC20lb MBeuO DKV0Md").text
                top_logo = hit.find("img", class_="XNo5Ab").get("src")
                res[idx] = {}
                res[idx]["title"] = top_title
                res[idx]["url"] = top_url
                res[idx]["logo"] = top_logo
            except:
                pass

        return res

    @property
    def search_items(self):
        return self._google_search_items()
    
    @property
    def response(self):
        if self._response is None:
            print("Response is None!")
            return None
        return self._response


async def test():
    set_env()
    search_words = ["Asia Game"]
    lang = "en"
    num = 5

    # create a session
    with requests.Session() as session:
        for search_word in search_words:
            searcher = GoogleSearcher(search_word, session, lang=lang, num=num)
            await searcher._google_search()
            response = searcher.response
            # save 
            with open("response.html", "w") as f:
                f.write(response.text)
            res = searcher.search_items
            pprint(res)

if __name__ == "__main__":
    asyncio.run(test())
