from bs4 import BeautifulSoup
import requests
import pandas as pd
import functions

# Used to conjoin with incomplete href links
stripped_url = "https://www.romsgames.net"

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

# Iterates through console list
for each_console in consoles:
    console_url = stripped_url + "/roms/" + each_console
    print(console_url)
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
            URLS.append(base_url)
            game_url = requests.get(base_url)
            print(base_url)
            # Calls a function to grab info from url
            game_info = functions.get_info(base_url)
            # Puts each piece of info into their specific list
            Console.append(game_info[0])
            Title.append(game_info[1])
            Rating.append(game_info[2])
            Total_Votes.append(game_info[3])
            Region.append(game_info[4])
            Size.append(game_info[5])

    # Finds pages through pagination
    pagination = soup_console.find_all("ul", class_="pagination")
    # For loop to scrape every page after the first one
    for pages in pagination:
        # Finds anchor tags inside the game list
        links = pages.find_all("a", limit=1)
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
                    # Calls a function to grab info from url
                    game_info = functions.get_info(base_url)
                    # Puts each piece of info into their specific list
                    Console.append(game_info[0])
                    Title.append(game_info[1])
                    Rating.append(game_info[2])
                    Total_Votes.append(game_info[3])
                    Region.append(game_info[4])
                    Size.append(game_info[5])


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
