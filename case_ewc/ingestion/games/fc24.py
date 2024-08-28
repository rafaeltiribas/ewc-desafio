import requests
import os
import sys
import json
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from utils.constants import FC_URL_GROUPSTAGE, FC_URL

save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/furia_matches.json'))

def get_fc_matches():
    groupstage_matches = get_groupstage_matches()
    final_stage_matches = get_final_stage_matches()

    try:
        with open(save_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"Jogos": {}}

    data["Jogos"]["FC 24"] = {
        "Stage": "",
        "Partidas": {
            "Groupstage": groupstage_matches,
            "FinalStage": final_stage_matches
        }
    }

    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_final_stage_matches():
    response = requests.get(FC_URL)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'lxml')

        partidas = soup.find_all(class_="brkts-round-center")

        results = []
        for match in partidas:
            opponent_entries = match.find_all('div', class_='brkts-opponent-entry')
            if len(opponent_entries) >= 2:
                player1_name = opponent_entries[0].find('span', class_='name').text.strip()
                player1_score = opponent_entries[0].find('div', class_='brkts-opponent-score-inner').text.strip()
                
                player2_name = opponent_entries[1].find('span', class_='name').text.strip()
                player2_score = opponent_entries[1].find('div', class_='brkts-opponent-score-inner').text.strip()
                
                if 'Nathansr99' in player1_name or 'Nathansr99' in player2_name:
                    result = {
                        "Time1": player1_name,
                        "Time2": player2_name,
                        "Placar1": player1_score,
                        "Placar2": player2_score
                    }
                    results.append(result)

        return results
    else:
        print(f"Erro: {response.status_code}")
        return []

def get_groupstage_matches():
    response = requests.get(FC_URL_GROUPSTAGE)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        template_boxes = soup.find_all('div', class_='template-box')
        matches = []

        for box in template_boxes:
            matchlists = box.find_all('div', class_=['brkts-matchlist', 'brkts-matchlist-collapsible', 'brkts-matchlist-attached'])
            for matchlist in matchlists:
                match_items = matchlist.find_all('div', class_=['brkts-matchlist-match', 'brkts-match-has-details', 'brkts-match-popup-wrapper'])
                for match in match_items:
                    player_names = match.find_all('span', class_='name')
                    if any('Nathan' in name.get_text(strip=True) for name in player_names):
                        try:
                            player1 = match.find('div', class_='brkts-matchlist-cell brkts-matchlist-opponent brkts-matchlist-slot-winner brkts-opponent-hover')
                            player2 = match.find('div', class_='brkts-matchlist-cell brkts-matchlist-opponent brkts-opponent-hover')

                            score1 = match.find('div', class_='brkts-matchlist-cell brkts-matchlist-score brkts-matchlist-slot-bold brkts-opponent-hover')
                            score2 = match.find('div', class_='brkts-matchlist-cell brkts-matchlist-score brkts-opponent-hover')

                            if not player1 or not player2:
                                raise ValueError("Informações dos jogadores ausentes na partida")

                            player1_name = player1.find('span', class_='name').text.strip()
                            player2_name = player2.find('span', class_='name').text.strip()
                            score1_value = score1.get_text(strip=True)
                            score2_value = score2.get_text(strip=True)

                            winner = player1_name if int(score1_value) > int(score2_value) else player2_name

                            match_result = {
                                "Time1": player1_name,
                                "Time2": player2_name,
                                "Placar1": score1_value,
                                "Placar2": score2_value,
                                "Vencedor": winner
                            }
                            matches.append(match_result)
                        except Exception as e:
                            print(f'Erro ao processar match: {e}')

        return matches
    else:
        print(f"Erro: {response.status_code}")
        return []
