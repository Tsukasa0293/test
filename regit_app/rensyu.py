import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

db = 'rensyu.db'
con = sqlite3.connect(db)
cur = con.cursor()
sql = """create table if not exists test(
            id integer primary key autoincrement,
            name text,
            age integer
)"""
cur.execute(sql)
con.commit()
cur.close()
con.close()


def get_ccs():
    con = sqlite3.connect('./rensyu.db')
    cur = con.cursor()
    cur.execute('select id,name from test')
    cc_id = cur.fetchall()
    con.close()
    return cc_id

@app.route('/')
def form():
    if 'a' not in session:
        session['a'] = ''
    if 'total' not in session:
        session['total'] = 0    
    cc_id = get_ccs()
    return render_template('rensyu.html', cc_id = cc_id)

@app.route('/create_cc', methods=['POST', 'GET'])
def create_cc():
    if request.method == 'POST':
        name_form = request.form['name']
        age_form = request.form['age']
        age_form = int(age_form)
        con = sqlite3.connect('./rensyu.db')
        cur = con.cursor()
        sql = f'insert into test(name, age) values(?,?)'
        data = (name_form, age_form)
        cur.execute(sql, data)
        con.commit()
        cur.execute('select * from test')
        rows = cur.fetchall()
        session['a'] = rows
        con.close()
        cc_id = get_ccs()
    return render_template('rensyu.html', cc_id = cc_id)

@app.route('/clear', methods=['POST'])
def clear():
    con = sqlite3.connect('./rensyu.db')
    cur = con.cursor()
    cur.execute("DELETE FROM test")
    cur.execute("DELETE FROM sqlite_sequence ")
    con.commit()
    cur.execute('select * from test')
    rows = cur.fetchall()
    session['a'] = rows
    con.close()
    return render_template('rensyu.html')

@app.route('/select_cc', methods=['POST'])
def select_cc():
    con = sqlite3.connect('./rensyu.db')
    cur = con.cursor()
    con.close()
    return render_template('./rensyu.db')



if __name__ == '__main__':
    app.run(debug=True,port=8080)