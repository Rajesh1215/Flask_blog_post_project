from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet


app = Flask(__name__)
#key 
app.secret_key = 'qwertyuixcvbnm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/two_database'

key =  Fernet.generate_key()
fernet = Fernet(key)

db = SQLAlchemy(app)

class Users(db.Model):
    email = db.Column(db.String(25), primary_key = True, nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    rePassword = db.Column(db.String(50), nullable=False)
    phoneNo =db.Column(db.Integer, nullable=False)


class Blogs(db.Model):
    s_no = db.Column(db.Integer, nullable = False, primary_key = True)
    title = db.Column(db.String(20), nullable = False)
    img1 = db.Column(db.String(30), nullable = False)
    img2 = db.Column(db.String(30), nullable = False)
    img1sub =db.Column(db.String(50), nullable = False)
    img2sub=  db.Column(db.String(50), nullable = False)
    author_name = db.Column(db.String(30), nullable = False)
    date_time = db.Column(db.DateTime, nullable = False)
    content = db.Column(db.String(300), nullable = False)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home/<email>')
def home(email):
    # print(email)
    if session['username'] == email:
        # print(fernet.encrypt(email.encode()))
        blog_items = Blogs.query.all()
        return render_template('index.html', blog_items = blog_items)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signuping', methods=['GET', 'POST'])
def signIn():
    # if session['username'] != None:
    if(request.method == 'POST'):
        email = fernet.encrypt(request.form.get('email').encode())
        userid = fernet.encrypt(request.form.get('userid').encode())
        password = fernet.encrypt(request.form.get('password').encode())
        repassword = fernet.encrypt(request.form.get('re_password').encode())
        phoneno = fernet.encrypt(request.form.get('phoneno').encode())
        entry = Users(email = email, user_id = userid, password = password , rePassword = repassword, phoneNo = phoneno)
        db.session.add(entry)
        db.session.commit()
        session['username'] = email
        return redirect(url_for('home', email = email))


@app.route('/login_auth', methods=['GET', 'POST'])
def login_auth():
    if request.method == 'POST':
        email  = request.form.get('email')
        password  = request.form.get('password')
        # print("email from html form "+email)
        check = Users.query.filter_by(email = email).first()
        if(check is None):
            return "Invalid input"
        else:
            if(check.password == password):
                session['username'] = email
                return redirect(url_for('home', email=email))
    return redirect(url_for('login'))

@app.route('/signup')
def sign():
    return render_template('signup.html')


@app.route('/blog-content')
def blog_content():
    
    return render_template('blogContent.html')

@app.route('/create-blog')
def create_blog():
    return render_template("blogForm.html")

if __name__ == "__main__":
    app.run()


app.run(debug=True)
#.\env_name\Scripts\activate