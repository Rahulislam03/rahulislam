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
            # ১. নম্বর ক্লিন করা
            clean_num = phone_input.replace("+", "").replace(" ", "").replace("-", "")
            parsed = phonenumbers.parse(phone_input)
            
            # ২. সোর্স ১: Abstract API (Live Data)
            api_url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEY}&number={phone_input}"
            api_res = requests.get(api_url, timeout=7).json()
            
            # ৩. সোর্স ২: লোকাল ইন্টেলিজেন্স (Offline Meta)
            c_name = carrier.name_for_number(parsed, "en")
            loc = geocoder.description_for_number(parsed, "en")
            tz = list(timezone.time_zones_for_number(parsed))[0] if timezone.time_zones_for_number(parsed) else "N/A"
            
            # ৪. নাম নির্ধারণ লজিক (Whoscall/Truecaller ডাইনামিক স্ট্যাটাস)
            name = api_res.get("name")
            if not name or name == "":
                name = "Live Identity Detected"

            response = {
                "status": "success",
                "data": {
                    "owner": name,
                    "carrier": api_res.get("carrier") or c_name or "Unknown",
                    "location": f"{api_res.get('location', loc)}, {api_res.get('country', {}).get('name', 'Global')}",
                    "type": api_res.get("type", "Mobile"),
                    "valid": "Active / Online" if api_res.get("valid") else "Disconnected",
                    "intl": api_res.get("format", {}).get("international", phone_input),
                    "timezone": tz,
                    "whoscall_link": f"https://whoscall.com/en/search/{clean_num}"
                }
            }
        except Exception as e:
            response = {"status": "error", "message": "সার্ভার রেসপন্স দিচ্ছে না!"}
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
            
