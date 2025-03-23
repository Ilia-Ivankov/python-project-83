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
import requests
from bs4 import BeautifulSoup

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
    """Handle URL submission and validation"""
    submitted_url = request.form.get("url")

    if len(submitted_url) > 255 or not validate_url(submitted_url):
        flash("Некорректный URL", "danger")
        return redirect(url_for("index")), 422

    parsed = urlparse(submitted_url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}"
    existing_url = repo.get_url_by_name(normalized_url)

    if existing_url:
        flash("Страница уже существует", "info")
        return redirect(url_for("show_url_info", url_id=existing_url["id"]))

    url_id = repo.save_url(normalized_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("show_url_info", url_id=url_id))


@app.route("/urls/<int:url_id>")
def show_url_info(url_id):
    """Show details for specific URL with flash_messages"""
    flash_messages = get_flashed_messages(with_categories=True)
    url_data = repo.get_url_by_id(url_id)
    url_checks = repo.get_all_checks(url_id)

    return render_template(
        "url.html",
        site=url_data,
        checks=url_checks,
        flashed_messages=flash_messages,
    )


@app.get("/urls")
def get_urls():
    """Show all URLs"""
    all_urls = repo.get_all_urls()
    return render_template("urls.html", urls=all_urls)


@app.post("/urls/<int:url_id>/checks")
def add_url_check(url_id):
    """Add new check for specific URL"""
    url = repo.get_url_by_id(url_id).get("name", "")
    response = requests.get(url, timeout=180)
    try:
        response.raise_for_status()
        status = response.status_code
        soup = BeautifulSoup(response.text, "html.parser")
        h1_tag = soup.find("h1")
        h1 = h1_tag.text.strip() if h1_tag else None
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else None
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"].strip() if description_tag else None
        repo.save_url_check(url_id, status, h1, title, description)
        flash("Страница успешно проверена", "success")
    except requests.exceptions.RequestException:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("show_url_info", url_id=url_id))
