import psycopg2

conn = psycopg2.connect(database="qxiubase", user="xyl", password="xieyulonghenrenzhen", host="118.26.153.144", port="5432")
cur = conn.cursor()
cur.execute("insert ;")


def save_psg(dt):
    sql = ("INSERT INTO xyl.now_feedslist_v2 "
            "(feeds_id,is_ad,jump_url,pic_url,preload_doodle_pic_url,preload_file_id,preload_pic_url,preload_video_url,recorder_nick,recorder_pic,recorder_uid,view_times,deadline) "
            "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}');".format(
            dt['feeds_id'],dt['is_ad'],dt['jump_url'],dt['pic_url'],dt['preload_info']['doodle_pic_url'],dt['preload_info']['file_id'],
            dt['preload_info']['pic_url'],dt['preload_info']['video_url'],dt['recorder_nick'],dt['recorder_pic'],dt['recorder_uid'],dt['view_times'],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    cur.execute(sql)
    conn.commit()
    return 'Save successfully!'
