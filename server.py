from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prayer_requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define PrayerRequest Model
class PrayerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    request = db.Column(db.Text, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# HTML for Thank-You Page (same as before)
thank_you_html = "..."  # Keep your thank-you HTML here.

@app.route('/')
def prayer_request_form():
    return app.send_static_file('prayer_request.html')

@app.route('/submit_prayer', methods=['POST'])
def submit_prayer():
    # Extract form data
    name = request.form.get('name', 'Anonymous')
    email = request.form.get('email', 'Not Provided')
    prayer_request = request.form.get('request')

    # Save data to database
    new_request = PrayerRequest(name=name, email=email, request=prayer_request)
    db.session.add(new_request)
    db.session.commit()

    # Return the Thank-You Page
    return render_template_string(thank_you_html)

if __name__ == '__main__':
    app.run(debug=True)
