import poplib
from email import policy
from email.parser import BytesParser

host = 'pop.mail.ru'
port = 995

user = 'kadarmetov.dn@mail.ru'
password = open('password.txt').readline()

M = poplib.POP3_SSL(host, port)
M.getwelcome()
M.user(user)
M.pass_(password)
messages_count = len(M.list()[1])
emails_data = []
for i in range(1, messages_count + 1):
    response, lines, octets = M.retr(i)
             
    msg_content = b'\r\n'.join(lines)
            
    msg = BytesParser(policy=policy.default).parsebytes(msg_content)
    
    email_info = {
        'number': i,
        'subject': msg['subject'] or 'Без темы',
        'from': msg['from'] or 'Неизвестный отправитель',
        'date': msg['date'] or 'Неизвестная дата',
        'to': msg['to'] or '',
        'body': ''
    }

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
                        
            if content_type == "text/plain" and "attachment" not in content_disposition:
                email_info['body'] = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        email_info['body'] = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                
    emails_data.append(email_info)

M.quit()

for email_data in emails_data:
    print(f"\nПисьмо #{email_data['number']}")
    print(f"Тема: {email_data['subject']}")
    print(f"От: {email_data['from']}")
    print(f"Дата: {email_data['date']}")
    print("-" * 50)