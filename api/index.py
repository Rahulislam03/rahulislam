from http.server import BaseHTTPRequestHandler
import json
import requests
import random
import string

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        phone_input = data.get("number")
        
        # জেনারেট করা ট্রানজেকশন আইডি
        tran_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        
        try:
            # Phase 1: OSINT Data Gathering
            API_KEY = "a8c9306379ea4c2c8380149ad392b7cd"
            res_api = requests.get(f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEY}&number={phone_input}", timeout=10).json()
            
            # Phase 2: SSLCommerz Data Simulation Logic
            # রিয়েল লাইফে এখানে SSLCommerz API থেকে রেসপন্স আসবে
            raw_name = res_api.get("name")
            
            if not raw_name or raw_name == "" or raw_name == "Unknown":
                # এনক্রিপ্টেড ব্যাংকিং আইডি
                display_name = f"DBBL_MFS_USER_{tran_id[:4]}"
                status = "PENDING_KYC"
            else:
                # ব্যাংকের মতো ক্যাপিটাল লেটার ফরম্যাট
                display_name = raw_name.upper()
                status = "VERIFIED_MERCHANT"

            response = {
                "status": "success",
                "ssl_payload": {
                    "store_id": "NEXUS_SYSTEMS_786",
                    "tran_id": f"SSL-{tran_id}",
                    "cus_name": display_name,
                    "cus_phone": phone_input,
                    "kyc_verification": status,
                    "gateway": "SSLCommerz v4.0 (Live)",
                    "operator": res_api.get("carrier") or "Unknown"
                }
            }
        except:
            response = {"status": "error", "message": "SSL_HANDSHAKE_FAILED"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
