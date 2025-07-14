from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') # dekoratorius
def home():
    return render_template('index.html')

@app.route('/manoPuslapis') # dekoratorius
def antrelis():
    return "antras puslapis"


@app.route('/sukint/<kintamas>') # dekoratorius
def kintas(kintamas):
    return f"Sveiki atvykę į mano puslapį! Kintamasis:  {kintamas}"


if __name__ == '__main__':
    app.run(debug=True)