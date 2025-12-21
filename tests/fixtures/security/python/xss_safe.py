"""
Test Fixture: XSS Safe Patterns (Python/Jinja2)

This file contains SAFE XSS mitigation patterns that should NOT trigger false positives
for SEC-002 rule.

Expected detections: 0 violations (no false positives)
Rule ID: SEC-002
Severity: CRITICAL
"""

from jinja2 import Environment, select_autoescape
from flask import Flask, render_template, escape
from markupsafe import escape as markup_escape


# Safe Pattern 1: autoescape enabled (default)
def render_user_comment_safe(comment: str) -> str:
    """SAFE: Jinja2 with autoescape enabled"""

    # SAFE - autoescape=True by default
    env = Environment(autoescape=select_autoescape(['html', 'xml']))

    template = """
    <div class="comment">
        {{ user_comment }}
    </div>
    """

    # User input is automatically escaped
    rendered = env.from_string(template).render(user_comment=comment)

    return rendered


# Safe Pattern 2: Manual escaping with escape()
app = Flask(__name__)


@app.route("/greet/<name>")
def greet_user_safe(name: str):
    """SAFE: Manual escaping before rendering"""

    # SAFE - escape() function used
    safe_name = escape(name)
    template = f"<h1>Hello, {safe_name}!</h1>"

    return template


# Safe Pattern 3: Template file with autoescape
@app.route("/profile/<user_id>")
def show_profile_safe(user_id: str):
    """SAFE: Using template file (autoescape by default)"""

    # SAFE - render_template() enables autoescape
    return render_template("profile.html", user_id=user_id)


# Safe Pattern 4: markupsafe.escape for manual escaping
def format_user_bio_safe(bio_text: str) -> str:
    """SAFE: Manual escaping with markupsafe"""

    # SAFE - escape() before rendering
    escaped_bio = markup_escape(bio_text)

    return f"<p>{escaped_bio}</p>"


# Safe Pattern 5: Content Security Policy
@app.route("/dashboard")
def dashboard_safe():
    """SAFE: CSP header prevents inline scripts"""
    from flask import Response

    html = "<html><body><h1>Dashboard</h1></body></html>"
    response = Response(html)

    # SAFE - CSP prevents script execution
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'"
    )

    return response
