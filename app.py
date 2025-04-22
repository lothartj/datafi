from flask import Flask, request, Response, render_template, redirect
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TARGET_URL = os.getenv('TARGET_URL', '')

MOBILE_USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 12; Mobile; rv:100.0) Gecko/100.0 Firefox/100.0",
    "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1"
]

MOBILE_CARRIERS = [
    "T-Mobile", "Vodafone", "AT&T", "Verizon", "Orange", "Airtel", "MTN", "MTC", "Telecom Namibia"
]

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global TARGET_URL
        TARGET_URL = request.form.get('target_url', '').strip()
        if TARGET_URL:
            with open('.env', 'w') as f:
                f.write(f'TARGET_URL="{TARGET_URL}"\n')
            return render_template('index.html', target_url=TARGET_URL, configured=True)
        else:
            return render_template('index.html', error="Please enter a valid URL", target_url='', configured=False)
            
    if TARGET_URL and request.args.get('go') == 'true':
        return redirect(TARGET_URL, code=302)
        
    return render_template('index.html', target_url=TARGET_URL, configured=bool(TARGET_URL))

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path=''):
    if not TARGET_URL:
        return render_template('index.html', error="Please configure the target URL first", target_url='', configured=False)
    
    url = f"{TARGET_URL.rstrip('/')}/{path}"
    
    method = request.method
    
    headers = {key: value for key, value in request.headers if key.lower() not in ('host', 'user-agent', 'x-forwarded-for')}
    
    headers['User-Agent'] = random.choice(MOBILE_USER_AGENTS)
    headers['X-Carrier'] = random.choice(MOBILE_CARRIERS)
    headers['X-Wap-Profile'] = "http://wap.samsungmobile.com/uaprof/GTxxxxxprofile.xml"
    headers['X-Forwarded-For'] = f"106.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
    headers['X-Forwarded-Proto'] = 'https'
    headers['X-Requested-With'] = 'com.android.chrome'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Language'] = 'en-US,en;q=0.5'
    data = request.get_data()
    
    params = request.args
    
    try:
        resp = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            cookies=request.cookies,
            allow_redirects=True,
            stream=True,
            timeout=30 
        )
        response = Response(
            resp.iter_content(chunk_size=1024),
            status=resp.status_code
        )
        for key, value in resp.headers.items():
            if key.lower() not in ('content-encoding', 'transfer-encoding', 'content-length', 'connection'):
                response.headers[key] = value
                
        return response
    except requests.RequestException as e:
        return render_template('error.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 