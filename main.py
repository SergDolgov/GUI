import json
import sys
from linkensphere_api import LinkenSphereApi
from mainwimdow import MainWindow
from PyQt6.QtWidgets import QApplication

from totalcontrol_api import TotalControlApi
from utils import find_by_key

linken_sphere_api  = None
total_control_api  = None


def get_license():   
    
    license_str = total_control_api.get_license()
    license_dict = json.loads(license_str)
    lic = license_dict["License"]
    desktop = license_dict["Desktop"]
    user = license_dict["Login"]
    password = license_dict["Password"]
    response = linken_sphere_api.signin(user=user, password=password)
    
    window.logger.info(f"signin: {response}")
   
    return lic, desktop

def set_active_desktop(name):
    
    linken_sphere_api.set_active_desktop(name=name)
    window.logger.info(f"set active desktop: {name}")
    
def get_settings(license):
    
    settings_str = total_control_api.get_settings(lic=license)
    settings_dict = json.loads(settings_str)
    provider = settings_dict["provider"]
    pipeline = settings_dict["pipeline"]
    connection = settings_dict["connection"]
    count = settings_dict["count"]

    window.logger.info(f"get_settings: {provider}")

    return provider, pipeline, connection, count
    
def set_active_provider(name):
    
    linken_sphere_api.set_active_provider(name=name)
    window.logger.info(f"set active provider: {name}")

def create_sessions(count, pipeline, connection):
    
    for i in range(count):
        session_str = linken_sphere_api.create_sessions()
        session = json.loads(session_str)[0]
        uuid = session["uuid"]
        name = session["name"]
        linken_sphere_api.set_connection(uuid=uuid, connection=connection)
        total_control_api.confirm_session(session=session, pipeline=pipeline) 
        window.logger.info(f"confirm_session: {name}")
        
def get_tasks(license):
    tasks_str = total_control_api.get_tasks(lic=license)
    tasks_dict = json.loads(tasks_str)
    cmd = tasks_dict["cmd"]

    window.logger.info(f"get_tasks: {cmd}")

    return cmd

def cleanup_sessions():
    
    response = linken_sphere_api.get_sessions()
    sessions = json.loads(response)

    payload = []
    
    for session in sessions:
        payload = {"uuid":session["uuid"]}
    
    response = total_control_api.clean_sessions(payload=payload) 
    clean_sessions = json.loads(response)
    
    for session in clean_sessions:
        
        clean_session = find_by_key(sessions, key="uuid", value=session["uuid"])
        
        if clean_session:
            if clean_session["status"] == "running":
                linken_sphere_api.stop_session(uuid=session["uuid"])  
                name = session["name"]
                window.logger.info(f"stoped_session: {name}")
            linken_sphere_api.delete_session(uuid=session["uuid"])  
            window.logger.info(f"deleted_session: {name}")
        
    
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    linken_sphere_api = LinkenSphereApi(window)    
    total_control_api = TotalControlApi(window)    
    
    window.linken_sphere_api = linken_sphere_api
    window.total_control_api = total_control_api
    
    license, desktop = get_license()
    set_active_desktop(name=desktop)

    provider, pipeline, connection, count = get_settings(license)
    set_active_provider(name=provider)
    
    # create_sessions
    # create_sessions(count=count, pipeline=pipeline, connection=connection)

    # get_tasks
    # tasks = get_tasks(license)
    
    # if tasks == "cleanup_sessions":
    #    cleanup_sessions() 

    # if tasks == "gen_sessions":
    #    create_sessions(count=count, pipeline=pipeline, connection=connection) 

    sys.exit(app.exec())
        