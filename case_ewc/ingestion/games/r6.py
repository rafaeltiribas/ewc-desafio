import sys
import os
import requests
from bs4 import BeautifulSoup
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from utils.check_win import furia_win
from utils.constants import R6_URL

save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/furia_matches.json'))

def get_r6_matches():
    r = requests.get(R6_URL)
    html_content = r.text

    soup = BeautifulSoup(html_content, 'lxml')

    partidas = soup.find_all(class_="brkts-round-center")

    furia_matches = []

    for partida in partidas:
        times = partida.find_all(class_="name hidden-xs")
        placar = partida.find_all(class_="brkts-opponent-score-inner")

        if any('FURIA' in time.text for time in times):
            if len(times) == 2 and len(placar) == 2:
                team1 = times[0].text.strip()
                team2 = times[1].text.strip()
                score1 = int(placar[0].text.strip())
                score2 = int(placar[1].text.strip())
                result = ""
                if team1 == "FURIA":
                    result = "Vitória" if furia_win(score1, score2) else "Derrota"
                else:
                    result = "Vitória" if furia_win(score2, score1) else "Derrota"

                match_result = {
                    "Time1": team1,
                    "Time2": team2,
                    "Placar1": score1,
                    "Placar2": score2,
                    "Resultado": result
                }
                furia_matches.append(match_result)

    try:
        with open(save_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"Jogos": {}}

    data["Jogos"]["Rainbow Six 6"] = {
        "Partidas": furia_matches
    }

    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

