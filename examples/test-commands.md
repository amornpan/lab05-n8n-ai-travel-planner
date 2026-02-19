# คำสั่งทดสอบ Lab 05: AI Travel Planner Bot

## 1. ทดสอบ OpenWeatherMap API

```bash
# Linux/Mac
curl "https://api.openweathermap.org/data/2.5/weather?q=Bangkok&appid=YOUR_API_KEY&units=metric&lang=th"

# Windows PowerShell
Invoke-RestMethod -Uri "https://api.openweathermap.org/data/2.5/weather?q=Bangkok&appid=YOUR_API_KEY&units=metric&lang=th"
```

## 2. ทดสอบ Geoapify Places API

```bash
# Linux/Mac — ค้นหาสถานที่ท่องเที่ยวรอบ Bangkok (lon=100.5167, lat=13.75)
curl "https://api.geoapify.com/v2/places?categories=tourism.sights&filter=circle:100.5167,13.75,5000&limit=5&apiKey=YOUR_GEOAPIFY_KEY"

# Windows PowerShell
Invoke-RestMethod -Uri "https://api.geoapify.com/v2/places?categories=tourism.sights&filter=circle:100.5167,13.75,5000&limit=5&apiKey=YOUR_GEOAPIFY_KEY"
```

## 3. ทดสอบ OpenRouter API (Gemini Free)

> **หมายเหตุ**: ใน n8n ให้ใช้ **Basic LLM Chain** + **OpenRouter Chat Model** sub-node แทน HTTP Request ตรง คำสั่ง curl ด้านล่างใช้สำหรับทดสอบว่า API key ใช้งานได้

```bash
# Linux/Mac
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_OPENROUTER_KEY" \
  -d '{
    "model": "google/gemma-3-27b-it:free",
    "messages": [
      {"role": "system", "content": "You are a helpful travel planner. Answer in Thai."},
      {"role": "user", "content": "แนะนำที่เที่ยวกรุงเทพ 1 วัน อากาศร้อน 35 องศา"}
    ]
  }'

# Windows CMD
curl https://openrouter.ai/api/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_OPENROUTER_KEY" -d "{\"model\":\"google/gemma-3-27b-it:free\",\"messages\":[{\"role\":\"system\",\"content\":\"You are a helpful travel planner. Answer in Thai.\"},{\"role\":\"user\",\"content\":\"แนะนำที่เที่ยวกรุงเทพ 1 วัน\"}]}"
```

## 4. ทดสอบ Discord Webhook

```bash
# Linux/Mac
curl -X POST https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [{
      "title": "✈️ ทดสอบ Travel Planner",
      "description": "ถ้าเห็นข้อความนี้ แสดงว่า Discord Webhook ใช้งานได้!",
      "color": 15844367
    }]
  }'

# Windows CMD
curl -X POST https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN -H "Content-Type: application/json" -d "{\"embeds\":[{\"title\":\"ทดสอบ Travel Planner\",\"description\":\"Webhook ใช้งานได้!\",\"color\":15844367}]}"
```

## 5. ทดสอบ n8n Webhook (จำลอง bot.py)

> **หมายเหตุ**: bot.py ส่งข้อความดิบไป n8n — AI Extract Info จะแยก city/days ให้เอง

```bash
# Linux/Mac — ข้อความภาษาไทย
curl -X POST http://localhost:5678/webhook-test/travel-planner \
  -H "Content-Type: application/json" \
  -d '{
    "content": "อยากไปเที่ยวเชียงใหม่ 3 วัน",
    "author": {"username": "testuser", "id": "123"},
    "channel_id": "456",
    "guild_id": "789"
  }'

# Linux/Mac — ข้อความภาษาอังกฤษ
curl -X POST http://localhost:5678/webhook-test/travel-planner \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Plan a trip to Tokyo for 5 days",
    "author": {"username": "testuser", "id": "123"},
    "channel_id": "456",
    "guild_id": "789"
  }'

# Windows CMD
curl -X POST http://localhost:5678/webhook-test/travel-planner -H "Content-Type: application/json" -d "{\"content\":\"อยากไปเที่ยวเชียงใหม่ 3 วัน\",\"author\":{\"username\":\"testuser\",\"id\":\"123\"},\"channel_id\":\"456\",\"guild_id\":\"789\"}"
```

## 6. ทดสอบเมืองอื่นๆ

```bash
# Tokyo
curl "https://api.openweathermap.org/data/2.5/weather?q=Tokyo&appid=YOUR_API_KEY&units=metric"

# Chiang Mai
curl "https://api.openweathermap.org/data/2.5/weather?q=Chiang%20Mai&appid=YOUR_API_KEY&units=metric&lang=th"

# Paris
curl "https://api.openweathermap.org/data/2.5/weather?q=Paris&appid=YOUR_API_KEY&units=metric"
```

## เมืองที่ใช้ทดสอบได้

| เมือง | ภาษาอังกฤษ | หมายเหตุ |
|-------|-----------|---------|
| กรุงเทพ | Bangkok | เมืองหลวง ข้อมูลครบ |
| เชียงใหม่ | Chiang Mai | ใช้ %20 แทนช่องว่าง |
| โตเกียว | Tokyo | เมืองใหญ่ ข้อมูลครบ |
| ปารีส | Paris | ทดสอบสภาพอากาศหนาว |
| ลอนดอน | London | ทดสอบฝน |
