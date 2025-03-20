import os
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 🔹 뉴스 크롤링 함수
def crawl_news(keyword):
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_items = soup.select(".news_area")  
    news_list = []

    for item in news_items:
        title = item.select_one(".news_tit").get_text(strip=True)
        link = item.select_one(".news_tit")["href"]
        date = item.select_one(".info")  

        if date:
            date = date.get_text(strip=True)
        else:
            date = "날짜 없음"

        news_list.append({"title": title, "link": link, "date": date})

    print("크롤링 결과:", news_list)  
    return news_list

# 🔹 메인 페이지
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 뉴스 검색 엔드포인트
@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword")
    if not keyword:
        return jsonify([])
    
    news_data = crawl_news(keyword)
    return jsonify(news_data)

# 🔹 서버 실행 (Render의 PORT 환경변수 사용)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render 환경변수 사용, 기본값 5000
    app.run(host="0.0.0.0", port=port, debug=True)
