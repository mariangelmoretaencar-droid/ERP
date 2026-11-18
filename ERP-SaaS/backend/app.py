

from flask import Flask, render_template
from pathlib import Path

from backend.routes.customers import customers_bp

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "frontend" / "pages"),
    static_folder=str(BASE_DIR / "frontend"),
    static_url_path="/static"
)

# Registrar módulos
app.register_blueprint(customers_bp)


@app.route("/")
def home():
    return render_template("dashboard.html")


from backend.routes.customers import customers_bp

app.register_blueprint(customers_bp)
