from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.config import SECRET_KEY
from validators import url as validate_url
from urllib.parse import urlparse
from page_analyzer.urls_repository import UrlRepository

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    """Render main page with flash messages"""
    flash_messages = get_flashed_messages(with_categories=True)
    return render_template("index.html", flashed_messages=flash_messages)


@app.post("/urls")
def add_url():
    """Handle URL submission and validation"""
    repo = UrlRepository()
    submitted_url = request.form.get("url")

    if len(submitted_url) > 255 or not validate_url(submitted_url):
        flash("Некорректный URL", "danger")
        print("Flash message set: Некорректный URL, danger")
        return redirect(url_for("index"))

    parsed = urlparse(submitted_url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}"
    existing_url = repo.get_url_by_name(normalized_url)

    if existing_url:
        flash("Страница уже существует", "info")
        print("Flash message set: Страница уже существует, info")
        return redirect(url_for("show_url", url_id=existing_url["id"]))

    url_id = repo.save_url(normalized_url)
    flash("Страница успешно добавлена", "success")
    print("Flash message set: Страница успешно добавлена, success")
    return redirect(url_for("show_url", url_id=url_id))


@app.route("/urls/<int:url_id>")
def show_url(url_id):
    """Show details for specific URL with flash_messages"""
    repo = UrlRepository()
    flash_messages = get_flashed_messages(with_categories=True)
    url_data = repo.get_url_by_id(url_id)
    return render_template(
        "url.html",
        site=url_data,
        flashed_messages=flash_messages,
    )


@app.get("/urls")
def get_urls():
    """Show all URLs"""
    repo = UrlRepository()
    all_urls = repo.get_all_urls()
    return render_template("urls.html", urls=all_urls)
