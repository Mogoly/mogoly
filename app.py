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

    news_items = soup.select(".news_area")  # 네이버 뉴스 기사 크롤링
    news_list = []

    for item in news_items:
        title = item.select_one(".news_tit").get_text(strip=True)
        link = item.select_one(".news_tit")["href"]
        date = item.select_one(".info")  # 날짜 가져오기

        if date:
            date = date.get_text(strip=True)
        else:
            date = "날짜 없음"

        news_list.append({"title": title, "link": link, "date": date})

    print("크롤링 결과:", news_list)  # 🔹 디버깅용 출력 (Render Logs에서 확인 가능)
    return news_list

# 🔹 메인 페이지
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 뉴스 검색 엔드포인트 (AJAX 요청 처리)
@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword")  # 검색어 가져오기
    if not keyword:
        return jsonify([])  # 빈 검색어 처리
    
    news_data = crawl_news(keyword)
    return jsonify(news_data)  # JSON 형태로 반환

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
