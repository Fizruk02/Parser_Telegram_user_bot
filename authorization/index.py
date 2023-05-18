import requests
from pyrogram import Client
from bs4 import BeautifulSoup as BS

class Authorization:
    url = "https://my.telegram.org"

    def __init__(self, phone):
        self.session = requests.Session()
        self.phone = phone
        auth_to_code = self.session.get(url=self.url+"/auth/send_password", params={"phone": self.phone})
        self.hash = auth_to_code.text[16:-2]
        print(auth_to_code.text[16:-2])
        code = input("Enter the code: ")
        auth = self.session.post(url=self.url+"/auth/login", params={"phone": self.phone, "random_hash": self.hash, "password": code})

    def setProxy(self, type, ip, port, login, password):
        self.proxies = {'https': type+'://'+login+':'+password+'@'+ip+':'+str(port)}
        self.session.proxies.update(self.proxies)

    def getCreatorHash(self):
        params = {"hash": self.hash}
        apps = self.session.post(url=self.url+"/apps", params=params)
        html = BS(apps.content, "html.parser")
        input = html.select(".form-horizontal > input")
        hash_creator = input[0].get('value')
        return hash_creator

    def createApps(self, app_title, app_shortname, app_url, app_platform, app_desc):
        create = self.session.post(url=self.url+"/apps/create", params={"hash": self.getCreatorHash(), "app_title": app_title, "app_shortname": app_shortname, "app_url": app_url, "app_platform": app_platform, "app_desc": app_desc})
        print(create.text)
        if create.status_code != 200: return False
        return True

    def getApps(self):
        apps = self.session.post(url=self.url+"/apps", params={"hash": self.hash})
        html = BS(apps.content, 'html.parser')
        elements = html.select(".form-group > div > span")
        print(elements)
        if(len(elements)):
            api_key = elements[0].text
            api_hash = elements[1].text
            return {'api_key': api_key, 'api_hash': api_hash}
        elif(self.createApps("Honor 5G", "Honor 5G", "", "web", "")):
            return self.getApps()
        else:
            return False



#fake data
proxy = {"type": "socks5",
         "ip": "46.232.3.52",
         "port": 8000,
         "login": "ycjxxk",
         "password": "XVDYYQ"}

#fake data
phones = {"+6283840133226", "+6283840133230"}

for phone in phones:
    auth = Authorization(phone)
    #in development
    auth.setProxy(proxy['type'], proxy['ip'], proxy['port'], proxy['login'], proxy['password'])
    apps = auth.getApps()
    print({phone: apps})
#
#    for type in {"user", "parser"}:
#        with Client(name="../sessions/"+type+"/"apps['api_key'], api_id=apps['api_key'], api_hash=apps['api_hash'], proxy=dict(scheme=proxy['type'], hostname=proxy['ip'],port=proxy['port'], username=proxy['login'], password=proxy['password'])) as app:
#            app.send_message("me", "Message sent with **Pyrogram**!")