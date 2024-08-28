import ingestion.apply as ingestion
import case_ewc.processing.ranking as ranking
import case_ewc.processing.chart as chart

if __name__ == "__main__":
    ingestion.get_ewc_furia_matches()
    ranking.create_furia_ranking()
    chart.display_ranking()