# -*- coding: utf-8 -*-
#Author: vimystic@gmail.com
#put this file in your blog repo
#send mails in the following format
#-------------------------------------
#*****name\n   ->the desired name of md file
#*****title\n  ->title of the blog
#write your mark down file 

import getpass, imaplib, email, re, os, datetime, time


def remove_cret(str):
    r=re.compile(r"(.*)\r(.*)",re.DOTALL)
    m=r.match(str)
    while m!=None:
        str=''.join([m.group(1),m.group(2)])
        m=r.match(str)
    return str



def fnu():
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    M.login('send your md file to this mailbox', 'passwd for the mailbox')#add your info here
    M.select()
    typ, data = M.search(None, '(UNSEEN FROM "the mail box you send your blog")') #add your info here
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        mailText=data[0][1]
        r=re.compile(r"(.+charset=)(.+)(\nContent.+)",re.DOTALL)
        m=r.match(mailText)
        charset=m.group(2)
        msg=email.message_from_string(mailText)
        for part in msg.walk():
            if not part.is_multipart():
                contenttype = part.get_content_type()
                if contenttype in ['text/plain']:
                    
                    mailContent = part.get_payload(decode=True).decode(charset)
                    r=re.compile(r"(.+)name(.+)title(.+)(--.+)",re.DOTALL)
                    m=r.match(mailContent)
                    name = m.group(1)
                    title = m.group(2)
                    title = title[2:len(title)]
                    blograw = m.group(3)
                    blograw = remove_cret(blograw)
                    rakec=''.join(['rake post title=\"',name,'\"'])
                    os.system(rakec)
                    date=datetime.date.today().isoformat()
                    filename=''.join(['./_posts/',date,'-',name,'.md'])
                    newblog=open(filename,'w+b')
                    meta=''.join([u"---\nlayout: post\ntitle: \"",title,u"\"\n---\n{% include JB/setup %}\n"])
                    cont=''.join([meta,blograw])
                    newblog.write(cont.encode("utf-8"))
                    newblog.close()
                    gitc='git add .'
                    os.system(gitc)
                    gitc='git commit -m "email autoupdate"'
                    os.system(gitc)
                    gitc='git push'
                    os.system(gitc)
    M.close()
    M.logout()

while 1:
    fnu()
    time.sleep(300)


