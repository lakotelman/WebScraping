from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
from pprint import pprint
import math

CWD = Path(__file__).parent
DRIVER_PATH = CWD / "chromedriver"

driver = webdriver.Chrome(str(DRIVER_PATH))
driver.get("https://modest-jennings-77f32e.netlify.app/")
sleep(3)

password_input = driver.find_element(By.TAG_NAME, "input")
password_input.send_keys("jZ3HF+}g")

sleep(1)
submit_pass = driver.find_element(By.TAG_NAME, "button")
submit_pass.click()
sleep(3)


page_soup = BeautifulSoup(driver.page_source, "html.parser")
driver.close()

player_table = page_soup.find("tbody")
player_list = [row for row in list(player_table.children) if row != "\n"]


class Player:
    all_players = []

    def __init__(self, name, team, position, age, gp, mpg):
        self.name = name
        self.team = team
        self.position = position
        self.age = age
        self.gp = gp
        self.mpg = mpg
        self.all_players.append(self)


for idx, tr in enumerate(player_list):
    stats_list = list(tr.children)[1:]
    Player(
        name=stats_list[0].text,
        team=stats_list[1].text,
        position=stats_list[2].text,
        age=stats_list[3].text,
        gp=stats_list[4].text,
        mpg=stats_list[5].text,
    )

# pprint([x.__dict__ for x in Player.all_players])

# TODO: Selenium Challenge Tasks (try using Selenium to filter the data on the page)
# * Find the player with the most MPG in the league
mpg_list = [(float(player.mpg), player.name) for player in Player.all_players]
print(max(mpg_list, key=lambda item: item[0]))


# * Find the name of the oldest player on each team, add them to a dictionary with each team's name being a key and the player's name being the value.
teams_age_list = {}
for player in Player.all_players:
    if player.team not in teams_age_list.keys():
        teams_age_list[player.team] = []
    teams_age_list[player.team].append(player)

for teams in teams_age_list:
    teams_age_list[teams] = max(teams_age_list[teams], key=lambda x: float(x.age)).name


# * Find the player with position F that had the least games played (gp) for each team, save as a dictionary. If there are multiple players, pick one.

f_players_least_games = {}
for player in Player.all_players:
    if player.team not in f_players_least_games.keys():
        f_players_least_games[player.team] = []
    f_players_least_games[player.team].append(player)

pprint(f_players_least_games)

for teams in f_players_least_games:
    f_players_least_games[teams] = min(f_players_least_games[teams], key=lambda x: float(x.gp) if x.position == " F " else math.inf).name

pprint(f_players_least_games)