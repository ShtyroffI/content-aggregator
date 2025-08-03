import requests
from bs4 import BeautifulSoup

URL = "https://www.python.org/blogs/"

HEADERS = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_html(url, params=''):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None

def parse_articles(html_content):
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, 'html.parser')
    news_list_container = soup.find('ul', class_='list-recent-posts')

    if not news_list_container:
        return []
    
    news_items = news_list_container.find_all('li')

    articles = []
    for item in news_items:
        title_tag = item.find('a')

        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
            articles.append({'title': title, 'link': link})
            
    return articles

if __name__ == "__main__":
    html_content = get_html(URL)
    if html_content:
        print("HTML-код страницы успешно получен!")
        articles_list = parse_articles(html_content)
        print(f"Найдено статей: {len(articles_list)}")
        print(articles_list)
    else:
        print("Не удалось получить HTML-код страницы.")