import sys
import imaplib
import getpass
import email
import email.header
import datetime
import re
import smtplib
import poplib



def send_mail():
    try:
        srv=str(input("Enter the SMTP ServerName:"))
        EMAIL_ACCOUNT=str(input("Enter the Receipient Email Account:"))
        print ('Enter the Password:')
        PASS=getpass.getpass()
        _subject = str(input('Please enter subject of email:'))
        _body = str(input('Please enter body of email:'))
        smtp_server_conn = smtplib.SMTP(srv, 587)
        smtp_server_conn.ehlo()
        smtp_server_conn.starttls()
        smtp_server_conn.login(EMAIL_ACCOUNT, PASS)
        message = 'Subject:{}\n\n{}'.format(_subject, _body)
        smtp_server_conn.sendmail(EMAIL_ACCOUNT, EMAIL_ACCOUNT, message)
        smtp_server_conn.quit()
        print("Mail Sent Successfully!")
    except:
        print("error occured!")

def pop_fetch():
    try:
        srv=str(input("Enter the POP ServerName:"))
        EMAIL_ACCOUNT=str(input("Enter the Receipient Email Account:"))
        print ('Enter the Password:')
        PASS=getpass.getpass()
        pop_server_conn = poplib.POP3_SSL(srv)
        pop_server_conn.user(EMAIL_ACCOUNT)
        pop_server_conn.pass_(PASS)
        mailbox_stat = pop_server_conn.stat()
        print("Current Mailbox Status is {}".format(mailbox_stat))
        print(pop_server_conn.list()[1])
        #Fetches the latest mail from the mailbox
        (server_msg, body, octets) = pop_server_conn.retr(len(pop_server_conn.list()[1]))
        for i in body:
            try:
                msg = email.message_from_string(i.decode())
                strtext = msg.get_payload()
                print(strtext)
            except:
                print("Failed to read the message!")
        pop_server_conn.quit()
    except:
        print("failed to fetch!")

#send_mail("Test Mail", "Testing.....!")
#pop_fetch()



def mail_body(msg):
    #print (msg)
# Retrive mail body...
    text=""
    if msg.is_multipart():
        html = None
        for part in msg.get_payload():
             if part.get_content_charset() is None:
                     text = part.get_payload(decode=True)
                     continue
             charset = part.get_content_charset()
             if part.get_content_type() == 'text/plain':
                     text = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
             if part.get_content_type() == 'text/html':
                     html = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
        if text is not None:
             return (text.strip())
        else:
             return (html.strip())
    else:
        #text = str(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        #print (msg.get_payload)
        #print (str(msg.get_payload(decode=True)))
        text = msg.get_payload(decode=True).decode("utf-8")
        return (text.strip())

def process_mailbox(M):
# Doing some basic things like getting unread messages and printing datetime, message headers
    st, data = M.search(None, '(UNSEEN)')
    test=[item.decode('utf-8') for item in data]
    if st != 'OK' or (len(test) == 1 and len(test[0]) == 0):
        print("No messages found. Exiting!!!")
        return

    for num in data[0].split():
        st, data = M.fetch(num, '(RFC822)')
        if st != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        print (list(msg))
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
        #print('Received To And Date:', msg['X-Apparently-To:'])
        print('Subject %s: %s' % (num.decode("utf-8"), subject))
        print('Body:', mail_body(msg))

def imapread():
#Initializing variables and imap server
    srv=str(input("Enter the IMAP ServerName:"))
    EMAIL_ACCOUNT=str(input("Enter the Receipient Email Account:"))
    print ("Enter Password:")
    PASS=getpass.getpass()
    M = imaplib.IMAP4_SSL(srv)
    try:
        st, data = M.login(EMAIL_ACCOUNT, PASS)
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED!!! ")
        sys.exit(1)
# List MailBoxes
    st, mailboxes = M.list()
    if st == 'OK':
        print("Available MailBoxes...")
        x=re.findall(r'"(.*?)"', str(mailboxes))
        lst=list(filter(('/').__ne__, x))
        print (lst)
        E_FOLDER=str(input("Please Select the MailBox(Quotes needed): "))
        if any(lstt in E_FOLDER for lstt in lst):
            EMAIL_FOLDER=str(E_FOLDER)
# Select mailbox and process
    st, data = M.select(EMAIL_FOLDER)
    if st == 'OK':
        print("Processing Unread mailbox...\n")
        process_mailbox(M)
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", st)

    M.logout()

if __name__ == '__main__':
#Calling Main IMAP fetch function
    imapread()
