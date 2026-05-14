from http.server import BaseHTTPRequestHandler
import json
import phonenumbers
from phonenumbers import geocoder, carrier

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        phone_input = data.get("number")
        try:
            parsed = phonenumbers.parse(phone_input)
            response = {
                "status": "success",
                "data": {
                    "valid": "সক্রিয়" if phonenumbers.is_valid_number(parsed) else "নিষ্ক্রিয়",
                    "location": geocoder.description_for_number(parsed, "en"),
                    "carrier": carrier.name_for_number(parsed, "en")
                }
            }
        except:
            response = {"status": "error", "message": "ভুল নম্বর!"}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
          
