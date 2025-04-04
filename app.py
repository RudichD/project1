from flask import Flask, request, render_template, redirect, url_for, abort
from vk_api import VkApi
from database import Session, User, Answer
from datetime import datetime, timedelta
import hashlib
import os
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY


def verify_vk_signature():
    params = request.args.to_dict()
    sign = params.pop('sign', '')
    ordered = sorted(params.items())
    string = ''.join([f"{k}={v}" for k, v in ordered])
    calculated = hashlib.md5((string + Config.SERVICE_KEY).encode()).hexdigest()
    return sign == calculated


@app.before_request
def check_auth():
    if not verify_vk_signature():
        abort(403)


@app.route('/')
def index():
    session = Session()
    vk_user_id = request.args.get('vk_user_id')

    db_user = session.query(User).filter_by(vk_id=vk_user_id).first()

    if not db_user:
        return redirect(url_for('consent'))

    if db_user.current_day > 30:
        return render_template('cycle_complete.html')

    return redirect(url_for('daily_test'))


@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        session = Session()
        vk_user_id = request.args.get('vk_user_id')

        db_user = User(
            vk_id=int(vk_user_id),
            consent=True,
            start_date=datetime.now(),
            current_day=1
        )
        session.add(db_user)
        session.commit()
        return redirect(url_for('daily_test'))

    return render_template('consent.html')


@app.route('/daily-test')
def daily_test():
    session = Session()
    vk_user_id = request.args.get('vk_user_id')
    db_user = session.query(User).filter_by(vk_id=vk_user_id).first()

    if (datetime.now() - db_user.start_date).days >= 30:
        return render_template('cycle_complete.html')

    return render_template('test.html', day=db_user.current_day)


@app.route('/submit-test', methods=['POST'])
def submit_test():
    session = Session()
    vk_user_id = request.args.get('vk_user_id')
    db_user = session.query(User).filter_by(vk_id=vk_user_id).first()

    answer = Answer(
        user_id=db_user.id,
        day=db_user.current_day,
        color=request.form['color'],
        description=request.form['description'],
        cycle=db_user.cycle
    )
    session.add(answer)

    if db_user.current_day < 30:
        db_user.current_day += 1
    else:
        db_user.cycle += 1
        db_user.current_day = 1
        db_user.start_date = datetime.now()

    session.commit()
    return redirect(url_for('daily_test'))


if __name__ == '__main__':
    app.run(debug=False)