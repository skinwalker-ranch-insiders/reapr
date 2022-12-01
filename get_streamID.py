#!/usr/bin/python3
import mechanize
import re
from bs4 import BeautifulSoup
from settings import s_login, s_password
import urllib.request as urllib2 
import http.cookiejar as cookielib 

def get_streamID():
    user_agent = [('User-agent','Mozilla/5.0 (X11;U;Linux 2.4.2.-2 i586; en-us;m18) Gecko/200010131 Netscape6/6.01')]

    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders=user_agent
    br.open("https://skinwalker-ranch.com/ranch-webcam-livestream/")

    br.select_form(nr=0)
    br.form['log'] = s_login
    br.form['pwd'] = s_password 
    br.submit()

    soup = BeautifulSoup(br.response().read(), features="html5lib")
    for item in soup.find_all('iframe'):
        if 'embed' in item.get('src'):
            stream_url = item.get('src')

    strip_url_end = stream_url.rstrip("&embed_domain=skinwalker-ranch.com")
    stream_ID = strip_url_end.strip("https://www.youtube.com/live_chat?v=")
    return(stream_ID)
