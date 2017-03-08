import mysql.connector
from datetime import datetime


TAG = {}


def tag_id(tag, c):
    try:
        return TAG[tag]
    except KeyError:
        c.execute("INSERT INTO tagInfo (tagName) VALUE (%s)", (tag,))
        new_tag_id = c.lastrowid
        TAG[tag] = new_tag_id
        return new_tag_id


def main():
    wav_folder = "ogg/"
    db_name = "cocktail"
    
    with open("wav_info.txt", "r") as info:
        lines = info.readlines()
    
    cnx = mysql.connector.connect(user="root", 
        password="root", host="localhost", database=db_name)
    c = cnx.cursor()
    
    add_file = ("INSERT INTO fileInfo "
        "(fileName, file, fileSizeKb, fileLenSec) "
        "VALUES "
        "(%s, %s, %s, %s)")
    
    add_snippet = ("INSERT INTO snippetInfo "
        "(fileID, sizeKb, startTime, lenSec, creationDate, lastModifiedDate, userId) "
        "VALUES "
        "(%s, %s, %s, %s, %s, %s, %s)")
    
    add_tag = ("INSERT INTO bridgeSnippetTagTable "
        "(snippetID, tagID) "
        "VALUES "
        "(%s, %s)")
    
    i = 0
    for line in lines:
        file_name, env, _, sex, age, text, t, file_type, sample_rate, channels, encoding = line.split("\t")
        print(file_name, sex, age, t)
        with open(wav_folder + file_name, "rb") as f:
            data = f.read()
            
            c.execute(add_file, (
                file_name[:-4], 
                data, 
                len(data),
                t)
            )
            
            file_id = c.lastrowid
            c.execute(add_snippet, (
                file_id,
                len(data),
                0,
                t,
                datetime.now(),
                datetime.now(),
                1)
            )
            
            snippet_id = c.lastrowid
            for tag in [sex, age]:
                c.execute(add_tag, (
                    snippet_id,
                    tag_id(tag, c))
                )

            cnx.commit()

    cnx.commit()
    c.close()
    cnx.close()


if __name__ == "__main__":
    main()

