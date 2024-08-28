import requests
from bs4 import BeautifulSoup
import sys
import os
import json
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from utils.check_win import furia_win
from utils.constants import SF6_URL, SF6_PLAYER

save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/furia_matches.json'))

def get_sf6_matches():
    try:
        response = requests.get(SF6_URL)
        response.raise_for_status()
        html_content = response.text
    except requests.RequestException as e:
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    match_rows = soup.find_all('tr', class_='match-row')
    match_results = []

    for row in match_rows:
        players = row.find_all('span', style="white-space: pre")
        if len(players) == 2:
            player1 = players[0].get_text(strip=True)
            player2 = players[1].get_text(strip=True)

            if player1 == SF6_PLAYER or player2 == SF6_PLAYER:
                scores = row.find_all('td', align="center", width="10%")
                if len(scores) == 2:
                    try:
                        score1 = int(re.findall(r'\d+', scores[0].get_text(strip=True))[0])
                        score2 = int(re.findall(r'\d+', scores[1].get_text(strip=True))[0])
                    except (ValueError, IndexError):
                        continue

                    result = ""
                    if player1 == SF6_PLAYER:
                        result = "Vitória" if furia_win(score1, score2) else "Derrota"
                    else:
                        result = "Vitória" if furia_win(score2, score1) else "Derrota"

                    match_result = {
                        "Time1": player1,
                        "Time2": player2,
                        "Placar1": score1,
                        "Placar2": score2,
                        "Resultado": result
                    }
                    match_results.append(match_result)

    try:
        with open(save_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"Jogos": {}}

    data["Jogos"]["Street Fighter 6"] = {
        "Partidas": match_results
    }

    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
