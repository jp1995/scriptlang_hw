from flask_mysqldb import MySQL
from flask import Flask, render_template, request
import os


app = Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST'] = os.environ.get('SQLHOST')
app.config['MYSQL_USER'] = os.environ.get('SQLUSER')
app.config['MYSQL_PASSWORD'] = os.environ.get('SQLPASSWORD')
app.config['MYSQL_DB'] = os.environ.get('SQLDB')

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def Index():
    if request.method == 'POST':
        data = request.form
        code = data['code']
        user = data['user']
        email = data['email']
        status = data['status']

        c = mysql.connection.cursor()
        c.execute('INSERT INTO users(code, username, email, status) VALUES(%s, %s, %s, %s)',
                  (code, user, email, status))
        mysql.connection.commit()
        c.close()

    c = mysql.connection.cursor()
    c.execute('SELECT code, username, email, status FROM users')
    fetch = c.fetchall()
    c.close()

    return render_template('index.html', data=fetch)


def placeholder_test():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)
