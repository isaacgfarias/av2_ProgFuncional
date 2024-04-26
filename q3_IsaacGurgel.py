import mysql.connector


execsqlcmd = lambda cmd, crs: crs.execute(cmd)

mydb = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="root",
    )

crs = mydb.cursor()

exec_create_database = lambda dbname, crs: execsqlcmd(f"CREATE DATABASE IF NOT EXISTS {dbname};\n", crs)
exec_use_database = lambda dbname, crs: execsqlcmd(f"USE {dbname};\n", crs)
exec_drop_database = lambda dbname, crs: execsqlcmd(f"DROP DATABASE IF EXISTS {dbname};\n", crs)
exec_create_table = lambda table, attrs, crs: execsqlcmd(f"CREATE TABLE IF NOT EXISTS {table} ({attrs});\n", crs)
exec_drop_table = lambda table, crs: execsqlcmd(f"DROP TABLE IF EXISTS {table};\n", crs)

exec_insert_into = lambda table, attrs, values, crs: execsqlcmd(f"INSERT INTO {table} ({attrs}) VALUES ({values});\n", crs)
exec_delete_from_where = lambda table, condition, crs: execsqlcmd(f"DELETE FROM {table} WHERE {condition};\n", crs)
exec_select_from_where = lambda table, attrs, condition, crs: execsqlcmd(f"SELECT {attrs} FROM {table} WHERE {condition};\n", crs)

## CRIAÇÃO DO BANCO DE DADOS E TABELAS
exec_create_database("av2func", crs)
exec_use_database("av2func", crs)

exec_create_table("PUBLISHERS", "id_publisher INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), country VARCHAR(255)", crs)
exec_create_table("BOOKCLUBS", "id_club INT PRIMARY KEY, name VARCHAR(255), id_publisher INT, creation_date DATE, FOREIGN KEY (id_publisher) REFERENCES PUBLISHERS(id_publisher)", crs)
exec_create_table("MEMBERS", "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), country VARCHAR(255), id_club INT, FOREIGN KEY (id_club) REFERENCES BOOKCLUBS(id_club)", crs)
exec_create_table("BOOKS", "id_book INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), genre VARCHAR(255), release_date DATE, id_club INT, FOREIGN KEY (id_club) REFERENCES BOOKCLUBS(id_club)", crs)

########Exemplos#############
## INSERÇÃO DE DADOS
exec_insert_into("publishers", "name, country", "'Penguin', 'USA'", crs)
exec_insert_into("publishers", "name, country", "'HarperCollins', 'USA'", crs)

## REMOÇÃO DE DADOS
exec_delete_from_where("publishers", "name = 'Penguin'", crs)

## SELEÇÃO DE DADOS
exec_select_from_where("publishers", "*", "country = 'USA'", crs)


res = crs.fetchall()

print_result = lambda res: [print(row) for row in res]

print_result(res)

exec_drop_table("books", crs)
exec_drop_table("members", crs)
exec_drop_table("bookclubs", crs)
exec_drop_table("publishers", crs)
exec_drop_database("av2func", crs)

mydb.commit()
mydb.close()
