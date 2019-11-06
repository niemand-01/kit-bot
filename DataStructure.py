import time 

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
            'pick_art':'',
            'meet_place':'',
            'product_size':'',
            'if_used':True,
            'used_time':'',
            'available_datum':'',
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
        print('start checking completality')


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
            },
            'person':{
                'if_has_licence':False,
                'communicative_skill':{},
                'current_state':'',
                'name':'',
                'sex':'',
                'age':'',
                'legal_work':True,
                'experience':'',
                'flexibility':'',
                'available_datum':'',
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
                'product_price':'120',
                'pick_art':'',
                'meet_place':'',
                'product_size':'',
                'if_used':True,
                'used_time':'',
                'available_datum':'',
                'rest_info':'',
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
            'if_an':False,
            'if_with_pic':False,
            'pic_url':''
          }
    room_art = ['zwischen','nach']
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

if __name__ == '__main__':
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
