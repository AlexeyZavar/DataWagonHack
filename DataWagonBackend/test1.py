from pprint import pprint

import requests

# 55.8489488,38.0578153
resp = requests.get('http://localhost:5000/build_route?from=415&to=640')
res = resp.json()
pprint(res)
print(len(res))
