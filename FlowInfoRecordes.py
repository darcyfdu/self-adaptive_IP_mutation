class FlowCountInfo(object):
    def __init__(self):
        self.count = 0
        self.srv_count = 0
        self.serror_rate = 0
        self.srv_serror_rate = 0
        self.rerror_rate = 0
        self.srv_rerror_rate = 0
        self.same_srv_rate = 0
        self.diff_srv_rate = 0
        self.srv_diff_host_rate = 0
        self.dst_host_count = 0
        self.dst_host_srv_count = 0
        self.dst_host_same_srv_rate = 0
        self.dst_host_diff_srv_rate = 0
        self.dst_host_same_src_port_rate = 0
        self.dst_host_srv_diff_host_rate = 0
        self.dst_host_serror_rate = 0
        self.dst_host_srv_serror_rate = 0
        self.dst_host_rerror_rate = 0
        self.dst_host_srv_rerror_rate = 0
class NetFlow(object):
    def __init__(self,key=None, bps=0):
        self.ipsource  = key[0]
        self.ipdestination = key[1]
        self.ipprotocol = key[2]
        self.sourceport = key[3]
        self.destinationport = key[4]
        self.flag = key[5]
        self.bps = bps
class FlowInfoRecorder(object):
    def __init__(self):
        self.firstSecondInfo  = []
        self.secondSecondInfo  = []
        self.hostInfo = []
    def get_hostInfo(self,index):
        return self.hostInfo[index]
    def add_hostInfo(self,hostInfo):
        if(self.get_hostInfo_size()>=100):
            del self.hostInfo[0]
        self.hostInfo.append(hostInfo)
        print 'add_hostInfo:',hostInfo.ipsource,hostInfo.ipdestination,hostInfo.ipprotocol,hostInfo.flag,hostInfo.bps
    def add_timeInfo(self,timeInfo):
        self.secondSecondInfo.append(timeInfo)
        print 'add_timeInfo:',timeInfo.ipsource,timeInfo.ipdestination,timeInfo.ipprotocol,timeInfo.flag,timeInfo.bps
    def get_hostInfo_size(self):
        return len(self.hostInfo)
    def get_secondSecondInfo_size(self):
        return len(self.secondSecondInfo)
    def get_firstSecondInfo_size(self):
        return len(self.firstSecondInfo)
    def sitch_timeInfo(self):
        self.firstSecondInfo = self.secondSecondInfo
        self.secondSecondInfo  = []
