from flask import Flask, render_template,request
import crwal
from send_mail_smtp import sendmail
from ticket_crwal import get_data_from_yeosin

import crwal_setting

app = Flask(__name__)

is_crawling = False  # 크롤링 진행 상태를 나타내는 전역 변수
request_email =[]
equipment_list = ["올리지오x", "올리지오", "덴서티하이","덴서티", "써마지", "볼뉴머", "텐써마", "세르프"]
# equipment_list = [ "올리지오", "덴서티", "써마지",  "세르프"]
# equipment_list = ["덴서티"]

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
        product = request.form.get("product")
        request_email.append(email)

        a = crwal.gangnamunni_crawl()
        b = get_data_from_yeosin(equipment_list)
        a.extend(b)

        crwal_setting.make_to_csv(a)

    finally:
        request_email = []
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