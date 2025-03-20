import requests
from bs4 import BeautifulSoup

def crawl_news(keyword):
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_items = soup.select(".news_area")  # 크롤링할 뉴스 영역 선택
    news_list = []

    for item in news_items:
        title_element = item.select_one(".news_tit")
        if title_element:
            title = title_element.get_text(strip=True)
            link = title_element["href"]
        else:
            continue

        date_element = item.select_one(".info")
        date = date_element.get_text(strip=True) if date_element else "날짜 없음"

        news_list.append({"title": title, "link": link, "date": date})

    print("크롤링 결과:", news_list)  # 🔹 Render Logs에서 확인 가능
    return news_list
