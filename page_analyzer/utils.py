from urllib.parse import urlparse
from validators import url as validate


def normalize_url(url: str) -> str:
    """Normalize URL by keeping protocol and path"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def validate_url(url: str) -> bool:
    """Validate URL format"""
    return validate(url) and len(url) <= 255
