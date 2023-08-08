import sqlite3

conn=sqlite3.connect('sportdata.db')
conn.row_factory = sqlite3.Row
values = conn.execute('''SELECT * FROM certificati''').fetchall()
for v in values:
    print(v.keys())
    try:
        conn.execute('''REPLACE INTO medical_cert(id_no,date_of_emission)
                    VALUES (?,?)''',(v['ID'],v['Data']))
    except: continue
    conn.commit()
conn.close()