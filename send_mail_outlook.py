import win32com.client
import os

outlook=win32com.client.Dispatch("Outlook.Application")

def sendmail(email_list):
    for email in email_list:
        send_mail = outlook.CreateItem(0)
        send_mail.To = email #메일 수신인
        # send_mail.CC = "t@gmail.com" #메일 참조
        send_mail.Subject = "테스트 메일입니다" #메일 제목
        send_mail.HTMLBody = "테스트 메일 입니다" #내용

        file_path = './강남언니_b.csv' #상대경로 

        print(__file__)
        print(f"os.getcwd() : {os.getcwd()}")

        if not os.path.isabs(file_path): # 절대경로 가 아니면 절대경로로 설정
            data_path = os.path.abspath(file_path)
            print("abs path:", data_path)


        send_mail.Attachments.Add(data_path)

        send_mail.Send() #메일 보내기
sendmail(['kyu23336@gmail.com','kyu233@naver.com'])