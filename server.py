import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__, static_folder='static', template_folder='templates')

# Get the database URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://prayer_requests_db_user:ijbPHpm9XHKVw4q2xKNWZ9olTdEoSyPR@dpg-cu5g3152ng1s73be9e2g-a/prayer_requests_db')

# Function to save to the database
def save_to_db(name, email, prayer_request):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create the table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prayer_requests (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                request TEXT NOT NULL
            )
        """)

        # Insert prayer request into the database
        cur.execute("INSERT INTO prayer_requests (name, email, request) VALUES (%s, %s, %s)",
                    (name, email, prayer_request))

        conn.commit()  # Save changes to the database
        cur.close()    # Close the cursor
        conn.close()   # Close the connection
    except Exception as e:
        print(f"Error saving to database: {e}")

# HTML for the Prayer Request Form
def prayer_request_html():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prayer Request | Jesus Youth Intercession Team</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(to bottom right, #6a11cb, #2575fc);
                color: #ffffffa2;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background: rgba(255, 255, 255, 0.9);
                color: #333;
                max-width: 600px;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
                text-align: center;
            }
            h1 {
                color: #6a11cb;
                font-size: 2.2rem;
                margin-bottom: 10px;
            }
            p {
                margin-bottom: 20px;
                font-size: 1.1rem;
                line-height: 1.6;
                color: #555;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            label {
                font-weight: 500;
                text-align: left;
            }
            input, textarea {
                width: 100%;
                padding: 12px;
                font-size: 1rem;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-sizing: border-box;
            }
            button {
                background: linear-gradient(to right, #6a11cb, #2575fc);
                color: #fff;
                border: none;
                padding: 12px;
                font-size: 1.2rem;
                font-weight: 600;
                border-radius: 10px;
                cursor: pointer;
            }
            footer {
                margin-top: 20px;
                font-size: 0.9rem;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Submit Your Prayer Request</h1>
            <p>We believe in the power of prayer. Share your prayer request with us, and our prayer team will stand with you in faith.</p>
            <form method="POST" action="/submit_prayer">
                <label for="name">Your Name (optional):</label>
                <input type="text" id="name" name="name" placeholder="Enter your name">

                <label for="email">Your Email (optional):</label>
                <input type="email" id="email" name="email" placeholder="Enter your email">

                <label for="request">Your Prayer Request:</label>
                <textarea id="request" name="request" rows="5" placeholder="Write your prayer request here..." required></textarea>

                <button type="submit">Submit Prayer Request</button>
            </form>
            <footer>
                &copy; 2025 Jesus Youth Prayer Group | All Rights Reserved
            </footer>
        </div>
    </body>
    </html>
    '''

# HTML for the Thank You Page
thank_you_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You!</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to bottom right, #6a11cb, #2575fc);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background: #fff;
            color: #333;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
            max-width: 400px;
        }
        h1 {
            color: #6a11cb;
            font-size: 2rem;
        }
        p {
            font-size: 1.1rem;
            margin-top: 10px;
            line-height: 1.5;
        }
        a {
            color: #6a11cb;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🙏 Thank You!</h1>
        <p>Your prayer request has been received. Our prayer team will keep you in their prayers. 💖</p>
        <p><a href="/">Submit Another Request</a></p>
    </div>
</body>
</html>
'''

# Route for the Prayer Request Form
@app.route('/')
def prayer_request_form():
    return prayer_request_html()

# Route to Handle Form Submissions
@app.route('/submit_prayer', methods=['POST'])
def submit_prayer():
    name = request.form.get('name', 'Anonymous')
    email = request.form.get('email', 'Not Provided')
    prayer_request = request.form.get('request')

    # Save data to PostgreSQL database
    save_to_db(name, email, prayer_request)

    # Return the Thank-You Page
    return render_template_string(thank_you_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

