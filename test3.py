import pymysql

print("add")
connect_db = pymysql.connect(  
            user="root",
            password="1234",
            host="127.0.0.1",
            db="detection",
            charset="utf8",
    )
cursor = connect_db.cursor()
    
sql = "SELECT DATE_FORMAT(ob_date, '%Y-%m-%d') AS ob_date, COUNT(*) AS count FROM OBJECT_LOG WHERE OB_STATE = FALSE GROUP BY DATE_FORMAT(ob_date, '%Y-%m-%d') ORDER BY ob_date DESC LIMIT 7"
cursor.execute(sql)
temp_items = cursor.fetchall()
print(type(temp_items[0][0]))