from google.cloud import bigquery

from app.config import PROJECT_ID, BQ_DATASET
from app.utils.logger import log_sql


def get_client():
    return bigquery.Client(project=PROJECT_ID)


def run_query(query: str, params=None):
    formatted_query = query.format(project=PROJECT_ID, dataset=BQ_DATASET)

    log_sql(formatted_query, params)

    job_config = bigquery.QueryJobConfig(
        query_parameters=params or []
    )

    client = get_client()
    query_job = client.query(formatted_query, job_config=job_config)
    return query_job.result().to_dataframe()