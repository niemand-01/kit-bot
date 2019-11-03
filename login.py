import os
import sys
import traceback
import webbrowser
import pyqrcode
import requests
import mimetypes
import json
import xml.dom.minidom
import urllib
import time
import re
import random
from traceback import format_exc
from requests.exceptions import ConnectionError, ReadTimeout
import html

UNKONWN = 'unkonwn'
SUCCESS = '200'
SCANNED = '201'
TIMEOUT = '408'

#emoji

                    
def emoji_formatter(st):
    ''' _emoji_deebugger is for bugs about emoji match caused by wechat backstage
    like :face with tears of joy: will be replaced with :cat face with tears of joy:
    '''

    def _emoji_debugger(st):
        s = st.replace('<span class="emoji emoji1f450"></span',
            '<span class="emoji emoji1f450"></span>') # fix missing bug
        def __fix_miss_match(m):
            return '<span class="emoji emoji%s"></span>' % ({
                '1f63c': '1f601', '1f639': '1f602', '1f63a': '1f603',
                '1f4ab': '1f616', '1f64d': '1f614', '1f63b': '1f60d',
                '1f63d': '1f618', '1f64e': '1f621', '1f63f': '1f622',
                }.get(m.group(1), m.group(1)))
        return emojiRegex.sub(__fix_miss_match, s)
    def _emoji_formatter(m):
        s = m.group(1)
        if len(s) == 6:
            return ('\\U%s\\U%s'%(s[:2].rjust(8, '0'), s[2:].rjust(8, '0'))
                ).encode('utf8').decode('unicode-escape', 'replace')
        elif len(s) == 10:
            return ('\\U%s\\U%s'%(s[:5].rjust(8, '0'), s[5:].rjust(8, '0'))
                ).encode('utf8').decode('unicode-escape', 'replace')
        else:
            return ('\\U%s'%m.group(1).rjust(8, '0')
                ).encode('utf8').decode('unicode-escape', 'replace')
        
    emojiRegex = re.compile(r'<span class="emoji emoji(.{1,10})"></span>')
    if emojiRegex.search(st) != None:
        st = _emoji_debugger(st)
        st = emojiRegex.sub(_emoji_formatter, st)
        return st
    else:
        return st
        
#用于显示qrcode
def show_image(file_path):
    """
    跨平台显示图片文件
    :param file_path: 图片文件路径
    """
    #based on the version of python to decide include quote from which lib
    if sys.version_info >= (3, 3):
        from shlex import quote
    else:
        from pipes import quote

        
    #if its a linux darwin system
    if sys.platform == "darwin":
        command = "open -a /Applications/Preview.app %s&" % quote(file_path)
        os.system(command)
    #else open the pic in browser
    else:
        webbrowser.open(os.path.join(os.getcwd(),'temp',file_path))

        

#会话类 继承自requests.Session里面,调用request就是调用父类里面的request
class SafeSession(requests.Session):
    def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None,
                json=None):
        for i in range(3):
            try:
                return super(SafeSession, self).request(method, url, params, data, headers, cookies, files, auth,
                                                        timeout,
                                                        allow_redirects, proxies, hooks, stream, verify, cert, json)
            except Exception as e:
                #print(e.message, traceback.format_exc())
                continue

        #重试3次以后再加一次，抛出异常
        try:
            return super(SafeSession, self).request(method, url, params, data, headers, cookies, files, auth,
                                                    timeout,
                                                    allow_redirects, proxies, hooks, stream, verify, cert, json)
        except Exception as e:
            raise e

        

#自己的类
class KITBot:
    def __init__(self):
        self.session = SafeSession()
        self.uuid = ''
        self.conf = {'qr': 'png'}
        self.redirect_uri =''#redirect url
        self.base_uri=''
        self.base_host=''
        self.status=''
        self.base_request={}

        
        ###base_request elements basically userinfo
        self.uin=''
        self.sid=''
        self.skey=''
        self.device_id = 'e' + repr(random.random())[2:17]
        self.pass_ticket=''
        ###

        ###sync related attributes
        self.sync_key_str = ''
        self.sync_key = []
        self.sync_host = ''
        ###

        ###user related
        self.my_account =''
        ###

        ###debug
        self.DEBUG= False
        ###

        ###contact information related
        self.my_account = {}  # 当前账户
        # 所有相关账号: 联系人, 公众号, 群组, 特殊账号
        self.member_list = []
        # 所有群组的成员, {'group_id1': [member1, member2, ...], ...}
        self.group_members = {}
        # 所有账户, {'group_member':{'id':{'type':'group_member', 'info':{}}, ...}, 'normal_member':{'id':{}, ...}}
        self.account_info = {'group_member': {}, 'normal_member': {}}

        self.contact_list = []  # 联系人列表
        self.public_list = []  # 公众账号列表
        self.group_list = []  # 群聊列表
        self.special_list = []  # 特殊账号列表
        self.encry_chat_room_id_list = []  # 存储群聊的EncryChatRoomId，获取群内成员头像时需要用到
        ###
        

        #文件缓存目录 for saving qrcode or
        #getcwd:current working directory
        #os.path.join 用平台特定的连接符可能是/  连接两个string
        self.temp_dir  =  os.path.join(os.getcwd(),'temp')
        if os.path.exists(self.temp_dir) == False:
            os.makedirs(self.temp_dir)

    def getuuid(self):
        url = 'https://login.weixin.qq.com/jslogin'
        params = {
            'appid': 'wx782c26e4c19acffb',#定死的appid 猜测是网页版的id
            'redirect_url':'https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage',#新的redirect url参数
            'fun': 'new',
            'lang': 'zh_CN',#or en_US
            '_': int(time.time()) * 1000 + random.randint(1, 999),#greenwidh time in ms?
        }
        r = self.session.get(url, params=params)
        r.encoding = 'utf-8'
        data = r.text
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        pm = re.search(regx, data)
        if pm:
            code = pm.group(1)
            self.uuid = pm.group(2)
            return code == '200'#if code == 200 then getuuid ok!
        return False


    def init_sync(self):
        url = self.base_uri + '/webwxinit?r=%i&lang=en_US&pass_ticket=%s' % (int(time.time()), self.pass_ticket)
        params = {
            'BaseRequest': self.base_request
        }
        #json.dumps:make directory to json dorm
        r = self.session.post(url, data=json.dumps(params))
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        self.sync_key = dic['SyncKey']
        self.my_account = dic['User']
        self.sync_key_str = '|'.join([str(keyVal['Key']) + '_' + str(keyVal['Val']) for keyVal in self.sync_key['List']])
        return dic['BaseResponse']['Ret'] == 0
    
    #generate qrcode locally in qr_file_path/// qrcode is just a website!!
    def gen_qrcode(self,qr_file_path):
        string = 'https://login.weixin.qq.com/l/' + self.uuid #changed url!
        '''
        another method to get qrcode possibly generation exists online
        
        r = self.session.get('https://login.weixin.qq.com/qrcode/' + self.uuid, stream = True)
        with open('QRCode.jpg', 'wb') as f: f.write(r.content)
        '''
        qr = pyqrcode.create(string)
        #config code type of png
        if self.conf['qr'] == 'png':
            qr.png(qr_file_path, scale=8)
            show_image(qr_file_path)
            # img = Image.open(qr_file_path)
            # img.show()
        elif self.conf['qr'] == 'tty':
            #create an invalid qrcode
            print(qr.terminal(quiet_zone=1))

    def do_request(self, url,para):
        r = self.session.get(url,params = para)
        r.encoding = 'utf-8'
        data = r.text
        param = re.search(r'window.code=(\d+);', data)
        code = param.group(1)
        #print('before scanned',data)
        return code, data

    
    def check_scanning(self):
        """
        http comet:
        tip=1, 等待用户扫描二维码,
               201: scanned
               408: timeout
        tip=0, 等待用户确认登录,
               200: confirmed
        """
        LOGIN_TEMPLATE = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login'
        tip = 1#没有扫之前是1

        try_later_secs = 1
        MAX_RETRY_TIMES = 10
        code = UNKONWN
        retry_time = MAX_RETRY_TIMES

        #always in loop to look for scanning
        while retry_time > 0:

            #request for login status code
            para = 'tip=%s&uuid=%s&_=%s'%(tip, self.uuid, int(time.time()))
            code, data = self.do_request(LOGIN_TEMPLATE,para)

            
            if code == SCANNED:
                print('[INFO] Please confirm to login .')
                tip = 0#扫了以后是0
                
            elif code == SUCCESS:  # 确认登录成功
                #successfully login and then redirect to a new url
                param = re.search(r'window.redirect_uri="(\S+?)";', data)
                redirect_uri = param.group(1) + '&fun=new'
                self.redirect_uri = redirect_uri
                
                #rfind: from right to left check where is the last position of '/'
                self.base_uri = redirect_uri[:redirect_uri.rfind('/')]
                
                #print('base_uri',self.base_uri)

                #https:// has 8 letter
                temp_host = self.base_uri[8:]
                #print('temp host',temp_host)
                self.base_host = temp_host[:temp_host.find("/")]
                #print('base host',self.base_host)

                '''
            window.redirect_uri="https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A7rQhP8VnCOBuSlHMFI7ALfx@qrticket_0&uuid=IYvmbvNdDQ==&lang=zh_CN&scan=1571584486";
            base_uri https://wx2.qq.com/cgi-bin/mmwebwx-bin
            temp host wx2.qq.com/cgi-bin/mmwebwx-bin
            base host wx2.qq.com
                '''
                return code
            
            elif code == TIMEOUT:
                print('[ERROR] WeChat login timeout. retry in %s secs later...' % (try_later_secs,))

                tip = 1  # 重置
                retry_time -= 1
                time.sleep(try_later_secs)
            else:
                print ('[ERROR] WeChat login exception return_code=%s. retry in %s secs later...' %
                       (code, try_later_secs))
                tip = 1
                retry_time -= 1
                time.sleep(try_later_secs)

        return code

    def getUsrInfo(self):
        #get user info by examining the dom elemnents from the website catched
        
        if len(self.redirect_uri) < 4:
            print ('[ERROR] Login failed due to network problem, please try again.')
            return False
        r = self.session.get(self.redirect_uri)
        r.encoding = 'utf-8'
        data = r.text
        doc = xml.dom.minidom.parseString(data)
        root = doc.documentElement

        for node in root.childNodes:
            if node.nodeName == 'skey':
                self.skey = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                self.sid = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                self.uin = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                self.pass_ticket = node.childNodes[0].data

        if '' in (self.skey, self.sid, self.uin, self.pass_ticket):
            return False

        self.base_request = {
            'Uin': self.uin,
            'Sid': self.sid,
            'Skey': self.skey,
            'DeviceID': self.device_id,
        }
        return True


    #imitate the post request sequencely loaded by webwechat
    def status_notify(self):
        url = self.base_uri + '/webwxstatusnotify?lang=zh_CN&pass_ticket=%s' % self.pass_ticket
        self.base_request['Uin'] = int(self.base_request['Uin'])
        params = {
            'BaseRequest': self.base_request,
            "Code": 3,
            "FromUserName": self.my_account['UserName'],
            "ToUserName": self.my_account['UserName'],
            "ClientMsgId": int(time.time())
        }
        r = self.session.post(url, data=json.dumps(params))
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        #if send correctedly response will be 0
        return dic['BaseResponse']['Ret'] == 0

    #同样模拟网页请求，先get contact再 bachgetcontact
    def get_contact(self):
        """获取当前账户的所有相关账号(包括联系人、公众号、群聊、特殊账号)  全部在一个json返回包里面"""
        dic_list = []
        
        """base_uri https://wx2.qq.com/cgi-bin/mmwebwx-bin"""
        url = self.base_uri + '/webwxgetcontact?seq=0&pass_ticket=%s&skey=%s&r=%s' \
                              % (self.pass_ticket, self.skey, int(time.time()))

        #如果通讯录联系人过多，这里会直接获取失败
        try:
            r = self.session.post(url, data='{}', timeout=180)
        except Exception as e:
            return False
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        dic_list.append(dic)

        
        #Seq是列表最后元素=0，这里是联系人过多的情况，最后的seq!=0，那么就按依次的seq来post
        while int(dic["Seq"]) != 0:
            
            print ("[INFO] Geting contacts. Get %s contacts for now" % dic["MemberCount"])
            
            url = self.base_uri + '/webwxgetcontact?seq=%s&pass_ticket=%s&skey=%s&r=%s' \
                      % (dic["Seq"], self.pass_ticket, self.skey, int(time.time()))
            r = self.session.post(url, data='{}', timeout=180)
            r.encoding = 'utf-8'
            dic = json.loads(r.text)
            dic_list.append(dic)

        #如果是debug模式那么打印contact.json到文件夹
        if self.DEBUG:
            with open(os.path.join(self.temp_pwd,'contacts.json'), 'w') as f:
                f.write(json.dumps(dic_list))

        #成员组，如果这个contact是个群组就不为空，否则为空
        self.member_list = []
        #针对这里seq很多，导致dic很多的情况
        for dic in dic_list:
            #在尾部添加
            self.member_list.extend(dic['MemberList'])

        #特殊用户 比如微信公众平台，微信运动
        special_users = ['newsapp', 'fmessage', 'filehelper', 'weibo', 'qqmail',
                         'fmessage', 'tmessage', 'qmessage', 'qqsync', 'floatbottle',
                         'lbsapp', 'shakeapp', 'medianote', 'qqfriend', 'readerapp',
                         'blogapp', 'facebookapp', 'masssendapp', 'meishiapp',
                         'feedsapp', 'voip', 'blogappweixin', 'weixin', 'brandsessionholder',
                         'weixinreminder', 'wxid_novlwrv3lqwv11', 'gh_22b87fa7cb3c',
                         'officialaccounts', 'notification_messages', 'wxid_novlwrv3lqwv11',
                         'gh_22b87fa7cb3c', 'wxitil', 'userexperience_alarm', 'notification_messages']

        self.contact_list = []
        self.public_list = []
        self.special_list = []
        self.group_list = []

        #区分各个账号 并且归类，加入本地列表
        #这里进入account_info的都是独立个体，后面会解决群的事情
        for contact in self.member_list:
            if contact['VerifyFlag'] & 8 != 0:  # 公众号
                self.public_list.append(contact)
                self.account_info['normal_member'][contact['UserName']] = {'type': 'public', 'info': contact}
                
            elif contact['UserName'] in special_users:  # 特殊账户
                self.special_list.append(contact)
                self.account_info['normal_member'][contact['UserName']] = {'type': 'special', 'info': contact}
                
            elif contact['UserName'].find('@@') != -1:  # 群聊
                self.group_list.append(contact)
                self.account_info['normal_member'][contact['UserName']] = {'type': 'group', 'info': contact}
                
            elif contact['UserName'] == self.my_account['UserName']:  # 自己
                self.account_info['normal_member'][contact['UserName']] = {'type': 'self', 'info': contact}
                
            else:
                self.contact_list.append(contact)#朋友
                self.account_info['normal_member'][contact['UserName']] = {'type': 'contact', 'info': contact}

        print(self.group_list)
        #获取群的所有成员信息
        self.batch_get_group_members()

        for group in self.group_members:
            for member in self.group_members[group]:
                if member['UserName'] not in self.account_info:
                    self.account_info['group_member'][member['UserName']] = \
                        {'type': 'group_member', 'info': member, 'group': group}

        #记录debug
        if self.DEBUG:
            with open(os.path.join(self.temp_pwd,'contact_list.json'), 'w') as f:
                f.write(json.dumps(self.contact_list))
            with open(os.path.join(self.temp_pwd,'special_list.json'), 'w') as f:
                f.write(json.dumps(self.special_list))
            with open(os.path.join(self.temp_pwd,'group_list.json'), 'w') as f:
                f.write(json.dumps(self.group_list))
            with open(os.path.join(self.temp_pwd,'public_list.json'), 'w') as f:
                f.write(json.dumps(self.public_list))
            with open(os.path.join(self.temp_pwd,'member_list.json'), 'w') as f:
                f.write(json.dumps(self.member_list))
            with open(os.path.join(self.temp_pwd,'group_users.json'), 'w') as f:
                f.write(json.dumps(self.group_members))
            with open(os.path.join(self.temp_pwd,'account_info.json'), 'w') as f:
                f.write(json.dumps(self.account_info))
        return True

    def batch_get_group_members(self):
        """批量获取所有群聊成员信息"""
        url = self.base_uri + '/webwxbatchgetcontact?type=ex&r=%s&pass_ticket=%s' % (int(time.time()), self.pass_ticket)
        params = {
            'BaseRequest': self.base_request,
            "Count": len(self.group_list),
            "List": [{"UserName": group['UserName'], "EncryChatRoomId": ""} for group in self.group_list]
        }
        r = self.session.post(url, data=json.dumps(params))
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        group_members = {}
        encry_chat_room_id = {}
        for group in dic['ContactList']:
            gid = group['UserName']
            members = group['MemberList']
            group_members[gid] = members
            encry_chat_room_id[gid] = group['EncryChatRoomId']
        self.group_members = group_members
        self.encry_chat_room_id_list = encry_chat_room_id




    def test_sync_check(self):
        #要看那个才是synccheck的借口push还是push2
        for host1 in ['webpush.', 'webpush2.']:
            self.sync_host = host1+self.base_host
            try:
                retcode = self.sync_check()[0]
            except:
                retcode = -1
            if retcode == '0':
                return True
        return False
    def sync_check(self):
        params = {
            'r': int(time.time()),
            'sid': self.sid,
            'uin': self.uin,
            'skey': self.skey,
            'deviceid': self.device_id,
            'synckey': self.sync_key_str,
            '_': int(time.time()),
        }
        url = 'https://' + self.sync_host + '/cgi-bin/mmwebwx-bin/synccheck?' + urllib.parse.urlencode(params)
        try:
            r = self.session.get(url, timeout=60)
            r.encoding = 'utf-8'
            data = r.text
            pm = re.search(r'window.synccheck=\{retcode:"(\d+)",selector:"(\d+)"\}', data)
            retcode = pm.group(1)
            selector = pm.group(2)
            return [retcode, selector]
        except:
            return [-1, -1]
    def sync(self):
        url = self.base_uri + '/webwxsync?sid=%s&skey=%s&lang=en_US&pass_ticket=%s' \
                              % (self.sid, self.skey, self.pass_ticket)
        params = {
            'BaseRequest': self.base_request,
            'SyncKey': self.sync_key,
            'rr': ~int(time.time())
        }
        try:
            r = self.session.post(url, data=json.dumps(params), timeout=60)
            r.encoding = 'utf-8'
            dic = json.loads(r.text)
            if dic['BaseResponse']['Ret'] == 0:
                self.sync_key = dic['SyncCheckKey']
                self.sync_key_str = '|'.join([str(keyVal['Key']) + '_' + str(keyVal['Val'])
                                              for keyVal in self.sync_key['List']])
            return dic
        except:
            return None


    def addgroupListener(self,r):
        """
        r:wechat return msg
        
        """
        for msg in r['AddMsgList']:
            #group
            if msg['FromUserName'][:2]== '@@':
                g_name = ''
                for gp in self.group_list:
                    if gp['UserName'] == msg['FromUserName']:
                        g_name = gp['NickName']
                if g_name != '':
                    content = msg['Content']
                    content = emoji_formatter(content)
                    text = content[content.rfind('<br/>')+5:]
                    userid = content[:content.rfind(':<br/>')]
                    print('李泽凯id:',userid)
                    for memb in self.group_members[msg['FromUserName']]:
                        if memb['UserName'] == userid:
                            u_name = memb['NickName']
                    content = '来自群聊%s的%s给你发来的消息:%s'%(g_name,u_name,text)

                    #@9cef97ff87f96b39ed5ea4c5a888926fe960f5368528f6dade37d0fdb679b8ee:<br/>hello
                    for fr in self.contact_list:
                        if fr['NickName'].find('李泽凯')!=-1:
                            f_id = fr['UserName']
                    self.send_msg_by_uid(content,f_id)
                    self.send_msg_by_uid(content,'filehelper')
                    

    def check_groupid(self,id_,name):
        for group in self.group_list:
            if group['NickName'].find('张杰超')!=-1:
                if group['UserName'] == id_:
                    return true
        return false
    def get_groupid_by_name(self,name):
        for group in self.group_list:
            if group['NickName'].find(name)!=-1:
                return group['UserName']
    def handle_msg(self,r):
        """
        处理原始微信消息的内部函数
        msg_type_id:
            0 -> Init
            1 -> Self
            2 -> FileHelper
            3 -> Group
            4 -> Contact
            5 -> Public
            6 -> Special
            99 -> Unknown
        :param r: 原始微信消息
        """
        self.addgroupListener(r)
        for msg in r['AddMsgList']:
            user = {'id': msg['FromUserName'], 'name': 'unknown'}
            """
            if msg['MsgType'] == 51 and msg['StatusNotifyCode'] == 4:  # init message
                msg_type_id = 0
                user['name'] = 'system'
                #会获取所有联系人的username 和 wxid，但是会收到3次这个消息，只取第一次
                if self.is_big_contact and len(self.full_user_name_list) == 0:
                    self.full_user_name_list = msg['StatusNotifyUserName'].split(",")
                    self.wxid_list = re.search(r"username&gt;(.*?)&lt;/username", msg["Content"]).group(1).split(",")
                    with open(os.path.join(self.temp_pwd,'UserName.txt'), 'w') as f:
                        f.write(msg['StatusNotifyUserName'])
                    with open(os.path.join(self.temp_pwd,'wxid.txt'), 'w') as f:
                        f.write(json.dumps(self.wxid_list))
                    #print "[INFO] Contact list is too big. Now start to fetch member list ."
                    #self.get_big_contact()
            """
            if msg['MsgType'] == 37:  # friend request
                msg_type_id = 37
                pass
                # content = msg['Content']
                # username = content[content.index('fromusername='): content.index('encryptusername')]
                # username = username[username.index('"') + 1: username.rindex('"')]
                # #print u'[Friend Request]'
                # #print u'       Nickname：' + msg['RecommendInfo']['NickName']
                # #print u'       附加消息：'+msg['RecommendInfo']['Content']
                # # #print u'Ticket：'+msg['RecommendInfo']['Ticket'] # Ticket添加好友时要用
                # #print u'       微信号：'+username #未设置微信号的 腾讯会自动生成一段微信ID 但是无法通过搜索 搜索到此人
            elif msg['FromUserName'] == self.my_account['UserName']:  # Self
                msg_type_id = 1
                user['name'] = 'self'
            elif msg['ToUserName'] == 'filehelper':  # File Helper
                msg_type_id = 2
                user['name'] = 'file_helper'
            elif msg['FromUserName'][:2] == '@@':  # Group
                msg_type_id = 3
                user['name'] = self.get_contact_prefer_name(self.get_contact_name(user['id']))
            elif self.is_contact(msg['FromUserName']):  # Contact
                msg_type_id = 4
                user['name'] = self.get_contact_prefer_name(self.get_contact_name(user['id']))
            elif self.is_public(msg['FromUserName']):  # Public
                msg_type_id = 5
                user['name'] = self.get_contact_prefer_name(self.get_contact_name(user['id']))
            elif self.is_special(msg['FromUserName']):  # Special
                msg_type_id = 6
                user['name'] = self.get_contact_prefer_name(self.get_contact_name(user['id']))
            else:
                msg_type_id = 99
                user['name'] = 'unknown'
            if not user['name']:
                user['name'] = 'unknown'
            user['name'] = html.unescape(user['name'])

            if self.DEBUG and msg_type_id != 0:
                print( u'[MSG] %s:' % user['name'])
            content = self.extract_msg_content(msg_type_id, msg)
            message = {'msg_type_id': msg_type_id,
                       'msg_id': msg['MsgId'],
                       'content': content,
                       'to_user_id': msg['ToUserName'],
                       'user': user}
            print(message)

    #三个name 里面有哪个就返回哪个
    @staticmethod
    def get_contact_prefer_name(name):
        if name is None:
            return None
        if 'remark_name' in name:
            return name['remark_name']
        if 'nickname' in name:
            return name['nickname']
        if 'display_name' in name:
            return name['display_name']
        return None

    #把三个name全部装入name
    def get_contact_name(self, uid):
        info = self.get_contact_info(uid)
        if info is None:
            return None
        info = info['info']
        name = {}
        if 'RemarkName' in info and info['RemarkName']:
            name['remark_name'] = info['RemarkName']
        if 'NickName' in info and info['NickName']:
            name['nickname'] = info['NickName']
        if 'DisplayName' in info and info['DisplayName']:
            name['display_name'] = info['DisplayName']
        if len(name) == 0:
            return None
        else:
            return name
        
    def get_contact_info(self, uid):
        return self.account_info['normal_member'].get(uid)
    
    def extract_msg_content(self, msg_type_id, msg):
        """
        content_type_id:
            0 -> Text
            1 -> Location
            3 -> Image
            4 -> Voice
            5 -> Recommend
            6 -> Animation
            7 -> Share
            8 -> Video
            9 -> VideoCall
            10 -> Redraw
            11 -> Empty
            99 -> Unknown
        :param msg_type_id: 消息类型id
        :param msg: 消息结构体
        :return: 解析的消息
        """
        mtype = msg['MsgType']
        #使用html转义content里面的内容
        content = html.unescape(msg['Content'])
        msg_id = msg['MsgId']

        msg_content = {}
        if msg_type_id == 0:#init
            return {'type': 11, 'data': ''}
        elif msg_type_id == 2:  # File Helper
            return {'type': 0, 'data': content.replace('<br/>', '\n')}
        else:  # Self, Contact, Special, Public, Unknown
            pass
        """
        elif msg_type_id == 3:  # 群聊
            sp = content.find('<br/>')
            uid = content[:sp]
            content = content[sp:]
            content = content.replace('<br/>', '')
            uid = uid[:-1]
            name = self.get_contact_prefer_name(self.get_contact_name(uid))
            if not name:
                name = self.get_group_member_prefer_name(self.get_group_member_name(msg['FromUserName'], uid))
            if not name:
                name = 'unknown'
            msg_content['user'] = {'id': uid, 'name': name}
            """


        msg_prefix = (msg_content['user']['name'] + ':') if 'user' in msg_content else ''


        """
        content_type_id:
MsgType	说明
1	文本消息
3	图片消息
34	语音消息
37	好友确认消息
40	POSSIBLEFRIEND_MSG
42	共享名片
43	视频消息
47	动画表情
48	位置消息
49	分享链接
50	VOIPMSG
51	微信初始化消息
52	VOIPNOTIFY
53	VOIPINVITE
62	小视频
9999	SYSNOTICE
10000	系统消息
10002	撤回消息
        :param msg_type_id: 消息类型id
        :param msg: 消息结构体
        :return: 解析的消息 msg_content
        """
        
        if mtype == 1:
            #if content includes following string
            if content.find('http://weixin.qq.com/cgi-bin/redirectforward?args=') != -1:
                r = self.session.get(content)
                r.encoding = 'gbk'
                data = r.text
                pos = self.search_content('title', data, 'xml')
                msg_content['type'] = 1
                msg_content['data'] = pos
                msg_content['detail'] = data
                if self.DEBUG:
                    print ( '%s[Location] %s ' % (msg_prefix, pos))
            else:
                msg_content['type'] = 0
                if msg_type_id == 3 or (msg_type_id == 1 and msg['ToUserName'][:2] == '@@'):  # Group text message
                    msg_infos = self.proc_at_info(content)
                    str_msg_all = msg_infos[0]
                    str_msg = msg_infos[1]
                    detail = msg_infos[2]
                    msg_content['data'] = str_msg_all
                    msg_content['detail'] = detail
                    msg_content['desc'] = str_msg
                else:
                    msg_content['data'] = content
                if self.DEBUG:
                    try:
                        print('tt')
                        #print '    %s[Text] %s' % (msg_prefix, msg_content['data'])
                    except UnicodeEncodeError:
                        print('tt')
                        #print '    %s[Text] (illegal text).' % msg_prefix
        elif mtype == 3:
            msg_content['type'] = 3
            msg_content['data'] = self.get_msg_img_url(msg_id)
            msg_content['img'] = self.session.get(msg_content['data']).content.encode('hex')
            if self.DEBUG:
                image = self.get_msg_img(msg_id)
                #print '    %s[Image] %s' % (msg_prefix, image)
        elif mtype == 34:
            msg_content['type'] = 4
            msg_content['data'] = self.get_voice_url(msg_id)
            msg_content['voice'] = self.session.get(msg_content['data']).content.encode('hex')
            if self.DEBUG:
                voice = self.get_voice(msg_id)
                #print '    %s[Voice] %s' % (msg_prefix, voice)
        elif mtype == 37:
            msg_content['type'] = 37
            msg_content['data'] = msg['RecommendInfo']
            if self.DEBUG:
                print('tt')
                #print '    %s[useradd] %s' % (msg_prefix,msg['RecommendInfo']['NickName'])
        elif mtype == 42:
            msg_content['type'] = 5
            info = msg['RecommendInfo']
            msg_content['data'] = {'nickname': info['NickName'],
                                   'alias': info['Alias'],
                                   'province': info['Province'],
                                   'city': info['City'],
                                   'gender': ['unknown', 'male', 'female'][info['Sex']]}
            if self.DEBUG:
                print('tt')
                #print '    %s[Recommend]' % msg_prefix
                #print '    -----------------------------'
                #print '    | NickName: %s' % info['NickName']
                #print '    | Alias: %s' % info['Alias']
                #print '    | Local: %s %s' % (info['Province'], info['City'])
                #print '    | Gender: %s' % ['unknown', 'male', 'female'][info['Sex']]
                #print '    -----------------------------'
        elif mtype == 47:
            msg_content['type'] = 6
            msg_content['data'] = self.search_content('cdnurl', content)
            if self.DEBUG:
                print( '    %s[Animation] %s' % (msg_prefix, msg_content['data']))
        elif mtype == 49:
            msg_content['type'] = 7
            if msg['AppMsgType'] == 3:
                app_msg_type = 'music'
            elif msg['AppMsgType'] == 5:
                app_msg_type = 'link'
            elif msg['AppMsgType'] == 7:
                app_msg_type = 'weibo'
            else:
                app_msg_type = 'unknown'
            msg_content['data'] = {'type': app_msg_type,
                                   'title': msg['FileName'],
                                   'desc': self.search_content('des', content, 'xml'),
                                   'url': msg['Url'],
                                   'from': self.search_content('appname', content, 'xml'),
                                   'content': msg.get('Content')  # 有的公众号会发一次性3 4条链接一个大图,如果只url那只能获取第一条,content里面有所有的链接
                                   }
            if self.DEBUG:
                print ('    %s[Share] %s' % (msg_prefix, app_msg_type))
                #print '    --------------------------'
                #print '    | title: %s' % msg['FileName']
                #print '    | desc: %s' % self.search_content('des', content, 'xml')
                #print '    | link: %s' % msg['Url']
                #print '    | from: %s' % self.search_content('appname', content, 'xml')
                #print '    | content: %s' % (msg.get('content')[:20] if msg.get('content') else "unknown")
                #print '    --------------------------'

        elif mtype == 62:
            msg_content['type'] = 8
            msg_content['data'] = content
            if self.DEBUG:
                print('tt')
                #print '    %s[Video] Please check on mobiles' % msg_prefix
        elif mtype == 53:
            msg_content['type'] = 9
            msg_content['data'] = content
            if self.DEBUG:
                print('tt')
                #print '    %s[Video Call]' % msg_prefix
        elif mtype == 10002:
            msg_content['type'] = 10
            msg_content['data'] = content
            if self.DEBUG:
                print('tt')
                #print '    %s[Redraw]' % msg_prefix
        elif mtype == 10000:  # unknown, maybe red packet, or group invite
            msg_content['type'] = 12
            msg_content['data'] = msg['Content']
            if self.DEBUG:
                print('tt')
                #print '    [Unknown]'
        elif mtype == 43:
            msg_content['type'] = 13
            msg_content['data'] = self.get_video_url(msg_id)
            if self.DEBUG:
                print('tt')
                #print(.*)
        else:
            msg_content['type'] = 99
            msg_content['data'] = content
            if self.DEBUG:
                print('tt')
                #print '    %s[Unknown]' % msg_prefix
        return msg_content

    @staticmethod
    def proc_at_info(msg):
        if not msg:
            return '', []
        segs = msg.split(u'\u2005')
        str_msg_all = ''
        str_msg = ''
        infos = []
        if len(segs) > 1:
            for i in range(0, len(segs) - 1):
                segs[i] += u'\u2005'
                pm = re.search(u'@.*\u2005', segs[i]).group()
                if pm:
                    name = pm[1:-1]
                    string = segs[i].replace(pm, '')
                    str_msg_all += string + '@' + name + ' '
                    str_msg += string
                    if string:
                        infos.append({'type': 'str', 'value': string})
                    infos.append({'type': 'at', 'value': name})
                else:
                    infos.append({'type': 'str', 'value': segs[i]})
                    str_msg_all += segs[i]
                    str_msg += segs[i]
            str_msg_all += segs[-1]
            str_msg += segs[-1]
            infos.append({'type': 'str', 'value': segs[-1]})
        else:
            infos.append({'type': 'str', 'value': segs[-1]})
            str_msg_all = msg
            str_msg = msg
        return str_msg_all.replace(u'\u2005', ''), str_msg.replace(u'\u2005', ''), infos




    def is_contact(self, uid):
        for account in self.contact_list:
            if uid == account['UserName']:
                return True
        return False

    def is_public(self, uid):
        for account in self.public_list:
            if uid == account['UserName']:
                return True
        return False

    def is_special(self, uid):
        for account in self.special_list:
            if uid == account['UserName']:
                return True
        return False
    
    def proc_msg(self):
        #keep synchronisation through checking out on the retcode
        self.test_sync_check()
        self.status = 'loginsuccess'  #WxbotManage使用
        while True:
            if self.status == 'wait4loginout':  #WxbotManage使用
                return 
            check_time = time.time()
            try:
                [retcode, selector] = self.sync_check()
                # #print '[DEBUG] sync_check:', retcode, selector
                if retcode == '1100':  # 从微信客户端上登出
                    break
                elif retcode == '1101':  # 从其它设备上登了网页微信
                    break
                elif retcode == '0':
                    if selector == '2':  # 有新消息
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    elif selector == '3':  # 未知
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    elif selector == '4':  # 通讯录更新
                        r = self.sync()
                        if r is not None:
                            self.get_contact()
                    elif selector == '6':  # 可能是红包
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    elif selector == '7':  # 在手机上操作了微信
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    elif selector == '0':  # 无事件
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    else:
                        #print '[DEBUG] sync_check:', retcode, selector
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                else:
                    print('[DEBUG] sync_check:', retcode, selector)
                    time.sleep(10)
                #self.schedule()
            except Exception as e:
                print ('[ERROR] Except in proc_msg: '%e)
                #print format_exc()
            check_time = time.time() - check_time
            if check_time < 0.8:
                time.sleep(1 - check_time)
                




    '''send text to someone'''
    def get_user_id(self, name):
        if name == '':
            return None
        #name = self.to_unicode(name)
        for contact in self.contact_list:
            #如果contact里面有remarkname元素
            if 'RemarkName' in contact and re.match(r'(.*)'+name+'.*',contact['RemarkName']):
                return contact['UserName']
            elif 'NickName' in contact and re.match(r'(.*)'+name+'.*',contact['NickName']):
                return contact['UserName']
            elif 'DisplayName' in contact and re.match(r'(.*)'+name+'.*',contact['DisplayName']):
                return contact['UserName']
        for group in self.group_list:
            if 'RemarkName' in group and group['RemarkName'] == name:
                return group['UserName']
            if 'NickName' in group and group['NickName'] == name:
                return group['UserName']
            if 'DisplayName' in group and group['DisplayName'] == name:
                return group['UserName']

        return ''
    #wcccy account changed evry time need dynamically set
    def send_msg_by_uid(self, word, dst='FileHelper'):
        url = self.base_uri + '/webwxsendmsg?pass_ticket=%s' % self.pass_ticket
        msg_id = str(int(time.time() * 1000)) + str(random.random())[:5].replace('.', '')
        #word = word.encode('utf-8') if isinstance(word,str) else word
        params = {
            'BaseRequest': self.base_request,
            'Msg': {
                "Type": 1,
                "Content": word,
                "FromUserName": self.my_account['UserName'],
                "ToUserName": dst,
                "LocalID": msg_id,
                "ClientMsgId": msg_id
            }
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(params, ensure_ascii=False).encode('utf8')
        try:
            r = self.session.post(url, data=data, headers=headers)
        except (ConnectionError, ReadTimeout):
            return False
        dic = r.json()
        print(dic)
        return dic['BaseResponse']['Ret'] == 0
    
    def send_msg(self, name, word, isfile=False):
        uid = self.get_user_id(name)
        if uid is not None:
            if isfile:
                with open(word, 'r') as f:
                    result = True
                    for line in f.readlines():
                        line = line.replace('\n', '')
                        #print '-> ' + name + ': ' + line
                        if self.send_msg_by_uid(line, uid):
                            pass
                        else:
                            result = False
                        time.sleep(1)
                    return result
            else:
                word = self.to_unicode(word)
                if self.send_msg_by_uid(word, uid):
                    return True
                else:
                    return False
        else:
            if self.DEBUG:
                print ('[ERROR] This user does not exist .')
            return True
        
    def auto_login(self):
        try:
            #get uuid
            self.getuuid()
            #generate qrcode
            self.gen_qrcode(os.path.join(self.temp_dir,'wxqr.png'))
            print('[INFO] Please use WeChat to scan the QR code .')

            #check scanning
            return_code = self.check_scanning()
            if return_code != SUCCESS:
                print('ERROR:wx login falled error code:%s'%(return_code))
                self.status = 'logout'
                return
            #get uid key...userinfo
            if self.getUsrInfo():
                print('wx successfully login')
            else:
                self.status = 'logout'
                return
            #use the gotten userinfo to initailze syncronisation(get syncro-key)
            if self.init_sync():
                print('wx successfully iniated sync')
            else:
                self.status = 'logout'
                return

            self.status_notify()
            if self.get_contact():
                print ('[INFO] Get %d contacts' % len(self.contact_list))
                print ('[INFO] Start to process messages .')
            self.proc_msg()
            #out of loop
            self.status = 'loginout'
        except Exception as e:
            print('ERROR:error code'%e)
        
            


if __name__ == '__main__':
    bot = KITBot()
    bot.auto_login()
    
