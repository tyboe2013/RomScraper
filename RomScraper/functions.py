from bs4 import BeautifulSoup
import requests


# Scrapes for each piece of the rom info
def get_info(url):
    game_url = requests.get(url)
    # Grabs a portion of content to prevent possible scraping problems
    local_game_info = game_url.content[5800:11100]
    # Uses new page content
    local_game_info_soup = BeautifulSoup(local_game_info, 'html.parser')
    try:
        # Grabs Size of rom
        rom_size = local_game_info_soup.find('li', string=True).get_text().strip()
    except AttributeError:
        return None
        pass
    try:
        # Grabs Console
        rom_console = local_game_info_soup.find("strong").get_text()
        pass
    except AttributeError:
        return None
        pass
    try:
        # Grabs Title
        rom_title = local_game_info_soup.find('h1', class_="rom-title").get_text()
    except AttributeError:
        return None
        pass
    try:
        # Grabs Rating
        rom_rating = local_game_info_soup.find('div', {"class": "jq-stars ratings"})['rating']
    except AttributeError:
        return None
        pass
    try:
        # Grabs Total Votes
        rom_rating_total = local_game_info_soup.find('span', class_='rating-total-display').get_text()
    except AttributeError:
        return None
        pass
    try:
        # Grabs Region of rom
        rom_region = local_game_info_soup.select_one('ul.gameinfo > li').get_text().strip()
    except AttributeError:
        return None
        pass
    return rom_console, rom_title, rom_rating, rom_rating_total, rom_region, rom_size


if __name__ == "__main__":
    url = "https://www.romsgames.net/nintendo-ds-rom-pokemon-platinum-version/"
    info = get_info(url)
    print(info)
