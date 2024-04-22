from flask import Flask, request, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import socket
import tldextract
import whois
from datetime import datetime
import pickle
import numpy as np
import tldextract
import whois
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
import socket
app = Flask(__name__)

def extract_website_features(url):
    # Extract domain and subdomain
    domain_info = tldextract.extract(url)
    domain = domain_info.domain
    subdomain = domain_info.subdomain

    #IP address
    ip_address = None
    try:
        ip_address = socket.gethostbyname(domain)
    except socket.gaierror:
        pass

    # domain age
    domain_age = None
    try:
        whois_info = whois.whois(domain)
        creation_date = whois_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            domain_age = (datetime.now() - creation_date).days
    except whois.parser.PywhoisError:
        pass

    # Define soup outside the try block
    soup = None
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
    except requests.exceptions.RequestException:
        pass

    # Initialize features
    url_length = len(url)
    url_depth = url.count('/')
    redirection = False
    uses_https = url.startswith('https')
    dns_record = bool(ip_address)
    iframe_count = 0
    mouse_over = False
    right_click = False
    web_forwards = False

    # Update features if soup is not None
    if soup:
        redirection = len(soup.find_all('meta', attrs={'http-equiv': 'refresh'})) > 0
        iframe_count = len(soup.find_all('iframe'))
        mouse_over = 'onmouseover' in html_content
        right_click = 'event.button==2' in html_content
        web_forwards = len(soup.find_all('script', string=re.compile('window.location.href'))) > 0

    # Adjust URL depth
    url_length = 1 if url_length > 20 else 0
    return {
        'Have_IP': bool(ip_address),
        'Have_At': '@' in url,
        'URL_Length': url_length,
        'URL_Depth': url_depth,
        'Redirection': redirection,
        'https_Domain': uses_https,
        'Tiny_URL': url_length <= 20,
        'Prefix/Suffix': '-' in url or '_' in url,
        'DNS_Record': dns_record,
        'Web_traffic': None,
        'Domain_Age': domain_age,
        'Domain_End': 'com' in url,
        'iFrame': iframe_count > 0,
        'Mouse_Over': mouse_over,
        'Right_Click': right_click,
        'Web_Forwards': web_forwards,
    }
