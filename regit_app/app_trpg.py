from flask import Flask, redirect, render_template, request, session, url_for
import random, re, sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

db = 'dice.db'
con = sqlite3.connect(db)
cur = con.cursor()
sql = """create table if not exists roll(
            command_id integer primary key autoincrement,
            command text,
            result text
)"""
cur.execute(sql)
con.commit()
cur.close()
con.close()

def get_ccs():
    #if dice == 'command':
        con = sqlite3.connect('./dice.db')
        cur = con.cursor()
        cur.execute('select command_id,command from roll')
        command_db = cur.fetchall()
        con.close()
        return command_db

@app.route('/')
def route():
    session['result'] = ""
    session['total'] = ""
    session['dice_list'] = ""
    session['text_dice'] = ""
    return render_template('trpg.html')

def roll(Quantity, Value):
    value = int(Value)
    quantity = int(Quantity)
    total = session['total']
    dice_list = []
    dice_list.extend(session['dice_list'])
    if value >= 1 and quantity >= 1:
        for roll in range(quantity):
            result = random.randint(1,value)
            dice_list.append(result)
            total += result
            session['total'] = total
            session['dice_list'] = dice_list
    else :
        session['result'] = "エラー(1以上かつ整数で記入してください。)"

@app.route('/dice', methods=['get', 'post'])
def dice():
    if request.method == 'post':
        value_form = request.form['value']
        value_list = value_form.split('+')
        session['total'] = 0
        roll_list = []
        for a in range(len(value_list)):
            value = value_list.pop(0)
            b = value.split('d')
            roll(b[0], b[1])
            roll_list.extend(session['dice_list'])
            session['result'] = roll_list
            roll_list = []
        session['dice_list'] = ""
        session['text_dice'] = value_form
        con = sqlite3.connect('./dice.db')
        cur = con.cursor()
        sql = f'insert into roll(command, result) values(?,?)'
        data = (value_form, session['total'])
        cur.execute(sql, data)
        con.commit()
        cur.execute('select * from roll')
        rows = cur.fetchall()
        session['test'] = rows
        con.close()
    return render_template('trpg.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080)