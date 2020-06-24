import json
from elasticsearch import Elasticsearch



# pip3 install  elasticsearch==7.0.2  -i https://mirrors.aliyun.com/pypi/simple/

es = Elasticsearch(hosts="http://elasticsearch:9200/")
query_json = {
    "query": {
        "bool": {
            "must": [
                {
                "match_phrase": {
                    "app_id.keyword": {
                      "query": "9t5s5iaq"
                    }
                  }
                },
                {
                    "range": {
                        "@timestamp": {
                            "format": "strict_date_optional_time",
                            "gte": "2020-04-14T07:00:00.000Z",
                            "lte": "2020-04-14T07:59:59.000Z"
                        }
                    }
                }
            ]
        }
    }
}


def export():
    query = es.search(index='new-apm-alive-2020.04.14', body=query_json, scroll='5m', size=100)

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
