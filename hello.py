import requests
import json

url = "https://api-bakong.nbc.gov.kh/v1/check_transaction_by_md5"

payload = json.dumps({
  "md5": "3d5000a0da5a635d0893ff8c406d4807"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiMDU2N2I3NzQ5YWU1NGMzOSJ9LCJpYXQiOjE3MTc0ODc3NDQsImV4cCI6MTcyNTI2Mzc0NH0.MxKhpjXeFzwGuMTA9PDk_Gd0sykwBgdZ1hIj022pC8c'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
