from flask import Flask, request, render_template_string
import psycopg2
import os

app = Flask(__name__)

# Get the database URL from environment variables (set on Render)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://username:password@hostname:port/dbname')

# Function to save to the database
def save_to_db(name, email, prayer_request):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create the table if it doesn't already exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prayer_requests (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                request TEXT NOT NULL
            )
        """)

        # Insert the prayer request
        cur.execute("INSERT INTO prayer_requests (name, email, request) VALUES (%s, %s, %s)",
                    (name, email, prayer_request))

        conn.commit()  # Save changes to the database
        cur.close()    # Close the cursor
        conn.close()   # Close the connection
    except Exception as e:
        print(f"Error saving to database: {e}")

# HTML for Thank-You Page
thank_you_html = """
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
"""

# Route for the Prayer Request Form
@app.route('/')
def prayer_request_form():
    return '''
        <form method="POST" action="/submit_prayer">
            <label>Name:</label>
            <input type="text" name="name" required><br>
            <label>Email:</label>
            <input type="email" name="email" required><br>
            <label>Prayer Request:</label>
            <textarea name="request" required></textarea><br>
            <button type="submit">Submit</button>
        </form>
    '''

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

