
import json
import requests

from utils import find_by_key

ls_url = "http://127.0.0.1:40080"

class LinkenSphereApi:
     
    def __init__(self, main_window):
        self.main_window = main_window
    
    def request(self, method, url_name, headers = {}, payload = {}, loggining = True):
        
        url = ls_url + url_name
        data = json.dumps(payload) if isinstance(payload, dict)|isinstance(payload, list) else payload
        response = requests.request(method, url, headers=headers, data=data)
        
        if loggining:
            self.main_window.logger.info(f"{method}, {url}, {response.text}")
        
        return response.text

    def signin(self, user, password):
        payload = {"email": user, "password": password, "autologin":True}
        return self.request("POST", "/auth/signin", payload=payload)

    def signout(self):
        return self.request("POST", "/auth/signout")

    def get_sessions(self):
        return self.request("GET", "/sessions")

    def create_sessions(self):
        return self.request("POST", "/sessions/create_quick")
        
    def set_connection(self, uuid, connection):
        payload = {
            "uuid": uuid, 
            "type": connection["type"], 
            "ip": connection["host"], 
            "port": connection["port"], 
            "login": connection["username"], 
            "password": connection["password"]
        }

        return self.request("POST", "/sessions/connection", payload=payload)
        
    def stop_session(self, uuid):
        payload = {"uuid": uuid}
        return self.request("POST", "/sessions/stop", payload=payload)
        
    def delete_session(self, uuid):
        payload = {"uuid": uuid}
        return self.request("POST", "/sessions/delete", payload=payload)
        
    def get_desktops(self):
        return self.request("GET", "/desktops")

    def create_desktops(self, payload):
        return self.request("POST", "/desktops", payload=payload)
        
    def get_desktop(self, key, value):
        desktops = self.request("GET", "/desktops")
        return find_by_key(desktops, key, value)

    def set_active_desktop(self, name):
        response = self.request("GET", "/desktops", loggining=False)
        desktops = json.loads(response)
        desktop = find_by_key(desktops, "name", name)

        if desktop is None:
            try:
                response = f"Desktop not found - {name}"
                self.main_window.logger.info(response)
                response = self.get_teams()
                teams = json.loads(response)[0]
                payload = {"name": name, "uuid": teams["uuid"]}
                self.create_desktops(payload)
            except Exception as e:
                self.main_window.logger.error(f"Error create desktop: {e}")
                
        payload = {"uuid": desktop["uuid"]}
        return self.request("POST", "/desktops", payload=payload)
        
    def get_providers(self):
        return self.request("GET", "/providers")

    def set_active_provider(self, name):
        response = self.request("GET", "/providers")
        providers = json.loads(response)
        provider = find_by_key(providers, "name", name)
        
        if provider is None:
           response = f"Provider not found - {name}"
           self.main_window.logger.info(response)
           return  response        

        payload = {"uuid": provider["uuid"]}
        return self.request("POST", "/providers", payload=payload)
   
    def get_teams(self):
        return self.request("GET", "/teams")




