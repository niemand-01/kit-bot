from queue import Queue,Empty
from threading import *
#import EVENT_ID

KEYWORD = {
    'zufang':['租房','出房','Zwi','Zwischen','Nach'],
    'ershou':['好物','二手','求好物','求二手'],
    'bangdai':['帮带','求帮带'],
    'jianzhi':['Job','兼职','工作','全职','HIWI','求兼职','求工作']，  
    }


EVENT_SHARE_1 = 'ZUFANG_OFFER'
EVENT_SHARE_2 = 'ZUFANG_BEG'
EVENT_SHARE_3 = 'ERSHOU_OFFER'
EVENT_SHARE_4 = 'ERSHOU_BEG'

EVENT_SHARE_5 = 'BANGDAI_OFFER'
EVENT_SHARE_6 = 'BANGDAI_BEG'
EVENT_SHARE_7 = 'JIANZHI_OFFER'
EVENT_SHARE_8 = 'JIANZHI_BEG'

EVENT_SHARE = [EVENT_SHARE_1,EVENT_SHARE_2,EVENT_SHARE_3,EVENT_SHARE_4,
               EVENT_SHARE_5,EVENT_SHARE_6,EVENT_SHARE_7,EVENT_SHARE_8]


ev_user = EventManager()
#4 event manager for 4 different group type, every manager is incharge of 6 groups
ev_group_1 = EventManager()
ev_group_2 = EventManager()
ev_group_3 = EventManager()
ev_group_4 = EventManager()

ev_sum = [ev_user,ev_group_2,ev_group_3,ev_group_4,ev_group_1]



##########################
"""事件对象"""
class Event:
    def __init__(self, type_=None):
        self.type_ = type_
        #事件信息
        self.dict_ = {}

##########################
class EventManager:
    def __init__(self):
        #事件队列 event queue
        self._eventQueue = Queue()
        #开关
        self._active = False
        #线程
        self._thread = Thread(target = self._run)
        #已经处理event count
        self.event_count = 0
        #响应函数集合
        self.event_handlers = {}

    def _run(self):
        print('{}_run'.format(self.event_count))

        while self._active == True:
            try:
                #最多阻塞时间1s，超过1s get不到产生empty error
                event = self._eventQueue.get(block = True,timeout = 1)
                self.event_process(event)
                self.event_count += 1
            except Empty:
                pass
            

    def event_process(self,event):
        """处理事件"""
        print('{}_event process'.format(self.event_count))
        #如果在处理函数中有对type_的函数
        if event.type_ in self.event_handlers:
            for handler in self.event_handlers[event.type_]:
                handler(event)


    def Start(self):
        self._active = True

        self._thread.start()

    def Stop(self):

        self._active = False
        #等待处理退出
        self._thread.join()

    def AddEventListener(self,type_,handler):
        #绑定事件和监听器响应函数
        #对于type = type_的 event 绑定handler函数解决
        try:
            handlerList = self.event_handlers[type_]

        #没有type_
        except KeyError:

            handlerList = []
            self.event_handlers[type_] = handlerList

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)



    def RemoveEventListener(self,type_,handler):
        try:
            handlerList = self.event_handlers[type_]
            # 如果该函数存在于列表中，则移除
            if handler in handlerList:
                handlerList.remove(handler)
            # 如果函数列表为空，则从引擎中移除该事件类型
            if not handlerList:
                del self.event_handlers[type_]
        except KeyError:
            pass

    #----------------------------------------------------------------------
    def SendEvent(self, event):
        """发送事件 = 向事件队列中存入事件"""
        print('{}_SendEvent'.format(self.event_count))
        self._eventQueue.put(event)

#identify event id through user package
class EventIdentifier:
    def __init__(self):
        #本地pack
        self.local_pack = {}
        #本地提取的msg
        self.local_msg = ''
        #用户不良行为bank
        self.user_misbavior_bank = {}
        #存储用户event的list 也是stack 可以append 和remove,用于存储用户最近event的细节，可能会发送[租房]然后发照片
        #{username:id,user_event_bank:{time:,last_5_event:}}
        self.local_event_bank ={}

        self.base = ['zufang','ershou','bangdai','jianzhi']

    def get_msg_type(self,pack):

    def is_text(self,pack):
        return False
    def is_user(self):

    def is_group(self):

    def word_detect(self,content):
        #return [topic,offer = 0/require = 1,hascontent?]
        #simplt detect
        #later will add more fine detect method
        for key,_list in KEYWORD.items():
            for itm in _list:
                try:
                    if content.index(itm) != -1:
                        if content.index('求') != -1:
                            return [key,1,True]
                        else:
                            return [key,0,True]
                except:
                    pass
        return [None,None,False]

    def get_event_type(self,word_detect):
        """
        input: ['zufang',1,True]
        
        """
        if word_detect[2] == False:
            return
        else:
            event = []
            for idx,value in enumerate(self.base):
                if value == word_detect[0]:
                    event_idx =(idx+1)*2
                    if is_offer:
                        event_idx -= 2
                        event['type'] = value 
                        event['event']= EVENT_SHARE[event_idx])
                        break
            return event
    def user_behavior_check(self,word_detect,msg):
        #check if user has sent the right msg in right group
        #if no user misbehavior point += 1
        #if point >5 ban user / remove user from group
        return False
                 


#produce event according to the event id, the relating info may vary      
class EventProducer:
    def __init__(self):
        for evM in ev_sum:
            evM.Start()
    def trigger_event(self,event_list):
        #send all the input events
        for event in event_list:
            ev = Event(type_ = event['event'],dict_=)
            if event['type'] == 'zufang':
                ev_group_1.SendEvent(ev)
            elif event['type'] == 'ershou':
                ev_group_2.SendEvent(ev)
            elif event['type'] == 'bangdai':
                ev_group_3.SendEvent(ev)
            elif event['type'] == 'jianzhi':
                ev_group_4.SendEvent(ev)

        print('Event Sent successful')


#handle the occuring event 
class EventHandler:
    def __init__(self):
        zu_handler = []
        er_handler = []
        ba_handler = []
        ji_handler = []
        us_handler = []
        #add all the handler to the corresponding eventmanager
        #ev_user,ev_group_2,ev_group_3,ev_group_4,ev_group_1
        for evM in ev_sum:
            if evM == ev_user:
                #add all us_handler to this manager
                #...
    def evt_usr_1():
        return

    def evt_share(self,event_type,msg):
        


"""    

class user:
    def __init__(self,eventManager):
        self._eventManager = eventManager

    def friend_request(self):
        event = Event(type_ = EVENT_USR_1)
        event.dict = 'want to add friend!'

        #add event to the queue
        self._eventManager.SendEvent(event)
        print('event sent!')

class controller:
    def __init__(self):
        self.time = ''
    def processEvent(self,event):
        print('get event')
        print('processing {}'.format(event.dict))

if __name__ == '__main__':

    controller1 = controller()
    
    evM = EventManager()
    #这个注册的处理函数名字,相当于C里面的define，复制黏贴函数名字，并非函数
    evM.AddEventListener(EVENT_USR_1,controller1.processEvent)
    evM.Start()
    
    user1 = user(evM)
    user1.friend_request()
    
"""
    


        
    
        
