import requests
import json
from bs4 import BeautifulSoup

class AternosAPI():
    def __init__(self, headers, TOKEN):
        self.headers = {}
        self.TOKEN = TOKEN
        self.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
        self.headers['Cookie'] = headers
        self.JavaSoftwares = ['Vanilla', 'Spigot', 'Forge', 'Magma','Snapshot', 'Bukkit', 'Paper', 'Modpacks', 'Glowstone']
        self.BedrockSoftwares = ['Bedrock', 'Pocketmine-MP']
        
    def getSEC(self):
        headers = self.headers['Cookie'].split(";")
        for sec in headers:
            if sec[:12] == "ATERNOS_SEC_":
                sec = sec.split("_")
                if len(sec) == 3:
                    sec = ":".join(sec[2].split("="))
                    return sec

        print("Invaild SEC")
        exit(1)

    def GetStatus(self):
        server_info = self.GetServerInfo()
        return server_info['label']
    
    def QueuePos(self):
        server_info = self.GetServerInfo()
        position = server_info['queue']
        if position != None:
            position = position['position']
        return position
    
    def confirmQueue(self):
        position = self.QueuePos()
        if position != None:
            if position < 500:
                parameters = {}
                parameters['SEC'] = self.SEC
                parameters['TOKEN'] = self.TOKEN
                startserver = requests.get(url=f"https://aternos.org/panel/ajax/confirm.php", params=parameters, headers=self.headers)
                return True
        else:
            return False
    
    def StartServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Online":
            return False
        else:
            parameters = {}
            parameters['headstart'] = 0
            parameters['SEC'] = self.SEC
            parameters['TOKEN'] = self.TOKEN
            startserver = requests.get(url=f"https://aternos.org/panel/ajax/start.php", params=parameters, headers=self.headers)
            return True, self.QueuePos()

    def StopServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Offline":
            return False
        else:
            parameters = {}
            parameters['SEC'] = self.SEC
            parameters['TOKEN'] = self.TOKEN
            stopserver = requests.get(url=f"https://aternos.org/panel/ajax/stop.php", params=parameters, headers=self.headers)
            return True
    
    def RestartServer(self):
        parameters = {}
        parameters['SEC'] = self.SEC
        parameters['TOKEN'] = self.TOKEN
        restartserver = requests.get(url=f"https://aternos.org/panel/ajax/restart.php", params=parameters, headers=self.headers)
        return True
    
    def GetServerInfo(self):
        webserver = requests.get(url='https://aternos.org/server/', headers=self.headers)
        webdata = BeautifulSoup(webserver.content, 'html.parser')
        scripts = webdata.find_all('script')
        info = {}
        for script in scripts:
            if 'lastStatus' in str(script):
                info = json.loads(str(script).replace('\n','').replace('<script>        var lastStatus = ', '').replace(';    </script>', ''))
        return info

    def GetIP(self):
        server_info = self.GetServerInfo()
        return server_info['ip'], server_info['port'], server_info['dynip']
    
    def addWhitelist(self, name):
        parameters = {}
        parameters['SEC'] = self.SEC
        parameters['TOKEN'] = self.TOKEN
        data = {}
        data['list'] = 'whitelist'
        data['name'] = name
        adduser = requests.post(url=f"https://aternos.org/panel/ajax/restart.php", params=parameters, data=data, headers=self.headers)
        return True