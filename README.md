# SEO Website Analyzer 🔍
## Hexlet test and linter status
[![Hexlet tests](https://github.com/Ilia-Ivankov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Ilia-Ivankov/python-project-83/actions)
## CI 
[![CI Status](https://github.com/Ilia-Ivankov/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/Ilia-Ivankov/python-project-83/actions/workflows/ci.yml)
## Maintainability
[![Maintainability](https://api.codeclimate.com/v1/badges/11fe059c586729107e2b/maintainability)](https://codeclimate.com/github/Ilia-Ivankov/python-project-83/maintainability)

## Project Description 📝

SEO Website Analyzer is a web application designed to evaluate websites' SEO readiness. The project provides comprehensive analysis of web pages, including:

- Website URL validation and storage
- HTTP status code verification
- SEO tag analysis (h1, title, meta description)
- Detailed check history for each website
- User-friendly web interface for managing and reviewing results

## Key Features ✨

- **URL Management**: Add and store website URLs with automatic normalization
- **SEO Analysis**: Extract and analyze critical SEO elements from web pages
- **Check History**: Maintain complete history of all performed checks
- **Error Handling**: Comprehensive error handling and user notifications
- **Responsive Design**: Mobile-friendly interface using Bootstrap

## Technology Stack 🛠️

- **Backend**: Python, Flask
- **Frontend**: HTML, Bootstrap
- **Database**: PostgreSQL
- **HTML Parsing**: BeautifulSoup4
- **URL Validation**: validators
- **HTTP Requests**: requests
- **CI/CD**: GitHub Actions
- **Code Quality**: flake8

## Deployment 🚀

The project is deployed on Render: [https://python-project-83-ysk7.onrender.com](https://python-project-83-ysk7.onrender.com)

## ⚙️ Installation and Setup

First, create a `.env` file in the project root with the following content:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
SECRET_KEY=your_secret_key_here
```

Replace the values with your actual database credentials and a secure secret key.

Then run:

```bash
make build
```

> **Note:** Make sure you have PostgreSQL installed and export Database Url by doing this: `export DATABASE_URL=postgresql://janedoe:mypassword@localhost:5432/mydb`(replace with actual values) or the project won't work

This command will:
1. Install all required dependencies
2. Set up the database
3. Prepare the application for running

To start the application, use:

```bash
make start
```


## Linting 🧹

To run linter:
```bash
make lint
```

## How to Use 🕹️

1. Access the main page
2. Enter the website URL you want to analyze
3. Click "Проверить" button
4. View analysis results in the detailed table
5. Click "Запустить проверку" to start SEO analyze 
6. Manage all websites through the "Сайты" section

## Installation, Dev Mode, Linting demo
[![asciicast](https://asciinema.org/a/AdHrTnbkPX040D0vGrizyyiXd.svg)](https://asciinema.org/a/AdHrTnbkPX040D0vGrizyyiXd)