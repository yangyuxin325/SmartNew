import mysql.connector
config={'host':'127.0.0.1',
        'user':'root',
        'password':'123456',
        'port':3306,
        'database':'sample',
        }

try:
    cnn=mysql.connector.connect(**config)
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))
    
cursor=cnn.cursor()

try:
    sql_query='Select name,sex,birth,birthaddr from mytable'
    cursor.execute(sql_query)
    
    for name,sex,birth,birthaddr in cursor:
        print(name,sex,birth,birthaddr)
except mysql.connector.Error as e:
    print('query error!{}'.format(e))
    
finally:
    cursor.close()
    cnn.close()