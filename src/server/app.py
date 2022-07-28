from flask import Flask, jsonify, make_response
import elasticsearch
from elasticsearch import Elasticsearch, helpers, ConnectionError
import rantanplan 

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def indexer():
    print("Trying to connect to ElasticSearch...")
    es_client = Elasticsearch(
        hosts=[{"host": "es-container", "port": 9200, "scheme": "http"}]
    )
    return es_client

es_client = indexer()


def convert_aggregation(es_data, keys_mapping, subagg):
    items = []
    for item in es_data:
        new_item = {};
        for k,v in item.items():
            if k == subagg:
                del v['sum_other_doc_count']
                del v['doc_count_error_upper_bound']
            new_item[keys_mapping[k]] = v
        items.append(item)
    return items
            


@app.route('/')
def hello_rantanplan():
    
    print("Connected to ElasticSearch!")
    return f"Rantanplan version {rantanplan.__version__}. ElasticSearch version {elasticsearch.__version__}" 


@app.route("/get_authors/", methods=["GET"])
def get_authors():
    search_query = {
        "size": 0,
        "aggs": {
            "authors": {
                "terms": {
                    "field": "author.keyword",
                    "size": 20
                },
                "aggs": {
                    "stanza_type": {
                        "terms": {
                            "field": "stanzas.stanza_type.raw",
                        }
                    }
                }
            }
        }
    }

    resp = es_client.search(index='corpora', body=search_query)
    print(resp['aggregations']['authors'])
    return make_response(jsonify(convert_aggregation(resp['aggregations']['authors']['buckets'], 
    {'key': 'author', 
    'doc_count': 'count', 
    'stanza_type': 'stanza_type'}, "stanza_type")), 200)
    
    
if __name__ == "__main__":    
    app.run(debug=True, host='0.0.0.0')

