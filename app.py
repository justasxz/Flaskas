from flask import Flask, render_template, url_for, request, jsonify, redirect, abort
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

# @app.route('/naujasNaudKurti')
# def sukurti_naudotoja_get():
#     return render_template('naujas_naudotojas.html')

@app.route('/naujasNaud', methods=['POST', 'GET'])
def sukurti_naudotoja():
    if request.method == 'GET':
        return render_template('naujas_naudotojas.html')
    elif request.method == 'POST':
        vardas = request.form['Vardas']
        emailas = request.form['Pastas']
        naud = User(username = vardas, email = emailas)
        db.session.add(naud)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        abort(405)

# edit user

@app.route('/atnaujinti/<user_id>')
def sukurti_naudotoja_get(user_id):
    user = db.session.get(User, user_id)
    return render_template('update_user.html', user=user)


@app.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id: int):
    """
    Update an existing User's username and/or email.
    Expects JSON body with 'username' and/or 'email'.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    # Lookup using SQLAlchemy 2.0 style session.get
    user = db.session.get(User, user_id)  # :contentReference[oaicite:0]{index=0}
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Only update the fields that were provided
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    try:
        db.session.commit()  # :contentReference[oaicite:1]{index=1}
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user', 'message': str(e)}), 500

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 200



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
