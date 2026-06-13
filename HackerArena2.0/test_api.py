import requests, io
from PIL import Image

img = Image.new('RGB', (100, 100), color='red')
buf = io.BytesIO()
img.save(buf, format='JPEG')
buf.seek(0)

resp = requests.post('http://localhost:8000/api/v1/analyze', files={'file': ('test.jpg', buf, 'image/jpeg')})
print('Status:', resp.status_code)
print('Response:', resp.text[:1000])
