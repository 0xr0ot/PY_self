import psycopg2
import datetime

def save_psg(dt):
    sql = ("INSERT INTO ulion.feedslist (feeds_id,view_times,deadline) VALUES ('{0}','{1}','{2}');".format(
            dt['feeds_id'],dt['view_times'],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    cur.execute(sql)
    conn.commit()
    return 'Save successfully!'

def main():
    ##TODO
    for dt in data:
        #print(dt)
        save_psg(dt)
        #print('save successfully.')
    return 'func_main finished!'

if __name__ == '__main__':
    conn = psycopg2.connect(database="db", user="ulion", password="xxxx", host="xxx.xx.xxx.xxx", port="5432")
    cur = conn.cursor()
    cur.execute("CREATE TABLE ulion.feedslist (feeds_id varchar PRIMARY KEY,view_times integer,deadline timestamp);")
    main()##TODO
    cur.close()
    conn.close()
