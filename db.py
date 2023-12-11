# db: database calls
import sqlite3

def next_csv_id(): #get next id for csv file and iterate
    conn = sqlite3.connect("main.db")
    cur = conn.cursor()

    # get current count
    cur.execute("SELECT count FROM csv_count WHERE id = 1")
    rows = cur.fetchone()[0]

    print("rows:", rows)
    
    # iterate
    count = rows + 1

    print("count:", count)

    cur.execute("UPDATE csv_count SET count = :count WHERE id = 1", (count,))
    conn.commit()
    
    conn.close()

    return count


def addimage(session_id, img_count, filename, hash, filetype): #add images data to db
    conn = sqlite3.connect("main.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO image_log(session_id, img_count, filename, hash, filetype, time_added, status) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)", (session_id, img_count, filename, hash, filetype, 0))
    conn.commit()

    conn.close()


def get_next_image(session_id): # Get the next un-tagged image in the session (ordered by img_count) and return its filename. return 1 if no more images TODO: return 1 if no records
    conn = sqlite3.connect("main.db")
    cur = conn.cursor()

    cur.execute("SELECT id, filename, img_count, hash, filetype FROM image_log WHERE session_id = ? AND status = 0 ORDER BY img_count", (session_id,))
    rows = cur.fetchone()

    #placeholder = ["testimg.jpg", 2, "testfiletype", "testhash"]
    print("DB RESULT:", rows)
    conn.close()

    return rows

def add_tag(id, data): # add tag data to image by image id TODO: add date stamp
    conn = sqlite3.connect("main.db")
    cur = conn.cursor()

    cur.execute("UPDATE image_log SET data = :data, status = 1 WHERE id = :id", (data, id))
    conn.commit()
    conn.close()

def get_image_data(img_id): # get data on image for csv row using img_id
    conn = sqlite3.connect("main.db")
    cur = conn.cursor()

    cur.execute("SELECT filename, img_count, filetype, hash FROM image_log WHERE id = ?", (img_id,))
    rows = cur.fetchone()

    print("DB RESULT:", rows)
    conn.close()

    return rows