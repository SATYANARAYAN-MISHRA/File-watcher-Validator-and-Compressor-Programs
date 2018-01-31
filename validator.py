import sys
import os
import time
import sqlite3
import json
from operator import itemgetter

def fun_load_json_file(input_data_file):
    with open(input_data_file) as json_data:
        data = json.load(json_data)
        json_data.close()
    return data

def fun_validate_phone(phone):
    len_phone_no = len(phone['number'])
    if phone['type'] == 'home' or phone['type'] == 'office':
#        print "hey ",phone['type'],phone['number']
        if len_phone_no != 12:
            print "len"
            return False
        for i in range(0,len_phone_no):
            if i == 3 and phone['number'][i] != '-':
                print "lalu"
                return False
            elif i !=3 and not (phone['number'][i]).isdigit():
                print "elif"
                return False
        return True
    if phone['type'] == 'mobile':
#        print "hello mobile",phone['number']
        if len_phone_no != 10:
            return False
        for i in range(0,len_phone_no):
            if not (phone['number'][i]).isdigit():
                return False
        return True
                
                
def fun_validate_json_file(data):

    d = json.loads(data)
    len_data = len(d['persons'])
    phone_dir = []
    for i in range(0,len_data):

        if 'firstName' not in d['persons'][i]:
           
            return False
        elif len(d['persons'][i]['firstName']) == 0:
            return False
        elif 'lastName' not in d['persons'][i]:
            return False
        elif len(d['persons'][i]['lastName']) == 0:
            return False
        elif 'middleName' in d['persons'][i] and len(d['persons'][i]['middleName']) == 0:
            return False

        elif 'age' in d['persons'][i] and (d['persons'][i]['age'] > 100 or d['persons'][i]['age'] < 1):
            return False
            
        elif 'address' not in d['persons'][i]:
            return False
        elif len(d['persons'][i]['address']) != 4:
            return False
        elif 'streetAddress' not in d['persons'][i]['address']:
            return False
        elif len(d['persons'][i]['address']['streetAddress']) == 0:
            return False
        elif isinstance((d['persons'][i]['address']['streetAddress']),basestring) == False:
            return False
        elif 'city' not in d['persons'][i]['address']:
            return False
        elif len(d['persons'][i]['address']['city']) == 0:
            return False
        elif isinstance((d['persons'][i]['address']['city']),basestring) == False:
            return False
        elif 'state' not in d['persons'][i]['address']:
            return False
        elif len(d['persons'][i]['address']['state']) > 3:
            return False
        elif isinstance((d['persons'][i]['address']['state']),basestring) == False:
            return False
        elif 'postalCode' not in d['persons'][i]['address']:
            return False
        elif len(d['persons'][i]['address']['postalCode']) != 6:
            return False
        elif 'phoneNumbers' in d['persons'][i]:
            phone_count = len(d['persons'][i]['phoneNumbers'])
            for j in range(0,phone_count):
                if d['persons'][i]['phoneNumbers'][j]['number'] in phone_dir:
                    return False
                phone_dir.append(d['persons'][i]['phoneNumbers'][j]['number'])
#                print "hi phone dir", phone_dir
                ret_val = fun_validate_phone(d['persons'][i]['phoneNumbers'][j])
                if ret_val == False:
                    return False
        
    return True
def fun_insert_data_in_json_db(output_json_db,file_content):
    conn = sqlite3.connect(output_json_db)
    d = json.loads(file_content)
    conn.execute('''CREATE TABLE IF NOT EXISTS ADDRESS
                (POSTALCODE TEXT PRIMARY KEY NOT NULL,
                CITY TEXT, 
                STATE TEXT);''')


    conn.execute('''CREATE TABLE IF NOT EXISTS NAME
                (PERSONID INTEGER PRIMARY KEY AUTOINCREMENT,
                FIRSTNAME TEXT,
                MIDDLENAME TEXT,
                LASTNAME TEXT,
                STREET TEXT,
                POSTALCODE TEXT,
                FOREIGN KEY (POSTALCODE) REFERENCES ADDRESS(POSTALCODE));''')

    conn.execute('''CREATE TABLE IF NOT EXISTS CONTACT
                (PHONENO TEXT PRIMARY KEY NOT NULL,
                 PHONETYPE TEXT,
                 PERSONID INT,
                 FOREIGN KEY (PERSONID) REFERENCES NAME(PERSONID));''')

            
    len_data = len(d['persons'])
    flag_item = []
    for i in range(0,len_data):
        item = []
        item1 = []
        item2 = []
        len_address = len(d['persons'][i]['address'])
        if (d['persons'][i]['address']['postalCode']) not in flag_item:
            flag_item.append(d['persons'][i]['address']['postalCode'])
            item.append(d['persons'][i]['address']['postalCode'])
            item.append(d['persons'][i]['address']['city'])
            item.append(d['persons'][i]['address']['state'])
        print item
        # conn.execute('insert into ADDRESS values (?,?,?)',item)
        # conn.commit()

        item1.append(d['persons'][i]['firstName'])
        if 'middleName' in d['persons'][i]:
            item1.append(d['persons'][i]['middleName'])
        else:
            item1.append('-')
        item1.append(d['persons'][i]['lastName'])
        item1.append(d['persons'][i]['address']['streetAddress'])
        item1.append(d['persons'][i]['address']['postalCode'])
                     
        print len(item1)
        conn.execute('insert into Name values (?,?,?,?,?)',item1)
        phone_count = len(d['persons'][i]['phoneNumbers'])
        id = 

def fun_validator(input_db,output_tmp_db,output_json_db,sleep_time,table_tmp_db,table_tmptar_db):
    conn = sqlite3.connect(input_db)
    conn1 = sqlite3.connect(output_tmp_db)
    validate_file_name = []
    while(True):
        time.sleep(float(sleep_time))
        item = []
        tmp_ls = []
        cursor = conn.execute("select id,priority from PERSONDATA")
        conn.commit()
        for row in cursor:
            if row[0] not in validate_file_name:
                tup = (row[0],row[1])
                tmp_ls.append(tup)
            else:
                continue
        if tmp_ls != []:
            sorted_list = sorted(tmp_ls,key = itemgetter(1))
            sorted_list_file = map(lambda x:x[0],sorted_list)
            key = sorted_list_file[0]
            
            validate_file_name.append(key)
            cursor = conn.execute("select FDATA from PERSONDATA where id = '"+key+"'")
            for row in cursor:
                file_content = row[0]
            rt = fun_validate_json_file(file_content)
            if rt == True:
                conn1.execute("update FILEDATA SET VALIDATIONRESULT = 'valid' where id = '"+key+"'")
                conn1.commit()
                
                fun_insert_data_in_json_db(output_json_db,file_content)
                
                



def main(input_data_file):
    data = fun_load_json_file(input_data_file)
    input_db = data["validator"][0]["input_db_name"]
    output_tmp_db = data["validator"][0]["output_tmp_db_name"]
    output_json_db = data["validator"][0]["output_json_db_name"]
    
    table_tmp_db = data["validator"][0]["table_tmp_db"]
    table_tmptar_db =data["validator"][0]["table_tmptar_db"]
    sleep_time = data["validator"][0]["sleep_time"]
    fun_validator(input_db,output_tmp_db,output_json_db,sleep_time,table_tmp_db,table_tmptar_db)


if __name__ == "__main__":
    if(len(sys.argv)) != 2:
        print "invalid input"
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print "given input config file doesn't exist"
        exit(0)
    input_data_file = sys.argv[1]
    main(input_data_file)
