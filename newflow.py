#!/usr/bin/env python
import requests
import json

flowurl = 'http://localhost:8008/flows/json?maxFlows=10&timeout=60'
flowID = -1
while 1 == 1:
  r = requests.get(flowurl + "&flowID=" + str(flowID))
  if r.status_code != 200: break
  flows = r.json()
  if len(flows) == 0: continue

  flowID = flows[0]["flowID"]
  flows.reverse()
  for f in flows:
    print json.dumps(f)
