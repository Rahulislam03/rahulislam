from http.server import BaseHTTPRequestHandler
import json
import requests
import uuid

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            phone = data.get("number", "01700000000")

            # Aamarpay Sandbox API & Credentials
            api_url = "https://sandbox.aamarpay.com/jsonpost.php"
            
            payload = {
                "store_id": "amarpaytest",
                "signature_key": "dbb74894e82415a2f7ff0ec3a97e4183",
                "cus_name": "Islam Rahul",
                "cus_email": "rahul@mixveo.com",
                "cus_phone": phone,
                "amount": "10.00",
                "currency": "BDT",
                "tran_id": f"TXN_{uuid.uuid4().hex[:8].upper()}",
                "desc": "System Verification",
                "success_url": "https://www.google.com",
                "fail_url": "https://www.google.com",
                "cancel_url": "https://www.google.com",
                "type": "json"
            }

            r = requests.post(api_url, json=payload, timeout=15)
            res = r.json()

            # AmarPay সরাসরি পেমেন্ট ইউআরএল পাঠায়
            if res.get('payment_url'):
                output = {"status": "success", "url": res.get('payment_url')}
            else:
                output = {"status": "error", "message": "Aamarpay Sandbox is Offline"}

        except Exception as e:
            output = {"status": "error", "message": "Connection Lost"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(output).encode())
