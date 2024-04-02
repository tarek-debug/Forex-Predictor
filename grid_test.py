
from email.mime.text import MIMEText
from email.header import Header
import smtplib

# Create a MIMEText object to represent the email
msg = MIMEText('This is a test email.', 'plain', 'utf-8')
msg['From'] = Header('Your Name <tarek.alsolame@trincoll.edu>', 'utf-8')
msg['To'] = Header('Recipient Name <tareksolamy321@gmail.com>', 'utf-8')
msg['Subject'] = Header('Subject: Test', 'utf-8')

# SMTP configuration
server = smtplib.SMTP('smtp.sendgrid.net', 587)
server.starttls()

# Here, replace 'your_sendgrid_apikey' with your actual SendGrid API key
server.login('apikey', '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')

# Send the email
server.sendmail('tarek.alsolame@trincoll.edu', ['tareksolamy321@gmail.com'], msg.as_string())

server.quit()
