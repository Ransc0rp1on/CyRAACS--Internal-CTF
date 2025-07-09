from flask import Flask, request, session, redirect, url_for, render_template
import os

app = Flask(__name__)
app.secret_key = 'superctfsecret'
UPLOAD_FOLDER = 'app/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = file.filename
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            return f"File uploaded to /{path}. Visit /dev-notes"
    return render_template("upload.html")

@app.route('/dev-notes')
def dev_notes():
    return render_template("dev_notes.html")

@app.route('/profile/<uid>')
def profile(uid):
    if uid == '2':
        return render_template("profile2.html")
    return render_template("profile_generic.html")

@app.route('/reset')
def reset():
    token = request.args.get('token')
    if token == 'reset_token_user2_abc123':
        session['user'] = 'admin'
        return redirect('/admin')
    return 'Invalid token'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('user') != 'admin':
        return 'Unauthorized'
    if request.method == 'POST':
        query = request.form.get('search')
        if "'" in query or '1=1' in query:
            return render_template("sql_dump.html")
    return render_template("admin_search.html")

@app.route('/crack')
def crack():
    return render_template("crack.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            return f"Shell uploaded to /{path}. Visit /billing"
    return render_template("upload_shell.html")

@app.route('/billing')
def billing():
    return render_template("billing.html")

@app.route('/backup')
def backup():
    return render_template("backup.html")

@app.route('/ssrf')
def ssrf():
    url = request.args.get('url')
    if url == 'http://localhost/internal':
        return render_template("ssrf_success.html")
    return 'Try harder!'

@app.route('/logs')
def logs():
    return render_template("logs.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
