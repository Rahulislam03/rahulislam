from http.server import BaseHTTPRequestHandler
import json
import requests
import phonenumbers
from phonenumbers import geocoder, carrier

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        phone_input = data.get("number")
        
        # তোমার দেওয়া API Key এখানে সেট করা হয়েছে
        API_KEY = "a8c9306379ea4c2c8380149ad392b7cd" 
        
        try:
            # পাইথন লাইব্রেরি দিয়ে বেসিক চেক
            parsed = phonenumbers.parse(phone_input)
            
            # Abstract API কল (নাম ও বিস্তারিত তথ্যের জন্য)
            api_url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEY}&number={phone_input}"
            api_res = requests.get(api_url).json()
            
            # API থেকে প্রাপ্ত তথ্য গুছিয়ে নেওয়া
            response = {
                "status": "success",
                "data": {
                    "owner": api_res.get("name") if api_res.get("name") else "Private/Unknown",
                    "carrier": api_res.get("carrier") if api_res.get("carrier") else carrier.name_for_number(parsed, "en"),
                    "location": f"{api_res.get('location', 'N/A')}, {api_res.get('country', {}).get('name', 'Global')}",
                    "type": api_res.get("type", "Mobile"),
                    "format": api_res.get("format", {}).get("international", phone_input),
                    "valid": "Active" if api_res.get("valid") else "Inactive"
                }
            }
        except Exception as e:
            response = {"status": "error", "message": "Information not found or API limit reached!"}
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        
