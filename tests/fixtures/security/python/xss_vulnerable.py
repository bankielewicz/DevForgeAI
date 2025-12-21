"""
Test Fixture: XSS Vulnerability Patterns (Python/Jinja2)

This file contains 3+ XSS vulnerability patterns that MUST be detected by
SEC-002 rule (devforgeai/ast-grep/rules/python/security/xss.yml).

Expected detections: ≥3 violations
Rule ID: SEC-002
Severity: CRITICAL
"""

from jinja2 import Environment, select_autoescape
from flask import Flask, render_template_string, make_response


# Pattern 1: Jinja2 |safe filter with user input
def render_user_comment_unsafe(comment: str) -> str:
    """VULNERABLE: Jinja2 |safe filter bypasses escaping"""
    template = """
    <div class="comment">
        {{ user_comment|safe }}
    </div>
    """

    # SEC-002 should detect |safe filter
    env = Environment()
    rendered = env.from_string(template).render(user_comment=comment)

    return rendered


# Pattern 2: autoescape disabled globally
def render_with_autoescape_off(user_input: str) -> str:
    """VULNERABLE: autoescape=False disables XSS protection"""

    # SEC-002 should detect autoescape=False
    env = Environment(autoescape=False)

    template = "<p>Welcome, {{ username }}!</p>"
    rendered = env.from_string(template).render(username=user_input)

    return rendered


# Pattern 3: Flask render_template_string without escaping
app = Flask(__name__)


@app.route("/greet/<name>")
def greet_user_unsafe(name: str):
    """VULNERABLE: render_template_string with user input"""

    # SEC-002 should detect unescaped user input
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)


# Pattern 4: Direct HTML response with user input
@app.route("/profile/<user_id>")
def show_profile_unsafe(user_id: str):
    """VULNERABLE: Direct HTML concatenation"""

    # SEC-002 should detect user input in HTML
    html = f"""
    <html>
        <body>
            <h1>Profile for user {user_id}</h1>
        </body>
    </html>
    """

    response = make_response(html)
    response.headers["Content-Type"] = "text/html"
    return response


# Pattern 5: Mark user input as safe
def format_user_bio(bio_html: str) -> str:
    """VULNERABLE: Marking user input as safe"""
    from markupsafe import Markup

    # SEC-002 should detect Markup() on user input
    safe_bio = Markup(bio_html)

    return str(safe_bio)
