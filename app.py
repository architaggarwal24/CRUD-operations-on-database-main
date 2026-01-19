from flask import Flask, render_template, request, redirect, url_for, session
from db_helper import DBHelper

app = Flask(__name__)
app.secret_key = "super-secret-key-change-this"
db = DBHelper()

@app.route('/')
def home():
    users = db.fetch_all()
    return render_template('index.html', users=users)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        userName = request.form.get('userName')
        phone = request.form.get('phone')

        try:
            db.insert_user(userName, phone)
            session['toast'] = ('success', 'User added successfully!')
        except Exception:
            session['toast'] = ('error', 'Database error occurred!')

        return redirect('/')

    return render_template('insert.html')



@app.route('/update/<int:userId>', methods=['GET', 'POST'])
def update(userId):
    if request.method == 'POST':
        newName = request.form['userName']
        newPhone = request.form['phone']
        db.update_user(userId, newName, newPhone)
        return redirect(url_for('home'))
    return render_template('update.html', userId=userId)

@app.route('/delete/<int:userId>')
def delete(userId):
    db.delete_user(userId)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
