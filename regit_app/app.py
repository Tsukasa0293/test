from flask import Flask, redirect, render_template, request, session, url_for
import random, re

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

#初期化
def Initialization():
    session['result'] = ""
    session['total'] = ""
    session['dice_list'] = ""
    session['text_dice'] = ""
    session['quantity_4'] = 0
    session['quantity_6'] = 0
    session['quantity_8'] = 0
    session['quantity_12'] = 0
    session['quantity_20'] = 0
    session['hand_dl'] = ""
    session['total_dl'] = ""
    session['hand_pl'] = ""
    session['total_pl'] = ""
    session['hit'] = ""
    session['bust_pl'] = ""
    session['busst_dl'] = ""
    session['stand'] = ""
    session['card_list'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                            101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
                            201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213,
                            301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313]


# Dice
@app.route('/')
def form():
    Initialization()
    return render_template('index.html')

@app.route('/select_dice', methods=['GET'])
def select_dice():
    return render_template('dice.html')

@app.route('/select_bj', methods=['GET'])
def select_bj():
    return render_template('blackjack.html')

@app.route('/dice', methods=['GET', 'POST'])
def dice():
    if request.method == 'POST' and request.form['submit']:
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
    return render_template('dice.html')

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


@app.route('/clicked_4', methods=['GET', 'POST'])
def clicked_4():
    session['activ'] = 1
    session['quantity_4'] += 1
    return render_template('dice.html')

@app.route('/clicked_6', methods=['GET', 'POST'])
def clicked_6():
    total = 0
    session['result'] = ""
    result = random.randint(1,6)
    total += result
    session['total'] = total
    return render_template('dice.html')

@app.route('/clicked_8', methods=['GET', 'POST'])
def clicked_8():
    total = 0
    session['result'] = ""
    result = random.randint(1,8)
    total += result
    session['total'] = total
    return render_template('dice.html')

@app.route('/clicked_12', methods=['GET', 'POST'])
def clicked_12():
    total = 0
    session['result'] = ""
    result = random.randint(1,12)
    total += result
    session['total'] = total
    return render_template('dice.html')

@app.route('/clicked_20', methods=['GET', 'POST'])
def clicked_20():
    total = 0
    session['result'] = ""
    result = random.randint(1,20)
    total += result
    session['total'] = total
    return render_template('dice.html')


# BlackJack
def draw(value, name):
    card_list = []
    card_list.extend(session['card_list'])
    hand_pl_list = []
    hand_pl_list.extend(session['hand_pl'])
    hand_dl_list = []
    hand_dl_list.extend(session['hand_dl'])
    mark_list = ['♡', '♤', '♢', '♧']
    total_pl = session['total_pl']
    total_dl = session['total_dl']
    total = 0
    for draw in range(value):
        if total_pl or total_dl <= 21:
            hand = card_list.pop()
            if hand < 14:
                mark = mark_list[0]
                if hand > 10:
                    total += 10
                else :
                    total += hand
            elif 14 < hand < 114:
                mark = mark_list[1]
                if hand > 110:
                    total += 10
                else :
                    total += hand - 100
                hand = hand - 100
            elif 114 < hand < 214:
                mark = mark_list[2]
                if hand > 210:
                    total += 10
                else :
                    total += hand - 200
                hand = hand - 200
            else :
                mark = mark_list[3]
                if hand > 310:
                    total += 10
                else :
                    total += hand - 300
                hand = hand - 300
            card = f"{mark}{hand}"
            if name == 'pl':
                total_pl += total
                hand_pl_list.append(card)
                session['total_pl'] = total_pl
                session['hand_pl'] = hand_pl_list
            elif name == 'dl':
                total_dl += total
                hand_dl_list.append(card)
                session['total_dl'] = total_dl
                session['hand_dl'] = hand_dl_list
            session['card_list'] = card_list
        else:
            session['hit'] = ""
            session['stand'] = ""
            if total_pl > 21:
                session['bust_pl'] = "BUST"
            elif total_dl > 21:
                session['bust_dl'] = 'BUST'

def bj(command):
    if command == 'command_start':
        card_list = []
        card_list.extend(session['card_list'])
        mark_list = ['♡', '♤', '♢', '♧']
        hand_pl_list = []
        hand_dl_list = []
        total_pl = 0
        total_dl = 0
        random.shuffle(card_list)
        for state in range(2):
            hand = card_list.pop()
            if hand < 14:
                mark = mark_list[0]
                if hand > 10:
                    total_pl += 10
                else :
                    total_pl += hand
            elif 14 < hand < 114:
                mark = mark_list[1]
                if hand > 110:
                    total_pl += 10
                else :
                    total_pl += hand - 100
                hand = hand - 100
            elif 114 < hand < 214:
                mark = mark_list[2]
                if hand > 210:
                    total_pl += 10
                else :
                    total_pl += hand - 200
                hand = hand - 200
            else :
                mark = mark_list[3]
                if hand > 310:
                    total_pl += 10
                else :
                    total_pl += hand - 300
                hand = hand - 300
            card = f"{mark}{hand}"
            hand_pl_list.append(card)
            session['hand_pl'] = hand_pl_list
        for a in range(1):
            hand_dl = card_list.pop()
            if hand_dl < 14:
                mark = mark_list[0]
                if hand_dl > 10:
                    total_dl += 10
                else :
                    total_dl += hand_dl
            elif 14 < hand_dl < 114:
                mark = mark_list[1]
                if hand_dl > 110:
                    total_dl += 10
                else :
                    total_dl += hand_dl - 100
                hand_dl = hand_dl - 100
            elif 114 < hand_dl < 214:
                mark = mark_list[2]
                if hand_dl > 210:
                    total_dl += 10
                else :
                    total_dl += hand_dl - 200
                hand_dl = hand_dl - 200
            else :
                mark = mark_list[3]
                if hand_dl > 310:
                    total_dl += 10
                else :
                    total_dl += hand_dl - 300
                hand_dl = hand_dl - 300
            card = f"{mark}{hand_dl}"
            hand_dl_list.append(card)
            hand_dl_list.append("?")
            session['hand_dl'] = hand_dl_list
            session['total_dl'] = total_dl
            session['total_pl'] = total_pl
            session['card_list'] = card_list
            session['hit'] = 'HIT'
            session['stand'] = "STAND"


@app.route('/start', methods=['GET'])
def start():
    bj('command_start')
    return render_template('blackjack.html')

@app.route('/hit', methods=['GET'])
def hit():
    draw(1, 'pl')
    return render_template('blackjack.html')

@app.route('/stand')
def stand():
    hand_dl_list = []
    hand_dl_list.append(session['hand_dl_list'])
    hand_dl_list.remove('?')
    total_dl = session['total_dl']
    card_list = []
    card_list.extend(session['card_list'])
    mark_list = ['♡', '♤', '♢', '♧']
    while total_dl < 17:
        hand_dl = card_list.pop()
        if hand_dl < 14:
            mark = mark_list[0]
            if hand_dl > 10:
                total_dl += 10
            else :
                total_dl += hand_dl
        elif 14 < hand_dl < 114:
            mark = mark_list[1]
            if hand_dl > 110:
                total_dl += 10
            else :
                total_dl += hand_dl - 100
            hand_dl = hand_dl - 100
        elif 114 < hand_dl < 214:
            mark = mark_list[2]
            if hand_dl > 210:
                total_dl += 10
            else :
                total_dl += hand_dl - 200
            hand_dl = hand_dl - 200
        else :
            mark = mark_list[3]
            if hand_dl > 310:
                total_dl += 10
            else :
                total_dl += hand_dl - 300
            hand_dl = hand_dl - 300
        card = f"{mark}{hand_dl}"
        hand_dl_list.append(card)
    return render_template('blakjack.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080)
