# Desafio EWC

O **Desafio EWC** tem como objetivo gerar um ranking do desempenho dos times Fúria na Esports World Cup 2024. Para que o desafio fosse completado era necessário que a coleta de dados fosse feita de maneira automática! (Stack livre).

## Como foi feita a ingestão dos dados?

- 🔎**Web Scraping!**:
    - 🚨 A coleta dos dados de TODAS as partidas que a Fúria disputou no campeonato foi feita com Web Scraping!
    - 📚 Todos os dados do campeonato foram adquiridos da página do campeonato dentro da [Liquipedia](https://liquipedia.net/esports/Esports_World_Cup/2024).
    - 💡 O projeto foi desenvolvido de forma que com poucas alterações é possível gerar o ranking de QUALQUER time!
- 🤔 Por que não uma API?
    - 🚫 A maioria das API's disponíveis não cobriam os dados de todas as modalidades que a Fúria disputou.
    - 🙅‍♂️ Todas as API's disponíveis gratuitamente possuiam um limite de requisições ou menor gama de detalhes das partidas.

## Arquitetura

- 📚**O projeto está organizado da seguinte forma:**:
EWC Desafio
├── case_ewc
│   ├── ingestion
│   │   ├── scripts de ingestão dos dados via web scraping
│   ├── processing
│   │   ├── scripts de processamento dos dados para gerar o ranking e o gráfico
│   ├── main.py
├── data
│   ├── resultados das partidas em formato JSON
│   ├── ranking dos times FÚRIA em formato JSON
├── tests
│   ├── para testes unitários afim de verificar a funcionalidade do código
├── utils
│   ├── constantes e funções auxiliares
├── pyproject.toml
└── .tool-versions

## Requisitos

- Python (versão 3.8>)
- Dependências especificadas em **pyproject.toml**

### Instalação

1. Clone o repositório:

   \`\`\`bash
   git clone https://github.com/rafaeltiribas/ewc-desafio
   cd ewc-desafio
   \`\`\`

2. Instale as dependências:

   \`\`\`bash
   pip install .
   \`\`\`

3. Entre no diretório de execução:

   \`\`\`bash
   cd case_ewc
   \`\`\`

4. Rode o projeto:

   \`\`\`bash
   python main.go
   \`\`\`

## Execução

- **Resultados da Fúria**: Todos os resultados da Fúria na EWC 2024 são coletados e armazenados no diretório `data` no arquivo **furia_matches.json**, confira!
- **Ranking**: O ranking do time Fúria é gerado e armazenado no diretório `data` no arquivo **furia_ranking.json**, com os jogos que a Fúria disputou e o desempenho em cada modalidade!
- **Gráfico**: Um gráfico é impresso na tela para melhor visualização dos dados obtidos após a execução do projeto.

## Resultado

<p align="center">
  <img src="chart.png" width="528" height="272" alt="QR Code to join Limos"/>
</p>

## Contato

Para qualquer dúvida ou feedback, entre em contato comigo por [rafaeltiribas@outlook.com](mailto:rafaeltiribas@outlook.com).
