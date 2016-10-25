import requests, json, random

class WOT:
    def __init__(self):
        self.api_url = 'https://api.worldoftanks.ru/wot/account/info/'
        self.__jsondb = '' # wot.db
    def random_application_id(self):
        self.application_ids = ['APP_ID1','APP_ID2','APP_ID3','APP_ID4','APP_ID5']
        return self.application_ids[random.randint(0,len(self.application_ids)-1)]
    def db_init(self, key = 'r'):
        self.db = open(self.__jsondb, key)
    def db_close(self):
        self.db.close()
    def userinfo(self, account_id):
        return requests.post(self.api_url, data={'application_id':self.random_application_id(), 'account_id':account_id}).text
    def accounts_list(self, start_id, finish_id):
        return ','.join([str(x) for x in range(start_id, finish_id + 1)])
    def userparse(self, data, account_id):
        try:
            data = json.loads(data)['data']
            user_info = {x:{} for x in account_id.split(',')}
            for x in account_id.split(','):
                try: 
                    user_info[x]['battles'] = data[x]['statistics']['all']['battles']
                    user_info[x]['wins'] = data[x]['statistics']['all']['wins']
                    user_info[x]['global_rating'] = data[x]['global_rating']
                    user_info[x]['nickname'] = data[x]['nickname']
                except:
                    user_info[x]['battles'] = 0
                    user_info[x]['wins'] = 0
                    user_info[x]['global_rating'] = 0
                    user_info[x]['nickname'] = 0
        except:
            user_info = {x:{} for x in account_id.split(',')}
        return user_info
Wot = WOT()
i = 1
while i <= 10000:
    accounts = Wot.accounts_list(i,i+99)
    Wot.db_init()
    db = json.loads(Wot.db.read())
    Wot.db_close()
    db.update(Wot.userparse(Wot.userinfo(accounts),accounts))
    Wot.db_init('w+')
    Wot.db.write(json.dumps(db))
    Wot.db_close()
    i = i + 100
