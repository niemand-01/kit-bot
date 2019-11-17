import time
import re
"""
    流程：1.上一层接口返回分析好的用户内容信息ip
         2.初始化一个数据类型
         3.将此数据加入一个数据库



          如果有用户需求这个数据，比如：
          1.请求数据通过serialnum
          2.请求最近帮带信息
          3.请求推荐帮带信息
          4.
"""
#########
zufang_bank = 0
ershou_bank = 1
bangdai_bank = 2 
jianzhi_bank = 3
#########
class EventData:
    DataType = ['zufang','ershou','bangdai','jianzhi']
    def __init__(self):
        #event type
        self.EventType = []
        #detail info:house/merchandise/product/nebenjob
        self.ObjectInfo = {}
        #user contact
        self.ContactInfo ={}
        #upload time
        self.ReleaseTime = ''
        #if he want to sell or want to buy
        self.is_producer = False
        #viewed time
        self.ViewNumber = ''
        #if product is sold or bought or...
        self.is_out = False
        #the serial number to locate
        self.SerialNumber = ''

    def isFinished(self):
        return self.is_out

class SecondHandData(EventData):
    product_info = {
            'product_name':'11',
            'product_price':'120',
            'product_size':'',
            'if_used':True,
            'used_time':'',
            'pick_art':'',
            'meet_place':'',
#            'available_datum':'',
            'rest_info':'',
            'if_with_pic':False,
            'pic_url':''
        }
    pick_art = ['ziqu','jiaojie','songda']
    contact_info = {
            'contact_type':'wexinhao',
            'contact_number':''
          }
    contact_type = ['wexinhao','phonenumber']
    def __init__(self,ip):
        if (ip['info_type'] in super().DataType):
            self.EventType =  ip['info_type']
        self.ObjectInfo = ip['info']
        self.ContactInfo = ip['contact_info']
        self.ReleaseTime = time.time()
        self.is_Producer = ip['is_producer']
        self.ViewNumber = 0
        self.is_out = False
        self.SerialNumber = '%s_%d'%(self.EventType,self.ReleaseTime)
    def checkInfo(self,info_dic):
        #check if input info concludes the required parameter
        print('start checking completeness')


class JobData(EventData):
    job_info = {
            'job':{
                'job_art':'',
                'work_loc':'',
                'salary_per_hour':'',
                'salary_per_month':'',
                'if_testperiode':True,
                'job_description':'',
                'company_description':'',
                'work_time_per_month':'',
                'start_time':'',
                'duration':'',
                'requirements':'',
            },
            'person':{
                'if_has_licence':False,
                'current_state':'',
#                'name':'',
#                'sex':'',
#                'age':'',
#                'legal_work':True,
                'experience':'',
                'skills':{},
                'flexibility':'',
                'available_period':'',
            },
            
            'rest_info':'',
            'if_with_pic':False,
            'pic_url':''
        }
    job_art = ['parttime','fulltime','praxis','thesis']
    current_state = ['student','graduate']
    contact_info = {
            'contact_type':'wexinhao',
            'contact_number':''
          }
    contact_type = ['wexinhao','phonenumber']
    def __init__(self,ip):
        if (ip['info_type'] in super().DataType):
            self.EventType =  ip['info_type']
        self.ObjectInfo = ip['info']
        self.ContactInfo = ip['contact_info']
        self.ReleaseTime = time.time()
        self.is_Producer = ip['is_producer']
        self.ViewNumber = 0
        self.is_out = False
        self.SerialNumber = '%s_%d'%(self.EventType,self.ReleaseTime)
    def checkInfo(self,info_dic):
        #check if input info concludes the required parameter
        print('start checking completality')


class HelpBringData(EventData):
    Bring_info = {
            'bring_date':'',
            'bring_routine':['place1','place2','place3'],
            'bring_item':'',
            'price_per_doc':'',
            'price_per_product':'',
            'exchange_way':'',
        'regulation':'不满1kg按1kg计算,中德两国有关法律允许的航空携带(托运)物品。不接受违禁品、粉末、液体,如果出现被海关罚款、没收、征收关税等特殊情况，物品主人自行承担罚款、关税。需提前告知所带物品',
            
            'product':{
                'product_name':'11',
#                'product_price':'120',
                'product_size':'',
                },
            'if_with_pic':False,
            'pic_url':''
        }
    bring_item = ['doc','product']
    exchange_way = ['face','post']
    contact_info = {
            'contact_type':'wexinhao',
            'contact_number':''
          }
    contact_type = ['wexinhao','phonenumber']
    def __init__(self,ip):
        if (ip['info_type'] in super().DataType):
            self.EventType =  ip['info_type']
        self.ObjectInfo = ip['info']
        self.ContactInfo = ip['contact_info']
        self.ReleaseTime = time.time()
        self.is_Producer = ip['is_producer']
        self.ViewNumber = 0
        self.is_out = False
        self.SerialNumber = '%s_%d'%(self.EventType,self.ReleaseTime)
    def checkInfo(self,info_dic):
        #check if input info concludes the required parameter
        print('start checking completality')


class HouseData(EventData):
    """
        ip = {'info_type':'zufang',
          'info':{
            'house_name':'11',
            'house_price_per_month':'120',
            'house_adr':'',
            'room_size':'',
            'room_art':''
            'min_to_campus':''
            'available_datum':'',
            'roommate_info':'',
            'furniture_info':'',
            'deposit':'',
            'nachfei':'',
            'shopping_info':'',
            'houseowner_info':'',
            'rest_info':'',
          },
          'contact_info':{
            'contact_type':'wexinhao',
            'contact_number':''
          },
          'is_producer':False,
          }
    """
    house_info = {
            'rent_art':'',
            'location':'',
            'price_per_month_warm':'120',
            'price_per_month_cold':'120',
            'nebenkosten':'',
            'nachfei':'',
            'deposit':'',
            'room_size':'',
            'min_to_campus':'',
            'start_date':'',
            'end_date':'',
            'furniture_info':'',
            'shopping_info':'',
            'roommate_info':'',
            'houseowner_info':'',
            'preferred_sex':'',
            'rest_info':'',
            'if_an':False,
            'if_with_pic':False,
            'pic_url':''
          }
    
    rente_art = ['zwischen','nach']
    contact_info = {
            'contact_type':'wexinhao',
            'contact_number':''
          }
    contact_type = ['wexinhao','phonenumber']
    def __init__(self,ip):
        if (ip['info_type'] in super().DataType):
            self.EventType =  ip['info_type']
        self.ObjectInfo = ip['info']
        self.ContactInfo = ip['contact_info']
        self.ReleaseTime = time.time()
        self.is_Producer = ip['is_producer']
        self.ViewNumber = 0
        self.is_out = False
        self.SerialNumber = '%s_%d'%(self.EventType,self.ReleaseTime)

    def checkInfo(self,info_dic):
        #check if input info concludes the required parameter
        print('start checking completality')


class InfoBank:
    #注意，加入infobank的不是单纯的dict而是类HouseData
    #dict访问是[]
    #类的访问是.
    DataType = ['zufang','ershou','bangdai','jianzhi']
    timeout = 1296000 #15days
    def __init__(self):
        self.zufang_bank = []
        self.ershou_bank = []
        self.bangdai_bank = []
        self.jianzhi_bank = []
        self.bank_sum = [self.zufang_bank,self.ershou_bank,self.bangdai_bank,self.jianzhi_bank]

    def add(self,data_stru):
        for idx in range(len(self.DataType)):
            if self.DataType[idx] == data_stru.EventType:
                self.bank_sum[idx].append(data_stru)

    # delete method
    def delete_with_serial(self,serial_,bank):
        for itm in self.bank_sum[bank]:
            if itm.SerialNumber == serial_:
                self.bank_sum[bank].remove(itm)
                
    def delete_if_out(self):
        #automatically search for the item with if_out
        for bank in self.bank_sum:
            for itm in bank:
                if itm.is_out:
                    bank.remove(itm)
                    
    def delete_with_timeout(self):
        #automatically search for the item with time eclapsed
        current_Time  = time.time() 
        for bank in self.bank_sum:
            for itm in bank:
                if current_Time - itm.ReleaseTime > timeout:
                    bank.remove(itm)

    
    #get method
    def get_latest_post(self,itm_num,bank):
        bk = self.bank_sum[bank]
        #既然是先后加的那么后加的一定最先
        return bk[len(bk)-itm_num:]

    def get_info_with_serial(self,serial_):
        #methodes:1.brainless loop 2.classify serial_ 3.jump with time difference
        match = re.match(r"(?P<art>\w+)_(?P<time>\w+)",serial_)
        bk_name = match.group('art')
        time = match.group('time')
        for idx in range(len(self.DataType)):
            if self.DataType[idx] == bk_name:
                for itm in DataType[idx]:
                    if itm.SerialNumber == serial_:
                        return itm.ObjectInfo
                


if __name__ == '__main__':
    t1 = 'bangdai_12233'
    print(re.match(r".+_(?P<time>\w+)",t1).group('time'))

    


    
    ip = {'info_type':'bangdai',
          'info':{
            'house_name':'11',
            'house_price_per_month':'120',
            'house_adr':'',
            'room_size':'',
            'room_art':'',
            'min_to_campus':'',
           'free_datum':'',
            'roommate_info':'',
            'furniture_info':'',
            'deposit':'',
            'nachfei':'',
            'shopping_info':'',
            'houseowner_info':'',
            'rest_info':'',
          },
          'contact_info':{
            'contact_type':'wexinhao',
            'contact_number':''
          },
          'is_producer':False,
          }

    house = HelpBringData(ip)
    print(house.SerialNumber)
