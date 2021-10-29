from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import json
from flask_mail import Mail
import os
from werkzeug.utils import secure_filename

local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)

app.config['SECRET_KEY'] = ''
app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'bb2c94fd6e7156'
app.config['MYSQL_PASSWORD'] = '99b4698a'
app.config['MYSQL_DB'] = 'ideaboat'


mysql = MySQL(app)
print(mysql)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail = Mail(app)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/Services')
def services():
    return render_template('Services.html')


@app.route('/Portfolio')
def portfolio():
    return render_template('Portfolio.html')


@app.route('/Blog')
def blog():
    return render_template('Blog.html')


@app.route('/Blog1')
def blog1():
    return render_template('Blog1.html')


@app.route('/Blog2')
def blog2():
    return render_template('Blog2.html')


@app.route('/Blog3')
def blog3():
    return render_template('Blog3.html')


@app.route('/Contact', methods=['GET', 'POST'])
def contact():

    if (request.method == 'POST'):
        cur = mysql.connection.cursor()
        name = request.form.get('name', False)  # Full Name
        email = request.form.get('email1', False)  # Father's Name
        number = request.form.get('number', False)  # Mother's Name
        message = request.form.get('message', False)  # His grade/class

        sequence = (name, email, number, message)
        print(sequence)
        formula = "INSERT INTO contact (id, name, email, number, message) VALUES ('',%s,%s,%s,%s)"
        print(formula)
        cur.execute(formula, sequence)
        mysql.connection.commit()

        mail.send_message('New message from ' + name,sender = email,recipients = [params['gmail-user']],
                          body = message)
    return render_template('Contact.html')
    # return cur

@app.route('/CompleteEdit',methods=['GET','POST'])
def changePage():
    if request.method == "POST":
        return render_template('showDetails.html')

@app.route('/ContactDisplay',methods = ['GET','POST'])
def show():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        id = str(request.form.get('id'))
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('number')
        message = request.form.get('message')
        sequence = (id, name, email, str(number), message, id)

        formula = "UPDATE contact SET id = %s ,name = %s, email=%s, number=%s, message=%s WHERE id = %s"
        cur.execute(formula, sequence)
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM contact""")
        user = cur.fetchall()
        print(user)
        # return str(user[1])
        return render_template('showDetails.html', params=params, users=user)

    else:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM contact""")
        user = cur.fetchall()
        print(user)
        # return str(user[1])
        return render_template('showDetails.html',params=params,users = user)

@app.route('/Edit/<int:id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM contact WHERE id = %s""",(id,))
    user = cur.fetchone()
    return render_template('edit.html',user=user)

@app.route('/Delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM contact WHERE id = %s""",(id,))
    mysql.connection.commit()
    return "<html> <script> window.location = '/ContactDisplay' </script> </html>"

@app.route('/Upload',methods = ['GET','POST'])
def upload():
    if request.method=='POST':
        file = request.files['file1']
        file.save(os.path.join(params['upload_folder'],secure_filename(file.filename)))
        return "<html> <script> window.location = '/ContactDisplay' </script> </html>"

@app.route('/uploadFile')
def uploadFile():
    return render_template('fileupload.html')


if __name__ == '__main__':
    app.run()
