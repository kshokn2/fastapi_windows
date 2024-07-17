# fastapi_windows
Usage in windows

# API
This is the repository for API source.

## Getting Start

How to startup this api
```bash
cd /path/fastapi_linux
python main.py
```

## Sample Requests
1. url (GET method)
   ```bash
   curl -X GET http://vm_ip:8000/get
   ```
2. url (POST method)
   ```
   curl -X POST http://vm_ip:8000/url -H "Content-Type: application/json" -d "{\"user\":\"test_user\",\"data\":\"my_data\"}" 
   ```