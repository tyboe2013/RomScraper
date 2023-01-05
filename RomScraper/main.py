from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import csv
import os

url = 'https://www.romsgames.net/roms/'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

consoles = ["nintendo-64", "nintendo-ds", "nintendo-wii", "nintendo",
            "playstation", "playstation-2", "playstation-portable",
            "gameboy-color", "gameboy-advance", "gamecube", "sega-genesis"]

# Lists for all the rom info
Console = []
Title = []
Rating = []
Total_Votes = []
Region = []
Size = []
URLS = []
DL_LINKS = []

# Used to conjoin with incomplete href links
stripped_url = "https://www.romsgames.net"
DL_URL = "https://www.romsgames.net/download"

# Iterates through console list
for each_console in consoles:
    console_url = url + each_console
    # Sends request for each console link
    r_console = requests.get(console_url)
    soup_console = BeautifulSoup(r_console.content, 'html.parser')
    # Finds the games in console pages
    game_list = soup_console.find_all("ul", class_="rg-gamelist")
    # Iterates through game list
    # This main for loop scrapes first page
    for links in game_list:
        # Finds anchor tags inside the game list
        a_tag = links.find_all("a")
        # Iterates through the anchors and grabs the href link
        game_links = [link.get('href') for link in a_tag]
        print(game_links)
        # Iterates through the hrefs
        for games in game_links:
            # Makes the href a complete link
            base_url = stripped_url + games
            download_url = DL_URL + games
            URLS.append(base_url)
            game_url = requests.get(base_url)
            print(base_url)
            # Grabs a portion of content to prevent possible scraping problems
            local_game_info = game_url.content[5800:11100]
            # Uses new page content
            local_game_info_soup = BeautifulSoup(local_game_info, 'html.parser')
            try:
                # Grabs Size of rom
                rom_size = local_game_info_soup.find('li', string=True).get_text().strip()
                Size.append(rom_size)
            except AttributeError:
                Size.append(None)
                pass
            try:
                # Grabs Console
                rom_console = local_game_info_soup.find("strong").get_text()
                Console.append(rom_console)
                pass
            except AttributeError:
                Console.append(None)
                pass
            try:
                # Grabs Title
                rom_title = local_game_info_soup.find('h1', class_="rom-title").get_text()
                print(rom_title)
                # Appends Title to list for csv file
                Title.append(rom_title)
            except AttributeError:
                Title.append(None)
                pass
            try:
                # Grabs Rating
                rom_rating = local_game_info_soup.find('div', {"class": "jq-stars ratings"})['rating']
                Rating.append(rom_rating)
            except AttributeError:
                Rating.append(None)
                pass
            try:
                # Grabs Total Votes
                rom_rating_total = local_game_info_soup.find('span', class_='rating-total-display').get_text()
                Total_Votes.append(rom_rating_total)
            except AttributeError:
                Total_Votes.append(None)
                pass
            try:
                # Grabs Region of rom
                rom_region = local_game_info_soup.select_one('ul.gameinfo > li').get_text().strip()
                Region.append(rom_region)
            except AttributeError:
                Region.append(None)
                pass
            # Starts getting Download links
            driver.get(download_url)
            sleep(1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            rom_DL_Link = soup.find_all('form')
            for link in rom_DL_Link:
                rom = link.get("action")
                DL_LINKS.append(rom)
                print(rom)

    # Finds pages through pagination
    pagination = soup_console.find_all("ul", class_="pagination")
    # For loop to scrape every page after the first one
    for pages in pagination:
        # Finds anchor tags inside the game list
        links = pages.find_all("a", limit=35)
        # Iterates through the anchors and grabs the href link
        game_links = [link.get('href') for link in links]
        # Skips the first 3 to prevent scraping the same ones
        select_links = game_links[2:]
        print(select_links)

        # For loop makes links complete and requests to scrape new pages
        for next_link in select_links:
            # Makes the href a complete link
            next_page = stripped_url + next_link
            new_r = requests.get(next_page)
            # Uses new page content
            soup_page = BeautifulSoup(new_r.content, 'html.parser')

            # Finds anchor tags inside the game list
            game_list = soup_page.find_all("ul", class_="rg-gamelist")
            for links in game_list:
                # Finds anchor tags inside the game list
                a_tag = links.find_all("a")
                # Iterates through the anchors and grabs the href link
                game_links = [link.get('href') for link in a_tag]
                print(game_links)

                # Iterates through the hrefs
                for games in game_links:
                    # Makes the href a complete link
                    base_url = stripped_url + games
                    URLS.append(base_url)
                    download_url = DL_URL + games
                    print(download_url)
                    game_url = requests.get(base_url)
                    print(base_url)
                    # Grabs a portion of content to prevent possible scraping problems
                    local_game_info = game_url.content[5800:11100]
                    # Uses new page content
                    local_game_info_soup = BeautifulSoup(local_game_info, 'html.parser')
                    try:
                        # Grabs Size of rom
                        rom_size = local_game_info_soup.find('li', string=True).get_text().strip()
                        Size.append(rom_size)
                    except AttributeError:
                        Size.append(None)
                        pass
                    try:
                        # Grabs Console
                        rom_console = local_game_info_soup.find("strong").get_text()
                        Console.append(rom_console)
                        pass
                    except AttributeError:
                        Console.append(None)
                        pass
                    try:
                        # Grabs Title
                        rom_title = local_game_info_soup.find('h1', class_="rom-title").get_text()
                        print(rom_title)
                        # Appends Title to list for csv file
                        Title.append(rom_title)
                    except AttributeError:
                        Title.append(None)
                        pass
                    try:
                        # Grabs Rating
                        rom_rating = local_game_info_soup.find('div', {"class": "jq-stars ratings"})['rating']
                        Rating.append(rom_rating)
                    except AttributeError:
                        Rating.append(None)
                        pass
                    try:
                        # Grabs Total Votes
                        rom_rating_total = local_game_info_soup.find('span', class_='rating-total-display').get_text()
                        Total_Votes.append(rom_rating_total)
                    except AttributeError:
                        Total_Votes.append(None)
                        pass
                    try:
                        # Grabs Region of rom
                        rom_region = local_game_info_soup.select_one('ul.gameinfo > li').get_text().strip()
                        Region.append(rom_region)
                    except AttributeError:
                        Region.append(None)
                        pass
                    # Dynamic page had to use selenium
                    driver.get(download_url)
                    sleep(1)
                    dl_page_source = driver.page_source
                    soup = BeautifulSoup(dl_page_source, 'html.parser')

                    # Finds all Download links
                    rom_DL_Link = soup.find_all('form')
                    for link in rom_DL_Link:
                        rom = link.get("action")
                        DL_LINKS.append(rom)
                        print(rom)

# Takes items out of each list
series_Console = pd.Series(Console, name="Console")
series_Title = pd.Series(Title, name="Title")
series_Rating = pd.Series(Rating, name="Rating")
series_Total_Votes = pd.Series(Total_Votes, name="Total Votes")
series_Region = pd.Series(Region, name="Region")
series_Size = pd.Series(Size, name="Size")
series_URL = pd.Series(URLS, name="URL")

# Takes items out of series and formats it for csv conversion
df = pd.DataFrame({ 'Console': Console, 'Title': Title, 'Rating': Rating,
                    'Total Votes': Total_Votes, 'Region': Region, 'Size': Size,
                    'URL': URLS})

# Uses df to make the csv
df.to_csv('RomInfo.csv', index=False, encoding='utf-8')

# Cleans the csv the Download links for a downloader
text = open("RomInfo.csv", "r")
# Removes words from csv file
text = ''.join([i for i in text]) \
    .replace("Emulator", "")
x = open("RomInfo.csv", "w")
x.writelines(text)
x.close()


df = pd.DataFrame({'DL_LINKS': DL_LINKS})
df.to_csv('Links.csv', index=False, encoding='utf-8')

# Cleans the csv the Download links for a downloader
text = open("Links.csv", "r")
# Removes words from csv file
text = ''.join([i for i in text]) \
    .replace("/search/", "")
text_v2 = ''.join([i for i in text]) \
    .replace("DL_LINKS", "")
x = open("Links.csv", "w")
x.writelines(text_v2)
x.writelines(text)
x.close()

# Removes blank lines from csv file
with open("Links.csv") as input, open('Links_cleaned.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    for row in csv.reader(input):
        if any(field.strip() for field in row):
            writer.writerow(row)
