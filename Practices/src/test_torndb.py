#coding=utf8

import torndb
import json
from datetime import date, datetime 

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
#             return json.JSONEncoder.default(self, obj)
            raise TypeError('%r is not JSON serializable' % obj) 
        
def main():
    db = torndb.Connection("127.0.0.1:3306", "sample", user = "root", password = "123456")
    sql = "Select * from mytable"
    dataset = db.query(sql);
    print dataset
    datastring = json.dumps(dataset,cls=CJsonEncoder)
    print datastring
    db.close()
    
main()