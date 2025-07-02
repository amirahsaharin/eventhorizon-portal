from flask import Flask, render_template, request, redirect, session
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from models import db, User, Event, Registration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = SECRET_KEY

db.init_app(app)

@app.route('/')
def home():
    events = Event.query.all()
    return render_template('event.html', events=events)

@app.route('/models')
def create_models():
    try:
        with app.app_context():
            db.create_all()
        return "✅ Tables created successfully in the database."
    except Exception as e:
        return f"❌ Error creating tables: {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = User.query.filter_by(email=email, password=pwd).first()
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect('/dashboard' if user.role == 'organizer' else '/')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            full_name=request.form['full_name'],
            email=request.form['email'],
            password=request.form['password'],
            role=request.form['role']
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'role' not in session or session['role'] != 'organizer':
        return redirect('/login')
    events = Event.query.all()
    return render_template('dashboard.html', events=events)

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if 'role' not in session or session['role'] != 'organizer':
        return redirect('/login')
    if request.method == 'POST':
        event = Event(
            name=request.form['name'],
            date=request.form['date'],
            location=request.form['location'],
            capacity=request.form['capacity'],
            description=request.form['description']
        )
        db.session.add(event)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('create_event.html')

@app.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'role' not in session or session['role'] != 'organizer':
        return redirect('/login')
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.name = request.form['name']
        event.date = request.form['date']
        event.location = request.form['location']
        event.capacity = request.form['capacity']
        event.description = request.form['description']
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit_event.html', event=event)

@app.route('/delete-event/<int:event_id>')
def delete_event(event_id):
    if 'role' not in session or session['role'] != 'organizer':
        return redirect('/login')
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/register-event/<int:event_id>')
def register_event(event_id):
    if 'role' not in session or session['role'] != 'attendee':
        return redirect('/login')
    reg = Registration(user_id=session['user_id'], event_id=event_id)
    db.session.add(reg)
    db.session.commit()
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
