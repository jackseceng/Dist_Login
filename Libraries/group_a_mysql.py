import mysql.connector


sql_connection = mysql.connector.connect(
    user='<user>',
    password='<password>',
    host='<mysql_address>',
    database='dist_login')


sql_cursor = sql_connection.cursor()


def sql_write_username_timestamp(user):
    # print("Group A write username timestamp") # Uncomment this for debugging sql
    cmd = ("insert into credentials (username, timestamp) values ('%s', NOW())") % (user)
    sql_cursor.execute(cmd)
    cmd = ("insert into fingerprints (username) values ('%s')") % (user)
    sql_cursor.execute(cmd)
    sql_connection.commit()


def sql_write_timestamp(user):
    # print("Group A write timestamp") # Uncomment this for debugging sql
    cmd = ("update credentials set timestamp = NOW() where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    sql_connection.commit()


def sql_write_chunk_fingerprint(user, chunk, fingerprint):
    # print("Group A write chunk fingerprint") # Uncomment this for debugging sql
    cmd = ("update credentials set key_chunk=CONCAT('%s') where credentials.username = '%s'") % (chunk, user)
    sql_cursor.execute(cmd)
    cmd = ("update fingerprints set fingerprint=CONCAT('%s') where fingerprints.username =  '%s'") % (fingerprint, user)
    sql_cursor.execute(cmd)
    sql_connection.commit()


def sql_read_timestamp(user):
    # print("Group A read timestamp") # Uncomment this for debugging sql
    cmd = ("select timestamp from credentials where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    timestamp = str(sql_cursor.fetchall())
    return timestamp


def sql_read_key_chunk(user):
    # print("Group A read key chunk") # Uncomment this for debugging sql
    cmd = ("select key_chunk from credentials where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    key_chunk = str(sql_cursor.fetchall())
    return key_chunk.strip("()[],'")


def sql_read_fingerprint(user):
    # print("Group A read fingerprint") # Uncomment this for debugging sql
    cmd = ("select fingerprint from fingerprints where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    fingerprint = str(sql_cursor.fetchall())
    return fingerprint.strip("()[],'")


def clear_group_a(user):
    # print("Group A clear group a") # Uncomment this for debugging sql
    chunk = "blank"
    fingerprint = "blank"
    cmd = ("update credentials set key_chunk=CONCAT('%s') where credentials.username = '%s'") % (chunk, user)
    sql_cursor.execute(cmd)
    cmd = ("update fingerprints set fingerprint=CONCAT('%s') where fingerprints.username =  '%s'") % (fingerprint, user)
    sql_cursor.execute(cmd)
    sql_connection.commit()


def sql_close_connection():
    # print("Group A close connection") # Uncomment this for debugging sql
    sql_connection.close()
