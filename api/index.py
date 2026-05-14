from http.server import BaseHTTPRequestHandler
import json
import requests
import uuid

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        phone_input = data.get("number")
        
        # নম্বর ক্লিন করা (017... ফরম্যাটে নিয়ে আসা)
        clean_num = phone_input.replace("+", "").replace(" ", "").replace("-", "").strip()
        if clean_num.startswith("88"):
            target_num = clean_num[2:]
        else:
            target_num = clean_num

        # SSLCommerz Sandbox Credentials (Real 100% Data Source)
        STORE_ID = "testbox"
        STORE_PASS = "testbox@ssl"
        
        try:
            # SSLCommerz API Endpoint
            api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
            
            payload = {
                'store_id': STORE_ID,
                'store_passwd': STORE_PASS,
                'total_amount': '10.00',
                'currency': 'BDT',
                'tran_id': str(uuid.uuid4())[:10], # ইউনিক ট্রানজেকশন আইডি
                'success_url': 'https://your-site.vercel.app/success',
                'fail_url': 'https://your-site.vercel.app/fail',
                'cancel_url': 'https://your-site.vercel.app/cancel',
                'cus_name': 'ID_VERIFICATION_NODE',
                'cus_email': 'verify@nexus.com',
                'cus_phone': target_num, # টার্গেট নম্বর
                'cus_add1': 'Dhaka',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'product_name': 'Identity_Check',
                'product_category': 'Service',
                'product_profile': 'general'
            }

            response = requests.post(api_url, data=payload, timeout=10)
            res_data = response.json()

            if res_data.get('status') == 'SUCCESS':
                # সাকসেস হলে আমরা গেটওয়ে ইউআরএল এবং সেশন কি পাঠাবো
                final_response = {
                    "status": "success",
                    "gateway_url": res_data.get('GatewayPageURL'),
                    "session_id": res_data.get('sessionkey'),
                    "tran_id": payload['tran_id'],
                    "target": target_num
                }
            else:
                final_response = {"status": "error", "message": "GATEWAY_REJECTED"}
                
        except Exception as e:
            final_response = {"status": "error", "message": "CONNECTION_FAILED"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(final_response).encode())
