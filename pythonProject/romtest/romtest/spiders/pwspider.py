import json
import scrapy
from urllib.parse import urljoin
import re


class PwspiderSpider(scrapy.Spider):
    name = 'rom_info'

    def start_requests(self):
        console_list = ["nintendo-ds", "playstation-portable", "gameboy-advance",
                        "gamecube", "nintendo-wii", "super-nintendo", "playstation-2",
                        "nintendo-64", "playstation", "nintendo", "sega-genesis", "gameboy-color",
                        "dreamcast", "gameboy", ]
        for console in console_list:
            console_urls = f'https://www.romsgames.net/roms/{console}/'
            yield scrapy.Request(url=console_urls, callback=self.discover_console_urls,
                                 meta={'console': console, 'page': 1})

    def discover_console_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['console']

        ## Find Console URLs
        search_games = response.css("ul.rg-gamelist")
        for games in search_games:
            relative_url = games.css("li>a::(href)").get()
            game_url = urljoin("https://www.romsgames.net/roms", relative_url).split("?")[0]
            yield scrapy.Request(url=game_url, callback=self.parse_game_data, meta={'keyword': keyword, 'page': page})

    #Need to find game links with discover_console_urls and then use parse_game_data
    def discover_games:
    def parse_game_data(self, response):
        image_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0])
        yield {
            "name": response.css("h1.rom-title::text").get("").strip(),
            "lang": response.css("ul.gameinfo li::text")[0].get("").strip(),
            "size": response.css("ul.gameinfo li::text")[1].get("").strip(),
            "rating_count": response.css("span.rating-total-display ::text").get("").strip(),
            "images": image_data
        }
        pass
