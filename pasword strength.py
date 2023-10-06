from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def password_strength():
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Password Strength Checker</title>
    </head>
    <body>
        <h1>Password Strength Checker</h1>
        <form method="POST">
            <label for="password">Enter a password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Check Password</button>
        </form>
        {% if result is not none %}
        <div>
            <h2>Result:</h2>
            {% if result %}
            <p>Password is strong.</p>
            {% else %}
            <p>Password is weak. Suggestions:</p>
            <ul>
                {% for suggestion in suggestions %}
                <li>{{ suggestion }}</li>
                {% endfor %}
            </ul>
            {% endif %}
        </div>
        {% endif %}
    </body>
    </html>
    """

    if request.method == "POST":
        password = request.form["password"]
        result, suggestions = is_password_secure(password)
        return render_template_string(template, result=result, suggestions=suggestions)

    return render_template_string(template, result=None, suggestions=None)

def is_password_secure(password):
    # Define password criteria
    min_length = 8
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special_char = any(char in "!@#$%^&*()_+{}[]:;<>,.?~\\-" for char in password)

    # Check length
    if len(password) < min_length:
        return False, ["Password is too short. It should have at least {} characters.".format(min_length)]

    # Check character complexity
    suggestions = []
    if not has_lowercase:
        suggestions.append("Add at least one lowercase letter.")
    if not has_uppercase:
        suggestions.append("Add at least one uppercase letter.")
    if not has_digit:
        suggestions.append("Add at least one digit.")
    if not has_special_char:
        suggestions.append("Add at least one special character.")

    return len(suggestions) == 0, suggestions

if __name__ == "__main__":
    app.run(debug=True)
