import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:8161/api/jolokia"
user = "admin"
password = "admin"

payload = {
    "type": "read",
    "mbean": "org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName=*"
}

try:
    headers = {"Origin": "http://localhost"}
    response = requests.post(url, json=payload, auth=HTTPBasicAuth(user, password), headers=headers)
    response.raise_for_status()
    data = response.json()
    print("Connection Successful!")
    print(f"Status: {data.get('status')}")
    print(f"Value: {data.get('value')}")
except Exception as e:
    print(f"Connection Failed: {e}")
