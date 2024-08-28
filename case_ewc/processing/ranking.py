import json
import os

load_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/furia_matches.json'))
save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/furia_ranking.json'))

def calculate_winrate(partidas):
    total_partidas = len(partidas)
    vitorias = sum(1 for partida in partidas if partida["Resultado"] == "Vitória")
    return (vitorias / total_partidas) * 100 if total_partidas > 0 else 0

def create_furia_ranking():
    try:
        with open(load_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Arquivo {load_path} não encontrado.")
        return

    ranking = []
    for jogo, detalhes in data["Jogos"].items():
        winrate = calculate_winrate(detalhes["Partidas"])
        ranking.append({"Jogo": jogo, "Winrate (%)": winrate})

    ranking = sorted(ranking, key=lambda x: x["Winrate (%)"], reverse=True)

    ranking_data = {
        "Ranking Times Fúria EWC 2024": ranking
    }

    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(ranking_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    create_furia_ranking()
