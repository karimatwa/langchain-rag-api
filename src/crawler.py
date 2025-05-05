import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from typing import List
from config import BASE_URL, USER_AGENT
from logger import Logger
logger = Logger.get(__name__)

HEADERS = {'User-Agent': USER_AGENT} if USER_AGENT else {}

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    clean  = parsed._replace(query='', fragment='')
    return urlunparse(clean).rstrip('/')


def should_process_url(url: str) -> bool:
    exclude = {'.png','.jpg','.jpeg','.gif','.svg','.ico','.webp',
               '.pdf','.doc','.docx','.xls','.xlsx','.ppt','.pptx',
               '.zip','.tar','.gz','.rar','.7z','.css','.js','.woff',
               '.woff2','.ttf','.eot'}
    lower = url.lower()
    return bool(url) and not any(lower.endswith(ext) for ext in exclude)


def get_all_urls() -> List[str]:
    visited, to_visit, collected = set(), {BASE_URL}, set()
    while to_visit:
        url = to_visit.pop()
        norm = normalize_url(url)
        if norm in visited:
            continue
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            visited.add(norm)
            if resp.status_code != 200:
                continue
            collected.add(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = urljoin(url, a['href'])
                if not should_process_url(href):
                    continue
                if urlparse(href).netloc != urlparse(BASE_URL).netloc:
                    continue
                if normalize_url(href) not in visited:
                    to_visit.add(href)
        except Exception:
            continue
    logger.info(f'🐞 Crawled {len(collected)} URLs')
    return list(collected)