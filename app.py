from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date, time, datetime

DB = 'sportdata.db'

def decrCapital(total, conn: sqlite3.Connection):
    conn.execute('''UPDATE club
                 SET capital=((SELECT capital FROM club)-?)''',(total,))
    conn.commit()
    conn.close()

def incrCapital(total, conn: sqlite3.Connection):
    conn.execute('''UPDATE club
                 SET capital=((SELECT capital FROM club)-?)''',(total,))
    conn.commit()
    conn.close()

def selecter(db: str, query: str, num='all'):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    if num == 'all':
        result = conn.execute(query).fetchall()
    if num == 'one':
        result = conn.execute(query).fetchone()
    if num == 'many':
        result = conn.execute(query).fetchmany()
    conn.close()
    return result

app = Flask(__name__)

@app.route('/')
def index():
    club = selecter(DB, 'SELECT * FROM club')
    return render_template('index.html', club=club)

@app.route('/atleti')
def atlteti():
    atleti = selecter(DB, '''SELECT * FROM athlete LEFT JOIN (
                      SELECT athlete_attendance.athlete, COUNT(*) AS pres
                      FROM athlete_attendance 
                      WHERE (kind='allenamento'))
                      ON athlete = id_no
                      ORDER BY(id_no)
                       ''')
    return render_template('atleti.html',atleti=atleti)

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/allenatori')
def allenatori():
    allenatori = selecter(DB, 'SELECT * FROM coach')
    return render_template('allenatori.html', allenatori=allenatori)

@app.route('/accompagnatori')
def accompagnatori():
    accompagnatori = selecter(DB, 'SELECT * FROM companion')
    return render_template('allenatori.html', accompagnatori=accompagnatori)

@app.route('/volontari')
def volontari():
    volontari = selecter(DB,'SELECT * FROM volunteer')
    return render_template('allenatori.html', volontari=volontari)

@app.route('/sponsor')
def sponsor():
    sponsor = selecter(DB, '''SELECT p_iva, company_name, telephone_no, email, start_date, end_date, sponsor_value 
                              FROM company INNER JOIN sponsorship ON company.p_iva = sponsorship.company''')
    return render_template('sponsor.html',sponsor=sponsor)

@app.route('/pagamenti')
def pagamenti():
    return render_template('pagamenti.html')

@app.route('/pagamenti_atleti', methods=('GET','POST'))
def pagamenti_atlteti():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    atleti = conn.execute('''SELECT club.club_name, club.id_no, athlete.id_no id, athlete.name, athlete.surname, payment_date, payment_time, total
                              FROM (club INNER JOIN athlete_payment ON club.id_no = club) 
                             INNER JOIN athlete ON athlete = athlete.id_no''').fetchall()
    if request.method == 'POST':
        conn.execute('''INSERT INTO athlete_payment (club , athlete , payment_date , payment_time, total)
                     VALUES ((SELECT id_no FROM club), ?,?,?,?)''', 
                     (request.form['atleta'],request.form['data'], request.form['ora'], request.form['total']))
        conn.commit()
        decrCapital(request.form['total'],conn)
    conn.close()
    return render_template('pagamenti_atleti.html',atleti=atleti)


    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    atleti = conn.execute('''SELECT club.club_name, club.id_no, athlete.id_no id, athlete.name, athlete.surname, payment_date, payment_time, total
                              FROM (club INNER JOIN athlete_payment ON club.id_no = club) 
                             INNER JOIN athlete ON athlete = athlete.id_no''').fetchall()
    if request.method == 'POST':
        print("E' stata fatta una richiesta POST!")
        print(request.form['atleta'],request.form['total'],request.form['data'],request.form['ora'])
        conn.execute('''INSERT INTO athlete_payment (club , athlete , payment_date , payment_time, total)
                     VALUES ((SELECT id_no FROM club), ?,?,?,?)''', 
                     (request.form['atleta'],request.form['data'], request.form['ora'], request.form['total']))
        conn.commit()
        updateCapital(request.form['totale'],conn)
    conn.close()
    return render_template('pagamenti_atleti.html',atleti=atleti)

@app.route('/pagamenti_allenatori', methods=('GET','POST'))
def pagamenti_allenatori():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    allenatori = conn.execute('''SELECT club.club_name, club.id_no,coach.id_no id, coach.name, coach.surname, payment_date, payment_time, total
                              FROM (club INNER JOIN coach_payment ON club.id_no = club) 
                              INNER JOIN coach ON coach = coach.id_no''').fetchall()
    if request.method == 'POST':
        conn.execute('''INSERT INTO coach_payment (club , coach , payment_date , payment_time, total)
                     VALUES ((SELECT id_no FROM club), ?,?,?,?)''', 
                     (request.form['all'],request.form['data'], request.form['ora'], request.form['total']))
        conn.commit()
        decrCapital(request.form['total'],conn)
    conn.close()
    return render_template('pagamenti_allenatori.html', allenatori=allenatori)

@app.route('/pagamenti_sponsor', methods=('GET','POST'))
def pagamenti_sponsor():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    sponsor = conn.execute('''SELECT club.club_name, club.id_no, p_iva, company.company_name, payment_date, payment_time, total
                              FROM (club INNER JOIN sponsor_payment ON id_no = club) 
                              INNER JOIN company ON company = p_iva''').fetchall()
    if request.method == 'POST':
        #print("E' stata fatta una richiesta POST!")
        #print(request.form['all'],request.form['total'],request.form['data'],request.form['ora'])
        conn.execute('''INSERT INTO sponsor_payment (club , company , payment_date , payment_time, total)
                     VALUES ((SELECT id_no FROM club), ?,?,?,?)''', 
                     (request.form['az'],request.form['data'], request.form['ora'], request.form['total']))
        conn.commit()
        incrCapital(request.form['total'],conn)
    conn.close()
    return render_template('pagamenti_sponsor.html',sponsor=sponsor)

@app.route('/medico')
def medico():
    atleti_inf = selecter(DB,'SELECT * FROM injured_athletes')
    return render_template('medico.html', atleti=atleti_inf)

@app.route('/eventi')
def eventi():
    eventi = selecter(DB, 'SELECT * FROM sport_event')
    return render_template('eventi.html', eventi=eventi)

@app.route('/certificati', methods=('GET','POST'))
def certificati():
    valid = selecter(DB,'''SELECT athlete.id_no, athlete.name, athlete.surname, date_of_emission
                            FROM athlete INNER JOIN medical_cert ON athlete.id_no = medical_cert.id_no
                            WHERE (medical_cert.date_of_emission > DATE('now','-1 year'))
                            ORDER BY (date_of_emission)''')
    scad = selecter(DB,'''SELECT athlete.id_no, name, surname, date_of_emission
                            FROM athlete INNER JOIN medical_cert ON athlete.id_no = medical_cert.id_no
                            WHERE (medical_cert.date_of_emission <= DATE('now','-1 year'))
                            ORDER BY (date_of_emission);''')
    if request.method=='POST':
        id_no=request.form['id']
        date=request.form['date']
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        conn.execute('''REPLACE INTO medical_cert (id_no, date_of_emission)
                            VALUES (?,?)''',
                            (id_no,date))
        conn.commit()
    return render_template('certificati.html', valid=valid, scad=scad)

@app.route('/test')
def test():
    test = selecter(DB,'''SELECT athlete.id_no, name, surname, jump, sprint, endurance
                            FROM athlete LEFT OUTER JOIN physical_test ON athlete.id_no = physical_test.id_no
                            ORDER BY athlete.id_no;''')
    bestj = selecter(DB, '''SELECT athlete.id_no, name, surname, jump, sprint, endurance
                            FROM athlete LEFT OUTER JOIN physical_test ON athlete.id_no = physical_test.id_no
                            WHERE (jump >= (SELECT MAX(jump) FROM physical_test));''', num='one')
    bests = selecter(DB, '''SELECT athlete.id_no, name, surname, jump, sprint, endurance
                            FROM athlete LEFT OUTER JOIN physical_test ON athlete.id_no = physical_test.id_no
                            WHERE (sprint <= (SELECT MAX(sprint) FROM physical_test));''', num='one')
    beste = selecter(DB, '''SELECT athlete.id_no, name, surname, jump, sprint, endurance
                            FROM athlete LEFT OUTER JOIN physical_test ON athlete.id_no = physical_test.id_no
                            WHERE (endurance >= (SELECT MAX(endurance) FROM physical_test));''', num='one')
    return render_template('test.html', test=test, bestj=bestj, bests=bests, beste=beste)

@app.route('/aggiungi', methods=('GET','POST'))
def aggiungi():
    if request.method == 'POST':
        print(request.form)
        id_no=request.form['id_no']
        name=request.form['name']
        surname=request.form['surname']
        tel=request.form['tel']
        email=request.form['email']
        addr=request.form['addr']
        cat=request.form['cat']
        h=request.form['h']
        w=request.form['w']
        pos=request.form['pos']
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        conn.execute('''INSERT INTO athlete (id_no,name,surname,telephone_no,email,category,height,weight,position,adress)
                        VALUES (?,?,?,?,?,?,?,?,?,?)''',
                        (id_no,name,surname,tel,email,cat,h,w,pos,addr)
                        )
        conn.commit()
        conn.close()
        return redirect('/atleti')
    return render_template('aggiungi.html')

@app.route('/<int:id_no>/chiudiInf', methods=('POST',))
def chiudiInf(id_no):
    conn=sqlite3.connect(DB)
    conn.row_factory=sqlite3.Row
    conn.execute('''UPDATE athlete
                 SET injured = 0
                 WHERE (id_no=?)''',(id_no,))
    conn.commit()
    conn.close()
    return redirect('/medico')

@app.route('/<int:id_no>/apriInf', methods=('POST',))
def apriInf(id_no):
    conn=sqlite3.connect(DB)
    conn.row_factory=sqlite3.Row
    conn.execute('''UPDATE athlete
                 SET injured = 1
                 WHERE (id_no=?)''',(id_no,))
    conn.commit()
    conn.close()
    return redirect('/atleti') 

@app.route('/contratti', methods=('GET','POST'))
def contratti():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    atleti=conn.execute('''SELECT protocol_no, id_no, name, surname, starting_date, expiry_date, salary
                        FROM contract INNER JOIN (athlete a INNER JOIN stipulate_athlete s ON a.id_no=s.athlete) ON protocol_no = contract
                        ORDER BY(expiry_date)''').fetchall()
    allenatori=conn.execute('''SELECT protocol_no, id_no, name, surname, starting_date, expiry_date, salary
                            FROM contract INNER JOIN (coach c INNER JOIN stipulate_coach s ON c.id_no=s.coach) ON protocol_no = contract
                            ORDER BY(expiry_date)''').fetchall()
    if request.method == 'POST':
        id_no=request.form['id']
        num=request.form['num']
        start=request.form['start_date']
        end=request.form['end_date']
        valore=request.form['valore']
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        conn.execute('''INSERT INTO contract (protocol_no,starting_date,expiry_date,salary)
                            VALUES (?,?,?,?)''',
                            (num,start,end,valore))
        if request.form['kind'] == 'athlete':
            conn.execute('''INSERT INTO stipulate_athlete (contract,athlete)
                            VALUES (?,?)''',
                            (num,id_no))
        else:
            conn.execute('''INSERT INTO stipulate_coach (contract,coach)
                            VALUES (?,?)''',
                            (num,id_no))
        conn.commit()
    conn.close()
    return render_template('contratti.html',atleti=atleti,allenatori=allenatori) 