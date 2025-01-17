from flask import Flask, request, render_template_string

app = Flask(__name__)

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
    return app.send_static_file('prayer_request.html')

# Route to Handle Form Submissions
@app.route('/submit_prayer', methods=['POST'])
def submit_prayer():
    # Extract form data
    name = request.form.get('name', 'Anonymous')
    email = request.form.get('email', 'Not Provided')
    prayer_request = request.form.get('request')

    # Save data to a text file
    with open('prayer_requests.txt', 'a') as file:
        file.write(f"Name: {name}\nEmail: {email}\nRequest: {prayer_request}\n{'-'*40}\n")

    # Return the Thank-You Page
    return render_template_string(thank_you_html)

if __name__ == '__main__':
    app.run(debug=True)
