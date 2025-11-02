# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from forms import RegistrationForm, LoginForm
from models import db, User, Book, Room, Event, Booking
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken! Try another one')
            return render_template('register.html', form=form)
        
        hashed = generate_password_hash(form.password.data)
        user = User(username=form.username.data,
                    password_hash=hashed,
                    role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Wrong username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ─── LIBRARIAN ONLY: DASHBOARD ───
@app.route('/librarian')
@login_required
def librarian_dashboard():
    if not current_user.is_librarian():
        flash('Only librarians can access this page.')
        return redirect(url_for('index'))

    books = Book.query.all()
    rooms = Room.query.all()
    events = Event.query.all()
    return render_template('librarian.html', books=books, rooms=rooms, events=events)

@app.route('/librarian/add_book', methods=['POST'])
@login_required
def add_book():
    if not current_user.is_librarian(): return redirect(url_for('index'))
    title = request.form['title']
    author = request.form['author']
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    flash('Book added!')
    return redirect(url_for('librarian_dashboard'))

@app.route('/librarian/delete_book/<int:id>')
@login_required
def delete_book(id):
    if not current_user.is_librarian(): return redirect(url_for('index'))
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book removed.')
    return redirect(url_for('librarian_dashboard'))

# Repeat for Room & Event if you want – same pattern

# ─── READER: SEARCH & BOOK (same as before, simplified) ───
@app.route('/search')
@login_required
def search():
    q = request.args.get('q', '')
    type = request.args.get('type', 'book')
    results = []
    if type == 'book':
        results = Book.query.filter(Book.title.ilike(f'%{q}%') | Book.author.ilike(f'%{q}%')).all()
    return render_template('search.html', results=results, q=q)

@app.route('/book/<int:id>')
@login_required
def book_item(id):
    # BLOCK LIBRARIANS FROM BOOKING
    if current_user.is_librarian():
        flash('Librarians cannot book items. Only readers can!')
        return redirect(url_for('search'))

    book = Book.query.get_or_404(id)
    if not book.available:
        flash('Sorry, this book is already booked.')
        return redirect(url_for('search'))

    # Create booking
    booking = Booking(
        user_id=current_user.id,
        item_id=book.id,
        item_type='book',
        end_time=datetime.utcnow() + timedelta(hours=2)
    )
    book.available = False
    db.session.add(booking)
    db.session.commit()

    flash('Book reserved for 2 hours! Check "My Bookings"')
    return redirect(url_for('history'))

@app.route('/history')
@login_required
def history():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', bookings=bookings)

@app.route('/cancel/<int:bid>')
@login_required
def cancel(bid):
    b = Booking.query.get_or_404(bid)
    if b.user_id != current_user.id:
        flash('Not your booking.')
        return redirect(url_for('history'))
    if b.item_type == 'book':
        book = Book.query.get(b.item_id)
        book.available = True
    db.session.delete(b)
    db.session.commit()
    flash('Booking cancelled.')
    return redirect(url_for('history'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a default librarian for testing
        if not User.query.filter_by(username='admin').first():
            hashed = generate_password_hash('admin123')
            admin = User(username='admin', password_hash=hashed, role='librarian')
            db.session.add(admin)
            db.session.commit()
            print("Created default librarian → username: admin | password: admin123")
    app.run(debug=True)