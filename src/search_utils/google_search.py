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

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from common_utils import set_env


hl_map = {
    "Afrikaans": "af",
    "Akan": "ak",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bemba": "bem",
    "Bengali": "bn",
    "Bihari": "bh",
    "Bork, bork, bork!": "xx-bork",
    "Bosnian": "bs",
    "Breton": "br",
    "Bulgarian": "bg",
    "Cambodian": "km",
    "Catalan": "ca",
    "Cherokee": "chr",
    "Chichewa": "ny",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "Elmer Fudd": "xx-elmer",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Ewe": "ee",
    "Faroese": "fo",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Ga": "gaa",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Guarani": "gn",
    "Gujarati": "gu",
    "Hacker": "xx-hacker",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Interlingua": "ia",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Kinyarwanda": "rw",
    "Kirundi": "rn",
    "Klingon": "xx-klingon",
    "Kongo": "kg",
    "Korean": "ko",
    "Krio (Sierra Leone)": "kri",
    "Kurdish": "ku",
    "Kurdish (Soranî)": "ckb",
    "Kyrgyz": "ky",
    "Laothian": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Lozi": "loz",
    "Luganda": "lg",
    "Luo": "ach",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mauritian Creole": "mfe",
    "Moldavian": "mo",
    "Mongolian": "mn",
    "Montenegrin": "sr-ME",
    "Nepali": "ne",
    "Nigerian Pidgin": "pcm",
    "Northern Sotho": "nso",
    "Norwegian": "no",
    "Norwegian (Nynorsk)": "nn",
    "Occitan": "oc",
    "Oriya": "or",
    "Oromo": "om",
    "Pashto": "ps",
    "Persian": "fa",
    "Pirate": "xx-pirate",
    "Polish": "pl",
    "Portuguese (Brazil)": "pt-BR",
    "Portuguese (Portugal)": "pt-PT",
    "Punjabi": "pa",
    "Quechua": "qu",
    "Romanian": "ro",
    "Romansh": "rm",
    "Runyakitara": "nyn",
    "Russian": "ru",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Serbo-Croatian": "sh",
    "Sesotho": "st",
    "Setswana": "tn",
    "Seychellois Creole": "crs",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhalese": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Spanish (Latin American)": "es-419",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Tigrinya": "ti",
    "Tonga": "to",
    "Tshiluba": "lua",
    "Tumbuka": "tum",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Twi": "tw",
    "Uighur": "ug",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Wolof": "wo",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}


lr_map = {'Afrikaans': 'lang_af',
 'Arabic': 'lang_ar',
 'Armenian': 'lang_hy',
 'Belarusian': 'lang_be',
 'Bulgarian': 'lang_bg',
 'Catalan': 'lang_ca',
 'Chinese (Simplified)': 'lang_zh-CN',
 'Chinese (Traditional)': 'lang_zh-TW',
 'Croatian': 'lang_hr',
 'Czech': 'lang_cs',
 'Danish': 'lang_da',
 'Dutch': 'lang_nl',
 'English': 'lang_en',
 'Esperanto': 'lang_eo',
 'Estonian': 'lang_et',
 'Filipino': 'lang_tl',
 'Finnish': 'lang_fi',
 'French': 'lang_fr',
 'German': 'lang_de',
 'Greek': 'lang_el',
 'Hebrew': 'lang_iw',
 'Hindi': 'lang_hi',
 'Hungarian': 'lang_hu',
 'Icelandic': 'lang_is',
 'Indonesian': 'lang_id',
 'Italian': 'lang_it',
 'Japanese': 'lang_ja',
 'Korean': 'lang_ko',
 'Latvian': 'lang_lv',
 'Lithuanian': 'lang_lt',
 'Norwegian': 'lang_no',
 'Persian': 'lang_fa',
 'Polish': 'lang_pl',
 'Portuguese': 'lang_pt',
 'Romanian': 'lang_ro',
 'Russian': 'lang_ru',
 'Serbian': 'lang_sr',
 'Slovak': 'lang_sk',
 'Slovenian': 'lang_sl',
 'Spanish': 'lang_es',
 'Swahili': 'lang_sw',
 'Swedish': 'lang_sv',
 'Thai': 'lang_th',
 'Turkish': 'lang_tr',
 'Ukrainian': 'lang_uk',
 'Vietnamese': 'lang_vi'}

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
            raise("HTTP Error:", e)

        except requests.exceptions.ConnectionError as e:
            raise("Error Connecting:", e)

        except requests.exceptions.Timeout as e:
            raise("Timeout Error:", e)

        except requests.exceptions.RequestException as e:
            raise("Something Else:", e)
        except Exception as e:
            raise("Something went wrong!", e)

    def _google_search_items(self) -> dict:
        if self.response is None:
            return None
        soup = BeautifulSoup(self.response.content, "html.parser")
        search_results = soup.find_all("div", class_="g")

        res = {}

        valid_idx = 0
        for idx, hit in enumerate(search_results):
            try:
                top_url = hit.find("a")["href"]
                top_title = hit.find("h3", class_="LC20lb MBeuO DKV0Md").text
                top_logo = hit.find("img", class_="XNo5Ab").get("src")
                res[valid_idx] = {}
                res[valid_idx]["title"] = top_title
                res[valid_idx]["url"] = top_url
                res[valid_idx]["logo"] = top_logo
                valid_idx += 1
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
