import pandas
import os,sys
import re
from threading import *

class ComSession:
    def __init__(self):        
        self.lvl = '0'
        self.active = False
        self.thread_ = Thread(target = self.run)

    def rdUsrMsg(self):
        #demo
        a = input()
        return a
    def changeLVL(self,ip):
        if ip == '#':
            self.lvl = self.lvl[:-2]
        elif ip == 'end':
            self.active = False
        else:
            self.lvl += (':'+str(ip))

    def run(self):
        while 1:
            self.sendMsg()
            self.changeLVL(self.rdUsrMsg())
            if not self.active:
                break
    def start(self):
        self.active = True
        self.thread_.start()
        while 1:
            if not self.active:
                print('感谢使用卡鲁bot')
                self.stop()
                break
    def stop(self):
        self.thread_.join(timeout = 0.5)
    def sendMsg(self):
        #demo
        print(self.lvl)
        print(m.getMsgById(self.lvl)[0])


class MsgGenerator:
    def __init__(self):

        file = self.readfile('msg.txt')
        self.msgBank = self.pack(file)
        self.normalizeId(self.msgBank)
        #print(self.getMsgById('0'))
    def readfile(self,filename):
        for root,dirs,files in os.walk("."):
            for d in dirs:
                if d == 'data':
                    with open(d+'/'+'msg.txt','r') as fd:
                        ret = fd.read()
                        
        return ret
    def pack(self,f):
        temp = ('id','content')
        temp_a = []
        t = f.split('#\n')
        for line in t:
            matched = re.match(r'^(?P<id>.+):(?P<content>.+)',line,re.DOTALL)
            #print(matched.group())
            if matched is not None:
                t_d = dict.fromkeys(temp)
                t_d['id'] = matched.group('id')
                t_d['content'] = matched.group('content')
                temp_a.append(t_d)
        return temp_a
    def normalizeId(self,bank):
        for msg in bank:
            if '\n' in msg['id']:
                msg['id'] = msg['id'][1:]

    def getMsgById(self,id_):
        return [msg['content'] for msg in self.msgBank if msg['id'] == id_]

m = MsgGenerator()
c = ComSession()
c.start()


                
        
        
        
            


