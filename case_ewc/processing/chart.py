import json
import os
import pandas as pd
import matplotlib.pyplot as plt

ranking_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/furia_ranking.json'))

def display_ranking():
    with open(ranking_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    ranking_df = pd.DataFrame(data["Ranking Times Fúria EWC 2024"])

    ranking_df = ranking_df.sort_values(by='Winrate (%)', ascending=True)

    ranking_df.plot.barh(x='Jogo', y='Winrate (%)', color='skyblue', edgecolor='black')
    plt.xlabel('Winrate (%)')
    plt.ylabel('Jogo')
    plt.title('Ranking Times Fúria EWC 2024 Por Winrate')
    plt.xlim(0, 100)
    
    plt.show()