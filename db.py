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