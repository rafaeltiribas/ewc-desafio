import requests
import os
import json
from bs4 import BeautifulSoup
from utils.check_win import furia_win
from utils.constants import TEAM, CS_URL

save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/furia_matches.json'))

def get_cs_matches():
    response = requests.get(CS_URL)
    if response.status_code != 200:
        return

    html_content = response.text
    match_results = extract_results(html_content)

    try:
        with open(save_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"Jogos": {}}

    data["Jogos"]["Counter Strike"] = {"Partidas": match_results}

    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def extract_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    match_results = []

    for round_center in soup.find_all('div', class_='brkts-round-center'):
        teams = round_center.find_all('div', class_='brkts-opponent-entry')
        if len(teams) != 2:
            continue

        team1_name, team2_name = (team.get('aria-label') for team in teams)
        team1_score = int(teams[0].find('div', class_='brkts-opponent-score-inner').text.strip())
        team2_score = int(teams[1].find('div', class_='brkts-opponent-score-inner').text.strip())

        result = "Vitória" if (furia_win(team1_score, team2_score) if TEAM in team1_name else furia_win(team2_score, team1_score)) else "Derrota"

        if TEAM in team1_name or TEAM in team2_name:
            match_results.append({
                "Time1": team1_name,
                "Time2": team2_name,
                "Placar1": team1_score,
                "Placar2": team2_score,
                "Resultado": result
            })

    return match_results