import influxdb_client
import json
from django.http import JsonResponse
import datetime


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

bucket = "Temperature"
org = "b3b0d52dc711fb48"
token = "te75Y29_sbWgwok5AZfR1DNazghXhoXn-tbP4767qrOrFCYu0Jp6LbLBpjvcEsLkbhcWTfTyX6dyRHAfmnFPRg=="
# Store the URL of your InfluxDB instance
url = "https://europe-west1-1.gcp.cloud2.influxdata.com"


def get_data(request):
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    query_api = client.query_api()
    query = 'from(bucket: "Temperature")\
      |> range(start: -7d)\
      |> filter(fn: (r) => r["SSID"] == "Home line")\
      |> filter(fn: (r) => r["_field"] == "tempC" or r["_field"] == "tempF")'

    result = query_api.query(org=org, query=query)
    results = {
        "tempF": [],
        "tempC": []
    }

    for table in result:
        for record in table.records:
            results[record.get_field()].append([record.get_value(), record["_start"]])

    data = json.dumps(results, default=str)
    return JsonResponse(data, safe=False)