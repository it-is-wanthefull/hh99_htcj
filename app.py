from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
# 주석 사용법
'''
라이브러리 > 패키지 > 모듈 순으로 포함관계이다.
from/import는 종속관계를 지키는 범위에서 순서는 무의미하나 표준->서드->사용자정의 순이라는 관례는 있다.
- flask: 웹 프레임워크
-- Flask: 웹 구동을 위한 클래스, 통상 app.py로 작성하나 다른이름이어도 무관
-- render_template: HTML을 렌더링하는 함수
-- request: 현재 HTTP 요청에 대한 정보를 담은 객체
-- redirect: 클라이언트를 다른 URL로 리디렉션하는 함수
-- url_for: 뷰 함수나 정적 파일 등의 URL을 생성하는 함수입니다
- os: 파일시스템 관련
- sqlalchemy: SQL 관련
'''

# Flask 및 SQL 구동위한 기본코드
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.username} {self.title} 추천 by {self.username}'


@app.route("/")
def home():  # 세미콜론없어서 줄바꿈 필수
    context = {
        'name': "이름은 완다풀.",  # 따옴표 무관
        "motto": '세상은 완다풀!',
    }
    return render_template('motto.html', data=context)  # HTML로 넘김


@app.route("/iloveyou/<name>")  # URL로 값 추출
def iloveyou(name):  # 변수로 받은후
    motto = f"{name}야 난 너뿐이야!"  # 사용
    context = {
        "name": name,
        'motto': motto,
    }
    return render_template('motto.html', data=context)


@app.route("/music")
def music():
    song_list = Song.query.all()  # DB값 전부 로딩
    return render_template('music.html', data=song_list)


@app.route("/music/create")
def music_create():
    # form에서 건너받기
    username_receive = request.args.get("username")
    title_receive = request.args.get("title")
    artist_receive = request.args.get("artist")
    image_receive = request.args.get("image_url")

    # DB에 저장하기
    song = Song(username=username_receive, title=title_receive,
                artist=artist_receive, image_url=image_receive)
    db.session.add(song)
    db.session.commit()

    return redirect(url_for('render_music_filter', username=username_receive))


@app.route("/music/delete/<song_id>")
def delete_song(song_id):
    song = Song.query.get(song_id) # 삭제위해 소환
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('music')) # redirect일때는 'music(주소)'이어야하고 render_template일땐 'music.html(파일)'이어야함


@app.route("/music/<username>")
def render_music_filter(username): # 필터링 된 것만 넘김
    filter_list = Song.query.filter_by(username=username).all() # 파이썬도 동등연산자가 '=='인건 맞으나 메서드에선 '='로 동등연산한다함
    return render_template('music.html', data=filter_list)


if __name__ == "__main__":  # 코드 맨 뒷줄이어야만 함
    app.run(debug=True)  # debug=True이면 코드수정 즉시 실시간으로 반영된다
