from http.server import BaseHTTPRequestHandler
import json
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        phone_input = data.get("number")
        
        # তোমার Abstract API Key
        API_KEY = "a8c9306379ea4c2c8380149ad392b7cd" 
        
        try:
            # ক্লিন নম্বর তৈরি (যেমন: 88017...)
            clean_num = phone_input.replace("+", "").replace(" ", "").replace("-", "")
            parsed = phonenumbers.parse(phone_input)
            
            # Abstract API থেকে তথ্য সংগ্রহ
            api_url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEY}&number={phone_input}"
            api_res = requests.get(api_url).json()
            
            # নাম হ্যান্ডলিং লজিক
            raw_name = api_res.get("name")
            display_name = raw_name if raw_name else "Identity Hidden by Provider"
            
            response = {
                "status": "success",
                "data": {
                    "owner": display_name,
                    "carrier": api_res.get("carrier") or carrier.name_for_number(parsed, "en"),
                    "location": f"{api_res.get('location', 'N/A')}, {api_res.get('country', {}).get('name', 'Global')}",
                    "type": api_res.get("type", "Mobile"),
                    "valid": "Active" if api_res.get("valid") else "Inactive",
                    "intl": api_res.get("format", {}).get("international", phone_input),
                    "tz": list(timezone.time_zones_for_number(parsed))[0],
                    "tc_url": f"https://www.truecaller.com/search/db/{clean_num}"
                }
            }
        except Exception as e:
            response = {"status": "error", "message": "Connection Error!"}
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
            
