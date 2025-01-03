from flask import Flask, render_template,request
import crwal

app = Flask(__name__)

is_crawling = False  # 크롤링 진행 상태를 나타내는 전역 변수
request_email =[]

@app.route('/')
def index():
    global is_crawling
    global request_email
    if is_crawling:
        return render_template("reservation.html",email_list = request_email)
    else:
        return render_template('test.html')

@app.route('/start_crawling',methods=["POST"])
def start_crawling():
    global is_crawling
    global request_email
    if is_crawling:
        return render_template("reservation.html",email_list = request_email)
    is_crawling = True
    try:
        email = request.form.get("email")
        request_email.append(email)
        crwal.test() # 크롤링을 흉내내는 5초 대기
        print("크롤링 완료!")
        print(request_email)
    finally:
        is_crawling = False  # 크롤링 종료 후 변수 값 변경
    return "크롤링이 완료되었습니다."

@app.route('/finish_reservation',methods=["POST"])
def finish_reservation():
    global request_email
    email = request.form.get("email")
    request_email.append(email)
    return "예약 완료!"

if __name__ == '__main__':
    app.run(debug=True)