import requests

r = requests.get(URI)
print(r.status_code)
data = r.json()
print data