import requests
import sys
import os
import json
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from utils.constants import TEAM, CS_URL

save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/furia_matches.json'))

def get_cs_matches():
    response = requests.get(CS_URL)

    if response.status_code == 200:
        html_content = response.text

        match_results = extract_results(html_content)

        try:
            with open(save_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"Jogos": {}}

        data["Jogos"]["Counter Strike"] = {
            "Stage": "",
            "Partidas": match_results
        }

        with open(save_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    else:
        return

def extract_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    match_results = []

    round_centers = soup.find_all('div', class_='brkts-round-center')

    for round_center in round_centers:
        teams = round_center.find_all('div', class_='brkts-opponent-entry')
        if len(teams) == 2:
            team1_name = teams[0].get('aria-label')
            team1_score = int(teams[0].find('div', class_='brkts-opponent-score-inner').text.strip())
            team2_name = teams[1].get('aria-label')
            team2_score = int(teams[1].find('div', class_='brkts-opponent-score-inner').text.strip())

            if team1_score > team2_score:
                winner = team1_name
            elif team2_score > team1_score:
                winner = team2_name
            else:
                winner = "Draw"

            if TEAM in team1_name or TEAM in team2_name:
                match_result = {
                    "Time1": team1_name,
                    "Time2": team2_name,
                    "Placar1": team1_score,
                    "Placar2": team2_score,
                    "Vencedor": winner
                }
                match_results.append(match_result)

    return match_results
