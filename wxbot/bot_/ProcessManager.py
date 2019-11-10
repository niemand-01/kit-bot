class ProcessManager:
    def __init__(self,group_list):
        self.base = ['zufang','ershou','bangdai','jianzhi']
        self.MsgType = {
            'text':1,
            'image':3,
            'voice':34,
            'friend_request':37,
            'possible_friend_msg':40,
            'user_card':42,
            'video':43,
            'emoji':47,
            'loc':48,
            'share_link':49,
            'VOIPMSG':50,
            'wechat_init':51,
            'VOIPNOTIFY':52,
            'VOIPINVITE':53,
            'xiaoshiping':62,
            'SYSNOTICE':9999,
            'system_msg':10000,
            'recall_msg':10002
            }
        #群名：【卡鲁学联】租房信息1群
        #【卡鲁学联】二手信息1群，同里。。。
        #依次为zufang群的1-6群
        TARGET_GROUP={
            'zufang':[],
            'ershou':[],
            'bangdai':[],
            'jianzhi':[],
            }
        self.target_group = []

    def get_groupID_byName(self,name_list,group_list):
        local_gp_list = []
        gp_dict = {}
        for gp in group_list:
            for name in name_list:
                try:
                    if gp['NickName'].index(name) != -1:
                        gp_dict['group_name'] = gp['NickName']
                        gp_dict['group_id'] = gp['UserName']
                        local_gp_list.append(gp_dict)
                    if len(local_gp_list) == len(name_list):
                        break
                except:
                    pass
        self.target_group = local_gp_list
        return local_gp_list
    def get_target_groupID(self,group_list):
        for gp in group_list:
            for i in range(1,7):
                for idx,itm in enumerate(['租房','二手','帮带','兼职']):
                    info = str(itm) + '信息'+ str(i)
                    try:
                        if gp['NickName'].index(info) != -1:
                            print('find group %s index is %d'%(gp['NickName'],i))
                            print(gp['UserName'])
                            self.target_group[self.base[idx]].append(gp['UserName'])
                    except:
                        pass
    def get_msg_art(self,r):
        """
        return [], []
        """
        text_msg = []
        other_msg = []
        for msg in r['AddMsgList']:
            #loop all msg in one sync
            if msg['MsgType'] == 1:
                text_msg.append(msg)
            else:
                other_msg.append(msg)
                for name,value in self.MsgType.items():
                    if(msg['MsgType'] == value):
                        print('got msg type of %s'%name)
        return text_msg,other_msg
    def get_event(self,text_msg):
        event_list = []
        event = {}
        for msg in text_msg:
            content = msg['Content']
            key_d = self.keyword_detect(content)
            if key_d[2]:
                key_class = key_d[0]
                is_offer = True if key_d[1] == 0 else False
                #if no keyword detected then no need to get group id
                #get group name, group index: zufang 1

                #class name != null
                group_info =self.is_from_group(msg)
                if group_info[0]:
                    group_class = group_info[0]
                    #user penalty for send wrong type of message in group
                    if key_class != group_class:
                    #trigger user misbehavior event
                    #{eventid, userid}
                         break
                    else: 
    
                #save infomation with datastructure

                #return event type
                        """
                        for idx,value in enumerate(self.base):
                            if value == :
                                event_idx =(idx+1)*2
                                if is_offer:
                                    event_idx -= 2
                        event['type'] = group_class 
                        event['event'].append(EVENT_SHARE[event_idx])
                        event_list.append(event)
                        """

                

                   
            else:
                pass

        return event_list
    def is_from_user(self,msg):
        return 
    def is_from_group(self,msg):
        from_user_id = msg['FromUserName']
        to_user_id = msg['ToUserName']

    
        for name, group_id in self.target_group.items():
            if to_user_id in group_id:
                group_class = name
                group_idx = group_id.index(to_user_id)
                #potential target group id 
                p_tar_group = [_id for _id in group_id if _id != group_idx]

                

        return [group_class,group_idx,p_tar_group]
        
    def trigger_event(self,event):
        #eventmanager sendevent
        return       
                
            

    @staticmethod
    def run():
        #threading?
        while 1:
            #get msg from login.py
            r = get_msg()
            t_msg, o_msg = self.get_msg_art(r)
            if t_msg != []:
                event = self.get_event(t_msg)
                self.trigger_event(event)

"""
p = ProcessManager([{
    'UserName':'@@12312321',
    'NickName':'【卡鲁学联】租房信息1群'}])

i = [1,2,3,4]
newi = [_id for _id in i if _id !=3]
print(newi)
            
"""       

        
