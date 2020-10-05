import smtplib

from email.mime.text import MIMEText

def mailalarm():
    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)    
    # TLS 보안 시작
    s.starttls()    
    # 로그인 인증
    s.login('YOURID@gmail.com', 'YOUR_PW')    
    # 보낼 메시지 설정
    msg = MIMEText('내용 : ENERTALK 프로그램 확인 바랍니다.')
    msg['Subject'] = 'Alarm for Enertalk data donwload'    
    # 메일 보내기
    s.sendmail("SENDID@gmail.com", "RECEIVEDID@gmail.com", msg.as_string())    
    # 세션 종료
    s.quit()