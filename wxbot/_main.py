from bot_ import ProcessManager
from bot_.login import *
from bot_.EventManager import *

class mybot(KITBot):
    def __init__(self):
        #kitbot init
        super().__init__()
        
        pm = ProcessManager()
        ei_ = EventIdentifier()
        ep = EventProducer()
        #get group id by using group name
        target_group_name = []
        group_id_list = pm.get_groupID_byName(target_group_name,self.group_list)
    #override the handlemsg function which is donen every time by proc_msg, where r is the msg package
    def handle_msg(self,r):
        #handle msg func in superior class
        super().handle_msg(self,r)
        
        #seprate test msg from other msg
        t_msg, o_msg = pm.get_msg_art(r)

        #get event type
        event_type = []
        for msg in t_msg:
            #word detect
            detect_r = ei_.word_detect(msg['Content'])
            
            #get event type
            event_type.append(ei_.get_event_type(detect_r))
            #user misbehavior check

            #trigger event
            ep.trigger_event(event_type)


if __name__ == '__main__':
    bot = mybot()
    bot.auto_login()
        

