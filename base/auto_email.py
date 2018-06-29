# coding=utf-8
# UlionTse

import smtplib
from email.mime.multipart import MIMEMultipart as MMpt
from email.mime.text import MIMEText as MMTxt
import re


def auto_mail(from_email,from_pwd,to_email,subject,content):
    msg = MMpt()
    msg['from'] = from_email
    msg['to'] = to_email
    msg['subject'] = subject
    txt = MMTxt(content)
    msg.attach(txt)

    server = re.findall('@([a-z]+).com', from_email)
    smtp_server = 'smtp.' + server[0] + '.com'

    smtp = smtplib.SMTP()
    smtp.connect(smtp_server, '25')  # pop:110
    smtp.login(from_email, from_pwd)
    smtp.sendmail(from_email, to_email, str(msg))
    smtp.quit()
    print('Sent successfully!')


if __name__ == '__main__':
    from_email = 'xxxxx@sina.com'##修改成自己的发件邮箱，并开启该邮箱的SMTP服务(重要)
    from_pwd = '****'#密码
    to_email = 'xxxxx@163.com'#目标邮箱
    content = 'Hello, boss! I am auto-mail-helper of UlionTse.'#内容
    subject = 'Hello, boss!'#标题

    auto_mail(from_email,from_pwd,to_email,subject,content)

    self_email = 'xxxxx@qq.com'#自己检查邮箱
    self_content = 'Send successfully about {}!'.format(to_email)
    self_subject = 'exam {}'.format(to_email)

    auto_mail(from_email,from_pwd,self_email,self_subject,self_content)
