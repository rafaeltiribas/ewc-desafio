import requests
import os
import sys
import json
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from utils.constants import TEAM, SIGLA, ROCKET_LEAGUE_URL

save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/furia_matches.json'))

def get_rocket_matches():
    response = requests.get(ROCKET_LEAGUE_URL)

    if response.status_code == 200:
        html_content = response.text
        match_results = filter_team_matches(html_content)

        try:
            with open(save_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"Jogos": {}}

        data["Jogos"]["Rocket League"] = {
            "Partidas": match_results
        }

        with open(save_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    else:
        print(f"Erro: {response.status_code}")

def filter_team_matches(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    match_rows = soup.find_all('tr', class_='Match')
    match_results = []

    for match in match_rows:
        if match.find('span', {'data-highlightingclass': TEAM}):
            round_ = match.find('td', class_='Round').get_text(strip=True)
            team_left = match.find('td', class_='TeamLeft').get_text(strip=True)
            team_right = match.find('td', class_='TeamRight').get_text(strip=True)
            score = match.find('td', class_='Score').get_text(strip=True)

            result = determine_result(team_left, team_right, score)

            match_result = {
                "Round": round_,
                "Time1": team_left,
                "Time2": team_right,
                "Placar": score,
                "Resultado": result
            }

            match_results.append(match_result)

    return match_results

def determine_result(team_left, team_right, score):
    try:
        left_score, right_score = map(int, score.replace(' ', '').split(':'))
    except ValueError:
        return 'Erro ao interpretar o placar'

    is_team_left = SIGLA in team_left
    is_team_right = SIGLA in team_right

    if is_team_left and is_team_right:
        return 'Erro: Time encontrado em ambos os lados'
    elif is_team_left:
        return 'Vitória' if left_score > right_score else 'Derrota'
    elif is_team_right:
        return 'Vitória' if right_score > left_score else 'Derrota'
    else:
        return 'Não envolvido'