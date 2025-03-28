from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.database import UrlRepository
from page_analyzer.utils import normalize_url, validate_url, check_and_parse_url
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
repo = UrlRepository()


@app.route("/")
def index():
    """Render main page with flash messages"""
    flash_messages = get_flashed_messages(with_categories=True)
    return render_template("index.html", flashed_messages=flash_messages)


@app.post("/urls")
def add_url():
    """Add new URL to database"""
    url = request.form.get("url")

    if not validate_url(url):
        flash("Некорректный URL", "danger")
        return render_template(
            "index.html",
            flashed_messages=get_flashed_messages(with_categories=True),
        ), 422

    normalized_url = normalize_url(url)
    existing_url = repo.get_url_by_name(normalized_url)

    if existing_url:
        flash("Страница уже существует", "info")
        return redirect(url_for("show_url_info", url_id=existing_url["id"]))

    url_id = repo.insert_url(normalized_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("show_url_info", url_id=url_id))


@app.route("/urls/<int:url_id>")
def show_url_info(url_id):
    """Show details for specific URL with flash_messages"""
    flash_messages = get_flashed_messages(with_categories=True)
    url_data = repo.get_url(url_id)
    url_checks = repo.get_checks_by_url_id(url_id)

    return render_template(
        "url.html",
        site=url_data,
        checks=url_checks,
        flashed_messages=flash_messages,
    )


@app.route("/urls")
def get_urls():
    """Show all URLs"""
    all_urls = repo.get_urls_with_last_check_date_and_status_code()
    return render_template("urls.html", urls=all_urls)


@app.post("/urls/<int:url_id>/checks")
def add_url_check(url_id):
    """Add new check for specific URL"""
    url = repo.get_url(url_id).get("name", "")
    result = check_and_parse_url(url)

    if result is False:
        flash("Произошла ошибка при проверке", "danger")
    else:
        repo.insert_url_check(
            url_id,
            result["status_code"],
            result["h1"],
            result["title"],
            result["description"],
        )
        flash("Страница успешно проверена", "success")

    return redirect(url_for("show_url_info", url_id=url_id))
