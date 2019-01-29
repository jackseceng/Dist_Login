import mysql.connector


sql_connection = mysql.connector.connect(
    user='<user>',
    password='<password>',
    host='<mysql_address>',
    database='dist_login')


sql_cursor = sql_connection.cursor()


def sql_read_identifier(user):
    # print("identifier sql read identifier") # Uncomment this for debugging
    cmd = ("select identifier from identifiers where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    stored_identifier = str(sql_cursor.fetchall())
    return stored_identifier.strip("()[],'")


def sql_write_user_identifiers(user, identifier):
    # print("identifier sql write user identifiers") # Uncomment this for debugging
    cmd = ("insert into identifiers (username, identifier) values ('%s', '%s')") % (user, identifier)
    sql_cursor.execute(cmd)
    sql_connection.commit()


def sql_close_connection():
    # print("identifier sql close connection") # Uncomment this for debugging sql
    sql_connection.close()
