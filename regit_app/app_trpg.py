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
            result text,
            result_list text
)"""
cur.execute(sql)
con.commit()
cur.close()
con.close()

db = 'status.db'
con = sqlite3.connect(db)
cur = con.cursor()
sql = """create table if not exists character(
            name text ,
            user_id integer primary key
)"""
cur.execute(sql)
con.commit()
con.close()

db = 'status.db'
con = sqlite3.connect(db)
cur = con.cursor()
sql = """
CREATE TABLE IF NOT EXISTS ability (
    user_id INTEGER PRIMARY KEY,
    str INTEGER DEFAULT 0,
    con INTEGER DEFAULT 0,
    pow INTEGER DEFAULT 0,
    dex INTEGER DEFAULT 0,
    app INTEGER DEFAULT 0,
    siz INTEGER DEFAULT 0,
    int INTEGER DEFAULT 0,
    edu INTEGER DEFAULT 0,
    san INTEGER DEFAULT 0,
    luck INTEGER DEFAULT 0,
    idea INTEGER DEFAULT 0,
    know INTEGER DEFAULT 0,
    hp INTEGER DEFAULT 0,
    mp INTEGER DEFAULT 0,
    sp INTEGER DEFAULT 0,
    ip INTEGER DEFAULT 0,
    dbs INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES character(user_id)
)
"""
cur.execute(sql)
con.commit()
con.close()

def command_db(command):
    con = sqlite3.connect('./dice.db')
    cur = con.cursor()
    if command == 'command':
        cur.execute('select command ' 
                    'from roll ' 
                    'order by command_id asc ' 
                    'limit 4 offset max((SELECT COUNT(command_id) FROM roll) - 4, 0)')
        command_dice = cur.fetchall()
        con.close()
        return command_dice
    elif command == 'result':
        cur.execute('select result,result_list ' 
                    'from roll ' 
                    'order by command_id asc ' 
                    'limit 4 offset max((select count(command_id) from roll) - 4,  0)')
        result_dice = cur.fetchall()
        con.close()
        return result_dice
    elif command == 'delete':
        cur.execute("DELETE FROM roll")
        cur.execute("DELETE FROM sqlite_sequence ")
        con.commit()
    con.close()

def status_db(command, user):
    con = sqlite3.connect('./status.db')
    cur = con.cursor()
    if command == 'get_status':
        cur.execute("select * from ability where user_id = ?", (user))
        status_p = cur.fetchone()
        con.commit()
    con.close()
    return status_p

def get_ccs(user_id):
    con = sqlite3.connect('./status.db')
    cur = con.cursor()
    if user_id == 'all':
        cur.execute('select name from character')
        cc_id = cur.fetchall()
    else:
        cur.execute('select name from character where user_id = ?', (user_id,))
        cc_id = cur.fetchone()
    con.close()
    return cc_id

def keep_ability(user_id):
    con = sqlite3.connect('./status.db')
    cur = con.cursor()
    sql = ('UPDATE ability SET str = ?,con = ?,pow = ?,dex= ?,app = ?,siz = ?,int = ?,edu = ?,'
            'san = ?,luck = ?,idea = ?,know = ?,hp = ?,mp = ?,sp = ?,ip = ?,dbs = ? '
            'where user_id = ?')
    data = (session['str'],session['con'],session['pow'],session['dex'],session['app'],session['siz'],session['int'],session['edu'],
            session['san'],session['luck'],session['idea'],session['know'],session['hp'],session['mp'],session['sp'],session['ip'],session['dbs'],user_id)
    cur.execute(sql, data)
    con.commit()
    con.close()

def delete_character(user_id):
    con = sqlite3.connect('./status.db')
    cur = con.cursor()
    cur.execute('UPDATE ability SET str = ?,con = ?,pow = ?,dex= ?,app = ?,siz = ?,int = ?,edu = ?,'
                'san = ?,luck = ?,idea = ?,know = ?,hp = ?,mp = ?,sp = ?,ip = ?,dbs = ? '
                'where user_id = ?',
                (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,user_id))
    cur.execute('UPDATE character SET name = ? where user_id = ?', ('新しい探索者', user_id))
    con.commit()
    con.close()

@app.route('/')
def route():
    return render_template('home.html')

@app.route('/move', methods=['POST'])
def move():
    move = request.form.get('move_site')
    if move == 'home':
        return render_template('home.html')
    elif move == 'dice':
        command_db('delete')
        command_dice = command_db('command')
        result_dice = command_db('result')
        return render_template('trpg.html', command_dice = command_dice, result_dice = result_dice)
    elif move == 'create':
        con = sqlite3.connect('./status.db')
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM character")
        count = cur.fetchone()[0]
        if count == 0:
            for id in range(1,4):
                cur.execute('insert into character(name, user_id) values(?,?)', ('新しい探索者', id))
                cur.execute('insert into ability(user_id) values(?)', (id,))
                con.commit()
        con.close()
        cc_id = get_ccs('all')
        return render_template('new_create.html', cc_id = cc_id)

@app.route('/home', methods=['POST'])
def home():
    session['result'] = ""
    session['total'] = ""
    session['dice_list'] = ""
    session['1d4'] = 0
    session['1d6'] = 0
    session['1d8'] = 0
    session['1d12'] = 0
    session['1d20'] = 0
    session['1d100'] = 0
    session['str'] = 0
    session['con'] = 0
    session['pow'] = 0
    session['dex'] = 0
    session['app'] = 0
    session['siz'] = 0
    session['int'] = 0
    session['edu'] = 0
    session['san'] = 0
    session['luck'] = 0
    session['idea'] = 0
    session['know'] = 0
    session['hp'] = 0
    session['mp'] = 0
    session['sp'] = 0
    session['ip'] = 0
    session['dbs'] = 0
    select  = request.form.get('select')
    if select == 'dice_home':
        command_db('delete')
        command_dice = command_db('command')
        result_dice = command_db('result')
        return render_template('trpg.html', command_dice = command_dice, result_dice = result_dice)
    elif select == 'create_home':
        con = sqlite3.connect('./status.db')
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM character")
        count = cur.fetchone()[0]
        if count == 0:
            for id in range(1,4):
                cur.execute('insert into character(name, user_id) values(?,?)', ('新しい探索者', id))
                cur.execute('insert into ability(user_id) values(?)', (id,))
                con.commit()
        con.close()
        cc_id = get_ccs('all')
        print(cc_id)
        return render_template('new_create.html', cc_id = cc_id)

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

def roll_cc(Quantity, Value, Constant):
    value = int(Value)
    quantity = int(Quantity)
    Constant = int(Constant)
    total = 0
    if value >= 1 and quantity >= 1:
        for roll in range(quantity):
            result = random.randint(1,value)
            total += result
        total += Constant
        return total

@app.route('/dice', methods=['GET', 'POST'])
def dice():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == '1d4':
            session['1d4'] += 1
        elif action == '1d6':
            session['1d6'] += 1
        elif action == '1d8':
            session['1d8'] += 1
        elif action == '1d12':
            session['1d12'] += 1
        elif action == '1d20':
            session['1d20'] += 1
        elif action == '1d100':
            session['1d100'] += 1
        else:
            d4 = session['1d4']
            d6 = session['1d6']
            d8 = session['1d8']
            d12 = session['1d12']
            d20 = session['1d20']
            d100 = session['1d100']
            value_get = request.form['value']
            value_form = value_get
            if d4 >= 1:
                d4 = str(d4)
                value_form = f'{value_form}+{d4}d4'
                session['1d4'] = 0
            if d6 >= 1:
                d6 = str(d6)
                value_form = f'{value_form}+{d6}d6'
                session['1d6'] = 0
            if d8 >= 1:
                d8 = str(d8)
                value_form = f'{value_form}+{d8}d8'
                session['1d8'] = 0
            if d12 >= 1:
                d12 = str(d12)
                value_form = f'{value_form}+{d12}d12'
                session['1d12'] = 0
            if d20 >= 1:
                d20 = str(d20)
                value_form = f'{value_form}+{d20}d20'
                session['1d20'] = 0
            if d100 >= 1:
                d100 = str(d100)
                value_form = f'{value_form}+{d100}d100'
                session['1d100'] = 0
            if value_get == '':
                value_form = value_form.replace('+', '', 1)
                value_form = value_form.replace(' ', '')
                value_list = value_form.split('+')
            else:
                value_form = value_form.replace(' ', '')
                value_list = value_form.split('+')
            session['total'] = 0
            roll_list = []
            for a in range(len(value_list)):
                value = value_list.pop(0)
                b = value.split('d')
                roll(b[0], b[1])
                roll_list.extend(session['dice_list'])
                session['result'] = (str(roll_list))
                roll_list = []
            session['dice_list'] = ""
            con = sqlite3.connect('./dice.db')
            cur = con.cursor()
            sql = f'insert into roll(command,result,result_list) values(?,?,?)'
            data = (value_form, session['total'], session['result'])
            cur.execute(sql, data)
            con.commit()
            con.close()
        command_dice = command_db('command')
        result_dice = command_db('result')
        return render_template('trpg.html', command_dice = command_dice, result_dice = result_dice)


#キャラクリ
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        user_id = session['user_id']
        roll = request.form.get('roll')
        if roll == 'str':
            session['str'] = roll_cc(3, 6, 0)
        elif roll == 'con':
            session['con'] = roll_cc(3, 6, 0)
        elif roll == 'pow':
            session['pow'] = roll_cc(3, 6, 0)
        elif roll == 'dex':
            session['dex'] = roll_cc(3, 6, 0)
        elif roll == 'app':
            session['app'] = roll_cc(3, 6, 0)
        elif roll == 'siz':
            session['siz'] = roll_cc(2, 6, 6)
        elif roll == 'int':
            session['int'] = roll_cc(2, 6, 6)
        elif roll == 'edu':
            session['edu'] = roll_cc(3, 6, 6)
        elif roll == 'all_random':
            session['str'] = roll_cc(3, 6, 0)
            session['con'] = roll_cc(3, 6, 0)
            session['pow'] = roll_cc(3, 6, 0)
            session['dex'] = roll_cc(3, 6, 0)
            session['app'] = roll_cc(3, 6, 0)
            session['siz'] = roll_cc(2, 6, 6)
            session['int'] = roll_cc(2, 6, 6)
            session['edu'] = roll_cc(3, 6, 6)
        elif roll == '保存':
            keep_ability(user_id)
        elif roll == '削除':
            delete_character(user_id)
            cc_id = get_ccs('all')
            return render_template('new_create.html', cc_id = cc_id)
        session['san'] = session['pow']*5
        session['luck'] = session['pow']*5
        session['idea'] = session['int']*5
        session['know'] = session['edu']*5
        if session['know'] >= 96 :
            session['know'] = 95
        session['hp'] = round((session['con']+session['siz'])/2)
        session['mp'] = session['pow']*1
        session['sp'] = session['edu']*20
        session['ip'] = session['int']*10
        session['dbs'] = session['str']+session['siz']
        cc_id = get_ccs(user_id)
        return render_template('create.html', cc_id = cc_id)

@app.route('/change', methods = ['POST'])
def change():
    change = request.form.get('cc_name')
    if change == '名前変更':
        user_id = session['user_id']
        name = request.form.get('text')
        con = sqlite3.connect('./status.db')
        cur = con.cursor()
        cur.execute('UPDATE character SET name = ? where user_id = ?', (name, user_id))
        con.commit()
        con.close()
    cc_id = get_ccs(user_id)
    return render_template('create.html', cc_id = cc_id)

@app.route('/select', methods = ['POST'])
def select():
    edit = request.form.get('edit')
    if edit == 'cc_1':
        cc_id = get_ccs('1')
        session['user_id'] = '1'
        status_p = status_db('get_status', '1')
    elif edit == 'cc_2':
        cc_id = get_ccs('2')
        session['user_id'] = '2'
        status_p = status_db('get_status', '2')
    elif edit == 'cc_3':
        cc_id = get_ccs('3')
        session['user_id'] = '3'
        status_p = status_db('get_status', '3')        
    session['str'] = status_p[1]
    session['con'] = status_p[2]
    session['pow'] = status_p[3]
    session['dex'] = status_p[4]
    session['app'] = status_p[5]
    session['siz'] = status_p[6]
    session['int'] = status_p[7]
    session['edu'] = status_p[8]
    session['san'] = status_p[9]
    session['luck'] = status_p[10]
    session['idea'] = status_p[11]
    session['know'] = status_p[12]
    session['hp'] = status_p[13]
    session['mp'] = status_p[14]
    session['sp'] = status_p[15]
    session['ip'] = status_p[16]
    session['dbs'] = status_p[17]
    return render_template('create.html', cc_id = cc_id)


if __name__ == '__main__':
    app.run(debug=True,port=8080)