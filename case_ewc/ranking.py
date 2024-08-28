import json
import os

load_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/furia_matches.json'))
save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/furia_ranking.json'))

def create_furia_ranking():
    # Carregar o JSON
    with open(load_path, 'r') as file:
        data = json.load(file)

    rankings = {}

    # Iterar sobre todos os jogos no JSON
    for game, details in data["Jogos"].items():
        partidas = details["Partidas"]
        
        if game == "FC 24":
            # Para o "FC 24", há duas fases de partidas: Groupstage e FinalStage
            groupstage_partidas = details["Partidas"]["Groupstage"]
            finalstage_partidas = details["Partidas"]["FinalStage"]
            partidas = groupstage_partidas + finalstage_partidas

        score = 0
        for partida in partidas:
            if game == "FC 24":
                # No "FC 24", checar apenas pelo vencedor
                vencedor = partida.get("Vencedor")
                if vencedor == "Nathansr22" or vencedor == "Nathansr99":
                    score += 3
            else:
                # Para outros jogos, verificar se "FURIA" está em Time1 ou Time2
                team1 = partida.get("Time1")
                team2 = partida.get("Time2")
                placar1 = int(partida.get("Placar1", 0))
                placar2 = int(partida.get("Placar2", 0))

                if "FURIA" in [team1, team2]:
                    if (team1 == "FURIA" and placar1 > placar2) or (team2 == "FURIA" and placar2 > placar1):
                        score += 3

        rankings[game] = score

    # Ordenar os jogos pelo ranking
    sorted_rankings = dict(sorted(rankings.items(), key=lambda item: item[1], reverse=True))

    # Salvar o ranking em um arquivo de texto
    with open(save_path, 'w') as file:
        for game, points in sorted_rankings.items():
            file.write(f"{game}: {points} pontos\n")
