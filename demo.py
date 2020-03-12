import psycopg2
connection = psycopg2.connect('dbname = example')
# Open a cursor to perform database operations
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS table2;')
# create the todos table
# note : triple quotes allow multiline text in python
cursor.execute("""CREATE TABLE table2 (id INTEGER PRIMARY KEY,completed BOOLEAN NOT NULL DEFAULT False);""")
# string interpolation to compose a SQL query using python strings
# Using %s, passing in a tuple as the 2nd argument
cursor.execute('INSERT INTO table2 (id,completed)VALUES(%s,%s);',(1,True))
# Using named string parameters %(foo)s, passing in a dictionary instead.
data = {
    'id':2,
    'completed':False
}
SQL = 'INSERT INTO table2 (id,completed) VALUES(%(id)s,%(completed)s);'
cursor.execute(SQL,data)

cursor.execute('INSERT INTO table2 (id,completed)VALUES(%s,%s);',(3,True))
# Fetching the results through python
cursor.execute('SELECT * from table2;')
result = cursor.fetchmany(2)
print('fetchmany(2)',result)
result2 = cursor.fetchone()
print('fetchone',result2)
cursor.execute('SELECT * from table2;')
result3 = cursor.fetchone()
print('fetchone',result3)
connection.commit()
connection.close()
cursor.close()