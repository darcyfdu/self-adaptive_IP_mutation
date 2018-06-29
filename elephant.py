#!/usr/bin/env python
import requests
import json
from threading import Timer
from FlowInfoRecordes import FlowInfoRecorder,NetFlow,FlowCountInfo
eventID = -1
#info_recorder = None
rt = 'http://127.0.0.1:8008'
url = rt+'/activeflows/ALL/test_flow/json?maxFlows=100&minValue=1&aggMode=edge'
def calculateInfo(key,info_recorder,flow_info):
    SYNHostCount = 0
    SYNServiceCount = 0
    for i in range(info_recorder.get_firstSecondInfo_size()):
        if(key[1] == info_recorder.firstSecondInfo[i].ipdestination):
            flow_info.count += 1
            if(info_recorder.firstSecondInfo[i].)
        if(key[4] == info_recorder.firstSecondInfo[i].destinationport):
            flow_info.srv_count += 1
        if(key[4] == info_recorder.firstSecondInfo[i].destinationport):
def sendRequest(info_recorder):
    info_recorder.sitch_timeInfo()
    r = requests.get(url)
    if r.status_code != 200: return
    flows = r.json()
    #print events
    #eventID = events[0]["flowN"]
    flows.reverse()
    flow_info = FlowCountInfo()
    for f in flows:
        bps = f['value']*8
        key =  f['key'].split(',')
        calculateInfo(key,info_recorder,flow_info)
        net_flow = NetFlow(key,bps)
        info_recorder.add_hostInfo(net_flow)
        info_recorder.add_timeInfo(net_flow)
    t = Timer(1, sendRequest,[info_recorder])
    t.start()
if __name__ == "__main__":  
    info_recorder = FlowInfoRecorder()
    flow =    {'keys':'ipsource,ipdestination,ipprotocol,or:tcpsourceport:udpsourceport:icmptype,or:tcpdestinationport:udpdestinationport:icmpcode,or:tcpflags:udp_offset:icmptype','value':'bytes','t':'2','log':'true'}
    #flow = {'keys':'node:inputifindex,ipsource,ipdestination','value':'bytes'}
    requests.put(rt+'/flow/test_flow/json',data=json.dumps(flow))

    #threshold = {'metric':'pair','value':1000000/8,'byFlow':True,'timeout':1}
    #requests.put(rt+'/threshold/elephant/json',data=json.dumps(threshold))

    #eventurl = rt+'/events/json?thresholdID=elephant&maxEvents=10&timeout=60'

    sendRequest(info_recorder)
