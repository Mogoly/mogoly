from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

app = Flask(__name__)

def get_news(keyword):
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = soup.select('.news_area')[:20]
    news_list = []

    for item in news_items:
        title = item.select_one('.news_tit').get_text().strip()
        link = item.select_one('.news_tit')['href']
        press = item.select_one('.info.press').get_text().strip() if item.select_one('.info.press') else "발간사 정보 없음"

        date_tag = item.select_one('.info_group')
        date = "날짜 정보 없음"
        if date_tag:
            date_texts = [span.get_text().strip() for span in date_tag.find_all(["span", "div", "a"]) if span.get_text().strip()]
            for text in date_texts:
                if re.search(r'\d{4}\.\d{1,2}\.\d{1,2}\.\s\d{2}:\d{2}', text):
                    date = text
                    break
                elif re.search(r'\d{4}\.\d{1,2}\.\d{1,2}\.', text):
                    date = text + " 00:00"
                    break
                elif "시간 전" in text or "분 전" in text or "일 전" in text:
                    date = text
                    break
        
        try:
            if re.search(r'\d{4}\.\d{1,2}\.\d{1,2}\.\s\d{2}:\d{2}', date):
                date_obj = datetime.strptime(date, "%Y.%m.%d. %H:%M")
                date = date_obj.strftime("%Y년 %m월 %d일 %H:%M")
            elif re.search(r'\d{4}\.\d{1,2}\.\d{1,2}\.', date):
                date_obj = datetime.strptime(date, "%Y.%m.%d.")
                date = date_obj.strftime("%Y년 %m월 %d일 00:00")
            elif "시간 전" in date or "분 전" in date or "일 전" in date:
                now = datetime.now()
                if "시간 전" in date:
                    hours = int(re.search(r'\d+', date).group())
                    date = (now - timedelta(hours=hours)).strftime("%Y년 %m월 %d일 %H:%M")
                elif "분 전" in date:
                    minutes = int(re.search(r'\d+', date).group())
                    date = (now - timedelta(minutes=minutes)).strftime("%Y년 %m월 %d일 %H:%M")
                elif "일 전" in date:
                    days = int(re.search(r'\d+', date).group())
                    date = (now - timedelta(days=days)).strftime("%Y년 %m월 %d일 %H:%M")
        except Exception as e:
            print(f"날짜 변환 오류: {e}")
            date = "날짜 정보 없음"

        news_list.append({"press": press, "date": date, "title": title, "link": link})

    return news_list

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    news_results = get_news(keyword)
    return jsonify(news_results)

if __name__ == "__main__":
    app.run(debug=True)
