import mysql.connector as SQL

database = SQL.connect(host = 'sql6.freesqldatabase.com',
                       database = "sql6473907",
                       user = 'sql6473907',
                       password = 'SUe2hRjxgk')

cursor = database.cursor()



cursor.execute(f"""
                 create table Stud_Record(
                     chat_id bigint primary key not null,
                     usn char(11) unique not null,
                     name char(50) not null,
                     status char(10) not null check (status in ('Active','Inactive')),
                     year int not null check (year in (1, 2, 3, 4)),
                     semester TINYINT not null check (semester in (1, 2, 3, 4, 5, 6, 7, 8))
                 );
                 """)

database.close()