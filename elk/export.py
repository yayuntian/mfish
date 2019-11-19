import json
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="http://elasticsearch:9200/")
query_json = {
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        "@timestamp": {
                            "gte": "2019-10-28T18:00:34.402Z",
                            "lte": "2019-10-28T18:14:44.924Z"
                        }
                    }
                }
            ],
            "filter": [
                {
                    "multi_match": {
                        "type": "phrase",
                        "query": "8205"
                    }
                }
            ]
        }
    }
}


def export():
    query = es.search(index='tms-all', body=query_json, scroll='5m', size=100)

    results = query['hits']['hits']
    total = query['hits']['total']
    scroll_id = query['_scroll_id']

    batch = int(total['value'] / 100) + 1
    for i in range(0, batch):
        query_scroll = es.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
        results += query_scroll

    with open('/tmp/data.json', 'w', newline='', encoding='utf-8') as f:
        for res in results:
            json.dump(res['_source'], f)
            f.write('\n')

    print('done!')


if __name__ == '__main__':
    export()
