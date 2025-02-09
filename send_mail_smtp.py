import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
# from important_data import get_app_password


HOST = "smtp-mail.outlook.com"
PORT = 587
def sendmail(to_addr) : 
    from_addr = formataddr(('황규민','a20240802@jeisys.com'))
    password = get_app_password()

    # 메일 본문
    msg = MIMEMultipart()
    msg['From'] = from_addr  # 송신자
    msg['to'] = ", ".join(to_addr)      # 수신자
    msg["Subject"] = "테스트 이메일" # 제목

    body = "테스트" # 내용

    msg.attach(MIMEText(body,"plain"))

    #첨부파일 
    with open('강남언니.csv','rb') as file:
        attach_file = file.read()

    file_data = MIMEBase('application', 'octet-stream')
    file_data.set_payload(attach_file)
    encoders.encode_base64(file_data)

    #첨부파일 해더
    file_data.add_header('Content-Disposition', "attachment", filename="강남언니.csv") # << 파일 이름 변경해줌(기존 파일 유지)
    msg.attach(file_data)


    session = smtplib.SMTP(HOST,PORT)

    session.ehlo()
    session.starttls()

    status_code , response = session.login('a20240802@jeisys.com',password)
    print(f"{status_code} : {response}")

    text = msg.as_string()

    session.sendmail(from_addr,to_addr,text)
    session.quit()