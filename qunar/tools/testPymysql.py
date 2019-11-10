import pymysql

connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='dy123456',
            database='qunar',
            charset='utf8mb4'
        )

cursor = connection.cursor()
# sql = "insert into sight values ('{0}', '{1}', '{2}', '{3}', '{4}'," \
#               " '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', {12})"
# try:
#     cursor.execute(sql.format('aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', 'kkk', 'lll', '123'))
#     connection.commit()
#     cursor.execute(sql.format('aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', 'kkk', 'lll', '123'))
#     connection.commit()
# except pymysql.err.IntegrityError:
#     cursor.execute(sql.format('aaaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', 'kkk', 'lll', '123'))
#     connection.commit()

select_sql = "select subject from sight where sightId = '{0}'"
result = cursor.execute(select_sql.format('aaa'))
subject = cursor.fetchone()[0]
subject += 'bbb'
update_sql = "update sight set subject = '{0}' where sightId = '{1}'"
cursor.execute(update_sql.format(subject, 'aaa'))
connection.commit()
cursor.close()
connection.close()
