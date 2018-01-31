import json
import os
import sys
import time
import sqlite3
from operator import itemgetter
from chatdb import *

            
def fun_load_json(file_name):
    
    with open(file_name) as json_data:
        d = json.load(json_data)
        json_data.close()
    return d       



def fun_check_new_content(dir_path,db_path,sleep_time):
        ls = os.listdir(dir_path)
        ms = []
        if ls != []:
            path = dir_path + '/' + ls[0]
            data = fun_load_json(path)
            os.remove(path)
            user_first_name = data["userInfo"][0]['firstname']
            user_last_name = data["userInfo"][0]['lastname']
            user_email = data["userInfo"][0]['emailaddress']
            user_password = data["userInfo"][0]['password']
            ms.append(user_first_name)
            ms.append(user_last_name)
            ms.append(user_email)
            ms.append(user_password)
            if fun_user_in_db(user_email,db_path) == 0:
                
                fun_insert_in_db(ms,db_path)
                print "signup_success"
            else:
                print "user already exist"
        
    
        else:
            return
        
            


if __name__ == "__main__":
    
    
    if len(sys.argv) != 2:
        print "invalid input"
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print "target directory not found"
        exit(0)

    list_d = fun_load_json(sys.argv[1])

    db_path = list_d["filewatcher"][0]['db_path']
    dir_path = list_d["filewatcher"][0]['dir_path']
    sleep_time = list_d["filewatcher"][0]['sleep_time']
    print db_path,dir_path,sleep_time
    fun_check_new_content(dir_path,db_path,sleep_time)
    








