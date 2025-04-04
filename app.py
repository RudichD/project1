from flask import Flask, request, render_template, redirect, url_for, abort
from database import Session, User, Answer
from config import Config
from datetime import datetime
import hashlib

# Валидация переменных окружения
Config.validate()

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

@app.route('/submit-test', methods=['POST'])
def submit_test():
    session = Session()
    vk_user_id = request.args.get('vk_user_id')
    db_user = session.query(User).filter_by(vk_id=vk_user_id).first()

    if not db_user:
        return redirect(url_for('consent'))  # Если пользователь не найден, перенаправьте на consent

    # Проверка наличия параметров
    color = request.form.get('color')
    description = request.form.get('description')

    if not color or not description:  # Проверка на наличие значений
        return abort(400)  # Возврат 400 Bad Request, если параметры отсутствуют

    answer = Answer(
        user_id=db_user.id,
        day=db_user.current_day,
        color=color,
        description=description,
        cycle=db_user.cycle
    )
    session.add(answer)

    # Обновление данных пользователя
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