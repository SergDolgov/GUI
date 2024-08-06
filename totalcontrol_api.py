import json
import requests

ls_url = "https://totalcontrol.me/api_v2"

class TotalControlApi:
     
    def __init__(self, main_window):
        self.main_window = main_window
    
    def request(self, method, url_name, headers = {}, payload = {}, loggining = True):

        url = ls_url + url_name

        data = json.dumps(payload) if isinstance(payload, dict)|isinstance(payload, list) else payload
        response = requests.request(method, url, headers=headers, data=data)
        
        if loggining:
            self.main_window.logger.info(f"{method}, {url}, {response.text}")
        
        return response.text

    def get_license(self):
        return self.request("GET", "/get_lic.php")
        
    def get_settings(self, lic):
        return self.request("GET", f"/gen_config/super_gen_session.php?lic={lic}")
        
    def get_tasks(self, lic):
        return self.request("GET", f"/gen_config/supermain.php?lic={lic}")

    def confirm_session(self, session, pipeline):
        session["pipeline"] = pipeline
        payload = {"status": "successful", "data": session}
        
        return self.request("POST", f"/gen_config/super_gen_session.php?confirm=true", payload=payload)
        
    def clean_sessions(self, lic, payload):
        return self.request("POST", f"/gen_config/super_clean_session.php?lic={lic}", payload=payload)

        
        
