from .models import User, get_posts
from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
    username = session.get('username')
    posts = get_posts(username)
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not User(username).register(password):
            flash('A user with that username already exists.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    tags = request.form['tags']
    text = request.form['text']

    if not title:
        flash('You must give your post a title.')
    elif not tags:
        flash('You must give your post at least one tag.')
    elif not text:
        flash('You must give your post a text body.')
    else:
        User(session['username']).add_post(title, tags, text)

    return redirect(url_for('index'))

@app.route('/rate_valid')
def rate_valid():
    username = session.get('username')
    
    if not username:
        flash('You must be logged in to rate_valid a post.')
        return redirect(url_for('login'))

    User(username).rate_valid(request.args.get('post_id', 0, type=int),request.args.get('rating', 0, type=int))

    return redirect(request.referrer)
    
@app.route('/rate_like')
def rate_like():
    username = session.get('username')
    
    if not username:
        flash('You must be logged in to rate_like a post.')
        return redirect(url_for('login'))

    User(username).rate_like(request.args.get('post_id', 0, type=int),request.args.get('rating', 0, type=int))

    return redirect(request.referrer)
    
@app.route('/rate_authenticity')
def rate_authenticity():
    username = session.get('username')
    
    if not username:
        flash('You must be logged in to rate_authenticity a post.')
        return redirect(url_for('login'))

    User(username).rate_authenticity(request.args.get('post_id', 0, type=int),request.args.get('rating', 0, type=int))

    return redirect(request.referrer)

@app.route('/rate_trust')
def rate_trust():
    username = session.get('username')
    
    if not username:
        flash('You must be logged in to rate_trust a post.')
        return redirect(url_for('login'))

    User(username).rate_trust(request.args.get('post_id', 0, type=int),request.args.get('rating', 0, type=int))

    return redirect(request.referrer)


@app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username

    user_being_viewed = User(user_being_viewed_username)
    posts = user_being_viewed.get_recent_posts()

    if logged_in_username:
        logged_in_user = User(logged_in_username)

    return render_template(
        'profile.html',
        username=username,
        posts=posts
    )
