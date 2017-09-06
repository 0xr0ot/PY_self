import pymysql


def save_data(dt):
    sql =  ("INSERT INTO db.table "
            "(app_name,deadline,platform,active_yesterday,launch_yesterday,install_yesterday,install_all,"
            "sdk_version,sdk_tip,starred,app_id,game,report_path,host_url)"
            "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}');".format(
            dt['name'],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dt['platform'],dt['active_yesterday'],dt['launch_yesterday'],dt['install_yesterday'],dt['install_all'],
            dt['sdk_version'],dt['sdk_tip'],dt['starred'],dt['app_id'],dt['game'],dt['report_path'],csrf_url))

    cur.execute(sql)
    conn.commit()
    return 'Save successfully!\r\n {0}'.format(dt)


if __name__ == '__main__':
    url = 'https://xxxx'
    conn = pymysql.connect(host='xxx.xx.xx.xx',
                                 port=33066, #not str
                                 user='xxxx',
                                 password='xxxx',
                                 database='bd_xx',
                                 charset='utf8mb4')
                                 #cursorclass=pymysql.cursors.DictCursor)

    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS db.table "
        "(app_name text,deadline timestamp PRIMARY KEY,platform text,active_yesterday int,"
        "launch_yesterday int,install_yesterday int,install_all int,"
        "sdk_version text,sdk_tip text,starred text,app_id text,game text,report_path text,host_url text);")
    session = requests.Session()
    main() #TODO
    cur.close()
    conn.close()
    session.close()
    print('All end.')
######################################--------------------------############################################################
# Connect to the database
connection = pymysql.connect(host='localhost',
                             port=3306,#not str
                             user='user',
                             password='passwd',#passwd
                             database='db',#db
                             charset='utf8mb4')
                             #cursorclass=pymysql.cursors.DictCursor
                             #)
    
try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
