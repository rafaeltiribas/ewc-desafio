import ingestion.apply as ingestion
import ranking

if __name__ == "__main__":
    ingestion.get_ewc_furia_matches()
    ranking.create_furia_rankin()
    