from flask import Flask, render_template, url_for, sessions, request
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer, SignatureExpired

app = Flask(__name__)
# app.config.from_pyfile('config.cfg')
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeSerializer('secretthistime!')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('mail.html')
    email = request.form['email']
    token = s.dumps(email, salt='email-confirm')
    msg = Message(subject='Test Mail', sender='earvinbaraka@gmail.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)

    msg.body = render_template('newsletters.html', token=token, link=link)
    # 'Your link is {}'.format(link)

    mail.send(msg)

    return render_template('mailsent.html', token=token,link=link )
    # return '<h1>The email you entered is {}. The token is {}</h1> '.format(email, token)
    # return render_template('mail.html')


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', )
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
     # return '<h1>The token works!</h1>'
    return '<a href="https://www.google.com"><h1>Click here</h1></a>'

if __name__ == '__main__':
    app.run(debug=True)
