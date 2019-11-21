#score the less the better
#demand-supply
tagMatrix = {
            'price':{
                'level':['0-100','100-200','200-300','300-400','400-500','500+'],
                #weight [0-1]
                'weight':0.5,
                #if the lower the better =>1 ,other wise 0
                'dir':-1
                },
            'roomsize':{
                'level':['0-10','10-15','15-20','20+'],
                'weight':0.5,
                #if the lower the better =>1 ,other wise 0
                'dir':1
                },
            'roomart':{
                'level':['wg','private'],
                'weight':2,
                #if the lower the better =>1 ,other wise 0
                'dir':1
                },
            'roomtype':{
                'level':['nach','zwischen'],
                'weight':2,
                #if the lower the better =>1 ,other wise 0
                'dir':1
                },
            'm2campus':{
                'level':['0-5','5-10','10-20','20+'],
                'weight':0.3,
                #if the lower the better =>1 ,other wise 0
                'dir':-1
                },
            'freedatum':{
                'level':['<2','2-5','5-10','10+'],
                'weight':2,
                #if the lower the better =>1 ,other wise 0
                'dir':-1
                },
            'roommate':{
                'level':['nice','normal','bad'],
                'weight':0.1,
                #if the lower the better =>1 ,other wise 0
                'dir':-1
                },
            'furniture':{
                'level':['full','half','empty'],
                'weight':0.4,
                #if the lower the better =>1 ,other wise 0
                'dir':-1
                },
            'deposite':{
                'level':['0','0-300','300-500','500+'],
                'weight':0.5,
                #if the lower the better =>1 ,other wise 0
                'dir':1
                },
            'nachfei':{
                'level':['0','0-300','300-500','500+'],
                'weight':0.5,
                #if the lower the better =>1 ,other wise 0
                'dir':-1
                },
            'if_an':{
                'level':['y','n'],
                'weight':2,
                #if the lower the better =>1 ,other wise 0
                'dir':-1
                },
            'is_out':{
                'level':['n','y'],
                'weight':10,
                #if the lower the better =>1 ,other wise 0
                'dir':-1
                }
            }

ip1 = {'info_type':'zufang',
          'info':{
            'house_name':'11',
            'house_price_per_month':250,
            'house_adr':'',
            'room_size':22,
            'room_art':'wg',
            'room_type':'nach',
            'min_to_campus':2,
            #free datum from today
            'free_datum':2,
            'roommate_info':'nice',
            'furniture_info':'full',
            'deposit':100,
            'nachfei':100,
            'shopping_info':'',
            'houseowner_info':'',
            'rest_info':'',
            'if_an':True,
            'if_with_pic':False,
            'pic_url':''
          },
          'contact_info':{
            'contact_type':'wexinhao',
            'contact_number':''
          },
          'is_producer':True,
          'release_time':'',
          'viewed_time':'',
          'is_out':False,
          'serial_num':'',
          }

ip2 = {'info_type':'zufang',
          'info':{
            'house_name':'11',
            'house_price_per_month':120,
            'house_adr':'',
            'room_size':16,
            'room_art':'wg',
            'room_type':'nach',
            'min_to_campus':8,
            #free datum from today
            'free_datum':5,
            'roommate_info':'nice',
            'furniture_info':'full',
            'deposit':380,
            'nachfei':100,
            'shopping_info':'',
            'houseowner_info':'',
            'rest_info':'',
            'if_an':True,
            'if_with_pic':False,
            'pic_url':''
          },
          'contact_info':{
            'contact_type':'wexinhao',
            'contact_number':''
          },
          'is_producer':True,
          'release_time':'',
          'viewed_time':'',
          'is_out':False,
          'serial_num':'',
          }

ip3 = {'info_type':'zufang',
          'info':{
            'house_name':'11',
            'house_price_per_month':500,
            'house_adr':'',
            'room_size':40,
            'room_art':'wg',
            'room_type':'nach',
            'min_to_campus':3,
            #free datum from today
            'free_datum':10,
            'roommate_info':'nice',
            'furniture_info':'full',
            'deposit':1000,
            'nachfei':0,
            'shopping_info':'',
            'houseowner_info':'',
            'rest_info':'',
            'if_an':True,
            'if_with_pic':False,
            'pic_url':''
          },
          'contact_info':{
            'contact_type':'wexinhao',
            'contact_number':''
          },
          'is_producer':True,
          'release_time':'',
          'viewed_time':'',
          'is_out':False,
          'serial_num':'',
          }

ip = {'info_type':'zufang',
          'info':{
            'house_name':'11',
            'house_price_per_month':120,
            'house_adr':'',
            'room_size':16,
            'room_art':'wg',
            'room_type':'nach',
            'min_to_campus':8,
            #free datum from today
            'free_datum':5,
            'roommate_info':'nice',
            'furniture_info':'full',
            'deposit':380,
            'nachfei':100,
            'shopping_info':'',
            'houseowner_info':'',
            'rest_info':'',
            'if_an':True,
            'if_with_pic':False,
            'pic_url':''
          },
          'contact_info':{
            'contact_type':'wexinhao',
            'contact_number':''
          },
          'is_producer':True,
          'release_time':'',
          'viewed_time':'',
          'is_out':False,
          'serial_num':'',
          }

ipbank = [ip1,ip2,ip3]
target_ip = ip

class Matcher:
    def __init__(self):
        print()
class HausMatcher(Matcher):
    def __init__(self):
        #a key in ip could be a tag to the house
        #in order to better classify the tag, we need to create a tag matrix to
        #store the different lvl of a tag
        #the key chosen to be a tag must have some characteristics which help
        #the object distinguish to others
        #each tag is also equipped with a weight
       
        matrix_bank = []
        for ip in ipbank:
            matrix_bank.append(self.get_matrix(ip))
        target_m = self.get_matrix(target_ip)
        
        res = self.evaluate(target_m,matrix_bank)
        
        for r in res:
            print(r)

    def get_matrix(self,ip):
        #anhand der Beispiel Hausdata
        _m ={
            'price':[ip['info']['house_price_per_month'],-1,0.5],
            'roomsize':[ip['info']['room_size'],1,0.5],
            'roomart':[ip['info']['room_art'],1,2],
            'roomtype':[ip['info']['room_type'],1,2],
            'm2campus':[ip['info']['min_to_campus'],-1,0.3],
            'freedatum':[ip['info']['free_datum'],-1,2],
            'roommate':[ip['info']['roommate_info'],-1,0.1],
            'furniture':[ip['info']['furniture_info'],-1,0.4],
            'deposite':[ip['info']['deposit'],1,0.5],
            'nachfei':[ip['info']['nachfei'],-1,0.5],
            'if_an':[ip['info']['if_an'],-1,2],
            'is_out':[ip['is_out'],-1,10]
            }

        #classify lvl
        tM1 = tagMatrix
        for key_,l_ in _m.items():
            if key_ == 'price':
                #second value of the array is 1vl
                p = [100,200,300,400,500]
                for i,v in enumerate(p):
                    if p[i] > _m[key_][0]:
                        _m[key_].append(i)
                        break
                if p[len(p)-1]<=_m[key_][0]:
                    _m[key_].append(5)
            if key_ == 'roomsize':
                p = [10,15,20]
                for i,v in enumerate(p):
                    if p[i] > _m[key_][0]:
                        _m[key_].append(i)
                        break
                if p[len(p)-1]<=_m[key_][0]:
                    _m[key_].append(3)

            if key_ == 'roomart':
                _m[key_].append(0 if _m[key_][0] == 'wg' else 1)

            if key_ == 'roomtype':
                _m[key_].append(0 if _m[key_][0] == 'nach' else 1)

            if key_ == 'm2campus':
                p = [5,10,20]
                for i,v in enumerate(p):
                    if p[i] > _m[key_][0]:
                        _m[key_].append(i)
                        break
                if p[len(p)-1]<=_m[key_][0]:
                    _m[key_].append(3)

            if key_ == 'freedatum':
                p = [2,5,10]
                for i,v in enumerate(p):
                    if p[i] > _m[key_][0]:
                        _m[key_].append(i)
                        break
                if p[len(p)-1]<=_m[key_][0]:
                    _m[key_].append(3)
            if key_ == 'roommate':
                p = ['nice','normal','bad']
                for i,v in enumerate(p):
                    if p[i] == _m[key_][0]:
                        _m[key_].append(i)
                        break
            if key_ == 'furniture':
                p = ['full','half','empty']
                for i,v in enumerate(p):
                    if p[i] == _m[key_][0]:
                        _m[key_].append(i)
                        break
            if key_ == 'deposite':
                p = [0,300,500]
                for i,v in enumerate(p):
                    if p[i] > _m[key_][0]:
                        _m[key_].append(i)
                        break
                if p[len(p)-1]<=_m[key_][0]:
                    _m[key_].append(3)
            if key_ == 'nachfei':
                p = [0,300,500]
                for i,v in enumerate(p):
                    if p[i] > _m[key_][0]:
                        _m[key_].append(i)
                        break
                if p[len(p)-1]<=_m[key_][0]:
                    _m[key_].append(3)
            if key_ == 'if_an':
                _m[key_].append(0 if _m[key_][0] == 'y' else 1)
            if key_ == 'is_out':
                _m[key_].append(0 if _m[key_][0] == 'n' else 1)
        #print(_m)
        return _m
    def evaluate(self,target_m,m_bank):
        #regulation:
        # s = sigma((target_tag - my_tag)*dir*weight)
        #sort list with the value s
        res_l = []
        s = 0
        for m in m_bank:
            for key_,l_ in m.items():
                s += m[key_][1]*(target_m[key_][3]-m[key_][3])*m[key_][2]
            _g = (m,s)
            res_l.append(_g)
        def second(val):
            return val[1]
        res_l.sort(key = second)
        return res_l
            

mm = HausMatcher()


        
        
