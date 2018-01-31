import os
import json
import sys
import time
import sqlite3
import zlib
import hashlib
from operator import itemgetter

def fun_load_json(config_json):
    with open(config_json) as json_data:
        d = json.load(json_data)
        json_data.close()
    return d

def fun_compress_file_content(input_db_name,output_db_name,table_name,sleep_time):
    conn = sqlite3.connect(input_db_name)
    conn1 = sqlite3.connect(output_db_name)
    conn1.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    compressed_file_name = []
    
    while(True):
        time.sleep(float(sleep_time))
        item = []
        tmp_ls = []
        cursor = conn.execute("Select id,priority from PERSONDATA")
        conn.commit()
        for row in cursor:
            if row[0] not in compressed_file_name:
            
                tup = (row[0],row[1])
                tmp_ls.append(tup)
            else:
                continue
        if tmp_ls != []:
            sorted_list = sorted(tmp_ls,key = itemgetter(1))
            sorted_list_file = map(lambda x: x[0],sorted_list)
            sorted_list_priority = map(lambda x : x[1],sorted_list)
            key = sorted_list_file[0]
            print key
            compressed_file_name.append(key)
            key_priority = sorted_list_priority[0]
            conn = sqlite3.connect(input_db_name)
        
            cursor = conn.execute("select FDATA from PERSONDATA where id = '"+key+"'")
            for row in cursor:
                strring = row[0]
            code = zlib.compress(strring)
#            print "hi :", type(code)
            md5_val = hashlib.md5(key).hexdigest()
#            print "hey ", type(md5_val)
            item.append(key)
            item.append(code)
            item.append(md5_val)
            item.append(key_priority)
            item.append("notknown")
            print item
            conn1.execute('''CREATE TABLE IF NOT EXISTS FILEDATA
            (ID TEXT PRIMARY KEY           NOT NULL,
            COMPRESSEDFILEDATA     TEXT,
            MD5HASHVALUE           TEXT,
            PRIORITY               INT,
            VALIDATIONRESULT       TEXT);''')
#            conn1.execute('insert into FILEDATA values (?,?,?,?,?)',item)
            conn1.commit()
        

def main(input_data):
    db_name_dict = fun_load_json(input_data)
    input_db_name = db_name_dict["compressor"][0]["input_db_name"]
    output_db_name = db_name_dict["compressor"][0]["output_db_name"]
    table_name = db_name_dict["compressor"][0]["table_name"]
    sleep_time = db_name_dict["compressor"][0]["sleep_time"]
    fun_compress_file_content(input_db_name,output_db_name,table_name,sleep_time)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "invalid input"
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print "target directory not found"
        exit(0)
    main(sys.argv[1])
    
