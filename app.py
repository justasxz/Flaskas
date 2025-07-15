# from flask import Flask, render_template, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return f'<User {self.username}>'

# @app.route('/') # dekoratorius
# def home():
#     users = User.query.all()
#     return render_template('index.html', naudotojai=users)

# @app.route('/manoPuslapis') # dekoratorius
# def antrelis():
#     return f"{url_for('vardai')} - tai mano puslapis!"


# @app.route('/sukint/<kintamas>') # dekoratorius
# def kintas(kintamas):
#     return f"Sveiki atvykę į mano puslapį! Kintamasis:  {kintamas}"

# @app.route('/varduVaizd') # dekoratorius
# def vardai():
#     vardeliai = ['Jonas', 'Petras', 'Ona', 'Marytė']
#     # return render_template('varduVaizd.html', vardai=['Jonas', 'Petras', 'Ona', 'Marytė'] )
#     return render_template('varduVaizd.html', vardai=vardeliai, kintas="Dar viena perduodama reiksme" )


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase

# --- SQLAlchemy 2.x Declarative Base ---
class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Tell Flask-SQLAlchemy to use our Base (requires Flask-SQLAlchemy ≥ 3.0)
db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)

# --- Models ---
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# --- Routes ---

@app.route('/')
def home():
    # SQLAlchemy 2.0 querying style
    users = db.session.scalars(select(User)).all()
    return render_template('index.html', naudotojai=users)

@app.route('/manoPuslapis')
def antrelis():
    return f"{url_for('vardai')} - tai mano puslapis!"

@app.route('/sukint/<kintamas>')
def kintas(kintamas):
    return f"Sveiki atvykę į mano puslapį! Kintamasis:  {kintamas}"

@app.route('/varduVaizd')
def vardai():
    vardeliai = ['Jonas', 'Petras', 'Ona', 'Marytė']
    return render_template(
        'varduVaizd.html',
        vardai=vardeliai,
        kintas="Dar viena perduodama reiksme"
    )

# --- New endpoint to create a User ---
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'username and email required'}), 400

    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()

    return (
        jsonify({'id': user.id, 'username': user.username, 'email': user.email}),
        201
    )

if __name__ == '__main__':
    app.run(debug=True)
