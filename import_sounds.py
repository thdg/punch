import mysql.connector
from datetime import datetime


def main():
    wav_folder = "ogg/"
    db_name = "cocktail"
    
    with open("ogg_info.txt", "r") as info:
        lines = info.readlines()
    
    cnx = mysql.connector.connect(user="root", 
        password="root", host="localhost", database=db_name)
    c = cnx.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS sounds ( "
        "id int(10) unsigned NOT NULL AUTO_INCREMENT, "
        "name varchar(100) not null, "
        "sex varchar(50) not null, "
        "age varchar(50) not null, "
        "text varchar(300) not null, "
        "time double unsigned not null, "
        "primary key (id) "
        ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;")

    add_sound = ("INSERT INTO sounds "
        "(name, sex, age, text, time) "
        "VALUES "
        "(%s, %s, %s, %s, %s)")
    
    i = 0
    for line in lines:
        file_name, env, _, sex, age, text, t, file_type, sample_rate, channels, encoding = line.split("\t")
        print(file_name, sex, age, t)
            
        c.execute(add_sound, (
            file_name, 
            sex,
            age,
            text,
            t)
        )
        cnx.commit()

    c.close()
    cnx.close()


if __name__ == "__main__":
    main()

