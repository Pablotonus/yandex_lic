import os

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, current_user

from data import db_session
from data.clubs import Club
from data.enrollments import Enrollment
from data.users import User
from forms.user import LoginForm, RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'clubs_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


CLUB_DETAILS = {
    1: {
        'status': 'Набор открыт',
        'duration': '2-3 месяца',
        'level': '5-8 классы',
        'long_description': 'На занятиях участники постепенно переходят от простых деталей к рабочим моделям: собирают механизмы, проверяют датчики и учатся исправлять ошибки в конструкции.',
        'learn': [
            'собирать простые механизмы и понимать, как они двигаются',
            'подключать датчики и проверять их работу',
            'работать в команде над небольшим техническим проектом'
        ],
        'result': 'К концу курса участник соберёт учебного робота и покажет небольшой проект.',
        'audience': 'Подойдёт тем, кто любит конструкторы, технику и практические задачи.',
        'bring': 'Тетрадь, ручка и желание спокойно разбираться, почему робот поехал не туда.'
    },
    2: {
        'status': 'Популярный кружок',
        'duration': '2 месяца',
        'level': '6-9 классы',
        'long_description': 'Кружок помогает разобраться, как устроены сайты: страницы, формы, шаблоны, маршруты и простая работа с данными.',
        'learn': [
            'создавать страницы сайта на HTML и подключать стили',
            'делать формы регистрации, входа и отправки данных',
            'понимать, как Flask связывает адрес страницы и функцию'
        ],
        'result': 'В конце получится небольшой сайт с несколькими страницами и личным кабинетом.',
        'audience': 'Подойдёт тем, кто хочет попробовать программирование на реальном проекте.',
        'bring': 'Ноутбук, если есть возможность, или флешку для сохранения работы.'
    },
    3: {
        'status': 'Есть свободные места',
        'duration': '1-2 месяца',
        'level': '4-9 классы',
        'long_description': 'На занятиях разбираются партии, типовые ловушки, простые комбинации и спокойная стратегия игры.',
        'learn': [
            'видеть угрозы соперника на несколько ходов вперёд',
            'решать тактические задачи и находить сильные ходы',
            'увереннее играть партии с контролем времени'
        ],
        'result': 'Участник сможет сыграть полноценную партию и попробовать себя в школьном турнире.',
        'audience': 'Подойдёт и новичкам, и тем, кто уже знает правила, но хочет играть сильнее.',
        'bring': 'Ничего особенного: доски и фигуры будут на занятиях.'
    },
    4: {
        'status': 'Творческая группа',
        'duration': '2 месяца',
        'level': '5-9 классы',
        'long_description': 'Кружок даёт спокойную практику рисунка: от быстрых набросков до законченных работ с цветом и композицией.',
        'learn': [
            'делать наброски и передавать форму предметов',
            'подбирать цвета и строить композицию',
            'аккуратно доводить работу до законченного вида'
        ],
        'result': 'К концу курса у участника будет несколько готовых работ для мини-портфолио.',
        'audience': 'Подойдёт тем, кто любит рисовать или хочет начать без страха чистого листа.',
        'bring': 'Альбом, простой карандаш, ластик и любимые цветные материалы.'
    },
    5: {
        'status': 'Разговорная практика',
        'duration': '2-3 месяца',
        'level': '5-8 классы',
        'long_description': 'Занятия построены вокруг живых тем: школа, увлечения, путешествия, друзья и короткие диалоги.',
        'learn': [
            'говорить о себе и своих интересах простыми фразами',
            'лучше понимать короткие тексты и задания',
            'пополнять словарный запас без скучной зубрёжки'
        ],
        'result': 'Участник сможет увереннее вести короткий диалог и рассказать о себе на английском.',
        'audience': 'Подойдёт тем, кто хочет больше говорить, а не только выполнять упражнения.',
        'bring': 'Тетрадь, ручка и словарь или приложение для новых слов.'
    }
}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


def add_start_clubs():
    db_sess = db_session.create_session()
    if db_sess.query(Club).first():
        return

    clubs = [
        Club(
            title='Робототехника',
            description='Сборка простых роботов, работа с датчиками и первые соревнования.',
            schedule='Понедельник и среда, 16:00',
            teacher='Иван Петрович',
            classroom='Кабинет 21'
        ),
        Club(
            title='Веб-разработка',
            description='Создание сайтов на Flask, работа с HTML-страницами и формами.',
            schedule='Вторник и четверг, 15:30',
            teacher='Анна Сергеевна',
            classroom='Кабинет 14'
        ),
        Club(
            title='Шахматы',
            description='Тактика, дебюты, решение задач и дружеские турниры.',
            schedule='Пятница, 16:30',
            teacher='Олег Викторович',
            classroom='Кабинет 8'
        ),
        Club(
            title='Рисование',
            description='Основы композиции, цвет, наброски и небольшие творческие проекты.',
            schedule='Среда, 17:00',
            teacher='Мария Андреевна',
            classroom='Кабинет 5'
        ),
        Club(
            title='Английский язык',
            description='Разговорная практика, новые слова и короткие сценки на английском.',
            schedule='Вторник, 17:00',
            teacher='Елена Павловна',
            classroom='Кабинет 12'
        )
    ]

    for club in clubs:
        db_sess.add(club)
    db_sess.commit()


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    clubs = db_sess.query(Club).all()
    return render_template(
        'index.html',
        title='Кружки школы',
        clubs=clubs,
        club_details=CLUB_DETAILS
    )


@app.route('/club/<int:club_id>')
def club_page(club_id):
    db_sess = db_session.create_session()
    club = db_sess.get(Club, club_id)
    if not club:
        return redirect('/')

    enrolled = False
    if current_user.is_authenticated:
        enrolled = db_sess.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.club_id == club.id
        ).first() is not None

    participants = db_sess.query(User).join(
        Enrollment,
        User.id == Enrollment.user_id
    ).filter(Enrollment.club_id == club.id).all()

    return render_template(
        'club.html',
        title=club.title,
        club=club,
        enrolled=enrolled,
        participants=participants,
        details=CLUB_DETAILS.get(club.id)
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message='Пароли не совпадают'
            )

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message='Такой участник уже есть'
            )

        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/profile')

        return render_template(
            'login.html',
            title='Вход',
            form=form,
            message='Неправильная почта или пароль'
        )

    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/')


@app.route('/enroll/<int:club_id>')
def enroll(club_id):
    if not current_user.is_authenticated:
        return redirect('/login')

    db_sess = db_session.create_session()
    club = db_sess.get(Club, club_id)
    if not club:
        return redirect('/')

    enrollment = db_sess.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.club_id == club.id
    ).first()

    if not enrollment:
        enrollment = Enrollment(user_id=current_user.id, club_id=club.id)
        db_sess.add(enrollment)
        db_sess.commit()

    return render_template('success.html', title='Заявка принята', club=club)


@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect('/login')

    db_sess = db_session.create_session()
    enrollments = db_sess.query(Enrollment).filter(
        Enrollment.user_id == current_user.id
    ).all()

    return render_template(
        'profile.html',
        title='Личный кабинет',
        enrollments=enrollments
    )


def main():
    db_session.global_init('db/clubs.db')
    add_start_clubs()
    port = int(os.environ.get('PORT', 8080))
    app.run(port=port, host='0.0.0.0')


if __name__ == '__main__':
    main()
