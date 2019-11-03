from queue import Queue,Empty
from threading import *


##########################
"""事件对象"""
class Event:
    def __init__(self, type_=None):
        self.type_ = type_
        #事件信息
        self.dict = {}

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





EVENT_USR_1 = 'friend_request'
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
#事件名称  新文章
EVENT_ARTICAL = "Event_Artical"

#事件源 公众号
class PublicAccounts:
    def __init__(self,eventManager):
        self.__eventManager = eventManager

    def WriteNewArtical(self):
        #事件对象，写了新文章
        event = Event(type_=EVENT_ARTICAL)
        event.dict["artical"] = u'如何写出更优雅的代码\n'
        
        #发送事件
        self.__eventManager.SendEvent(event)
        print(u'公众号发送新文章\n')

#监听器 订阅者
class Listener:
    def __init__(self,username):
        self.__username = username

    #监听器的处理函数 读文章
    def ReadArtical(self,event):
        print(u'%s 收到新文章' % self.__username)
        print(u'正在阅读新文章内容：%s'  % event.dict["artical"])

#测试函数
#--------------------------------------------------------------------
def test():
    # 实例化监听器
    listner1 = Listener("thinkroom") #订阅者1
    listner2 = Listener("steve")     #订阅者2
    # 实例化事件操作函数
    eventManager = EventManager()

    #绑定事件和监听器响应函数(新文章)
    eventManager.AddEventListener(EVENT_ARTICAL, listner1.ReadArtical)
    eventManager.AddEventListener(EVENT_ARTICAL, listner2.ReadArtical)
    # 启动事件管理器,# 启动事件处理线程
    eventManager.Start()

    publicAcc = PublicAccounts(eventManager)
    timer = Timer(2, publicAcc.WriteNewArtical)
    timer.start()

if __name__ == '__main__':
    test()

"""

        
    
        
