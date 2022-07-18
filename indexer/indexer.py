from retry import retry
from elasticsearch import Elasticsearch, helpers, ConnectionError
from glob import glob
import json

corpora_dir = '../corpora'

@retry(ConnectionError, max_delay=300, delay=5)
def indexer():
    print("Trying to connect to ElasticSearch...")
    es_client = Elasticsearch(
        hosts=[{"host": "es-container", "port": 9200, "scheme": "http"}]
    )
    return es_client

def load_json_corpora(dir):
    pathname = dir + "/**/*.json"
    print(pathname)
    json_filenames = glob(pathname, recursive=True)
    print(len(json_filenames))
    for filename in json_filenames:
        if 'averell' in filename:
            with open(filename, 'r') as open_file:
                yield json.load(open_file)

if __name__ == "__main__":
    es_client = indexer()
    print("Connected to ElasticSearch!")
    helpers.bulk(es_client, load_json_corpora(corpora_dir), index='corpora')
    