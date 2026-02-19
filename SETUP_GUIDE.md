# คู่มือติดตั้ง Lab 05: AI Travel Planner Bot

> ทำตามขั้นตอนด้านล่างทีละข้อ — ใช้เวลาประมาณ 60-90 นาที

---

## สารบัญ

1. [ภาพรวมระบบ](#1-ภาพรวมระบบ)
2. [สร้าง Discord Server + Channel](#2-สร้าง-discord-server--channel)
3. [สร้าง Webhook URL (สำหรับส่งข้อความ)](#3-สร้าง-webhook-url)
4. [สร้าง Bot Application + Token (สำหรับรับข้อความ)](#4-สร้าง-bot-application--token)
5. [เปิด Message Content Intent](#5-เปิด-message-content-intent)
6. [Invite Bot เข้า Server](#6-invite-bot-เข้า-server)
7. [สมัคร OpenWeatherMap API Key](#7-สมัคร-openweathermap-api-key)
8. [สมัคร Geoapify API Key](#8-สมัคร-geoapify-api-key)
9. [สมัคร OpenRouter API Key](#9-สมัคร-openrouter-api-key)
10. [รัน n8n](#10-รัน-n8n)
11. [สร้าง Workflow: Chat Command](#11-สร้าง-workflow-chat-command)
12. [ตั้งค่า bot.py + ทดสอบ](#12-ตั้งค่า-botpy--ทดสอบ)

---

## 1. ภาพรวมระบบ

Lab นี้ใช้ **4 บริการ** ร่วมกัน:

```
Discord Bot (bot.py)           ←→ n8n (Workflow Automation)
                                    ↓
                           OpenWeatherMap API (สภาพอากาศ)
                           Geoapify API (สถานที่ท่องเที่ยว)
                           OpenRouter/Gemini (AI วางแผน)
                                    ↓
                            Discord Channel (ผลลัพธ์)
```

### สิ่งที่ต้องมี:
| รายการ | หน้าที่ | ค่าใช้จ่าย |
|--------|---------|------------|
| Discord Account | สร้าง Server + Bot | ฟรี |
| OpenWeatherMap API Key | ข้อมูลสภาพอากาศ | ฟรี (1,000 calls/day) |
| Geoapify API Key | ข้อมูลสถานที่ท่องเที่ยว | ฟรี (3,000 calls/day) |
| OpenRouter API Key | เรียก Gemini AI | ฟรี (free models) |
| n8n | สร้าง Workflow | ฟรี (self-host) |
| Python 3.8+ | รัน bot.py | ฟรี |

---

## 2. สร้าง Discord Server + Channel

1. เปิด Discord → กดปุ่ม **+** ด้านซ้าย → **Create My Own**
2. เลือก **For me and my friends**
3. ตั้งชื่อ Server เช่น `Lab05-Travel-Planner`
4. สร้าง Text Channel ชื่อ `#travel-plans`
   - คลิกขวาที่ Category → **Create Channel**
   - ตั้งชื่อ `travel-plans` → Create

---

## 3. สร้าง Webhook URL

Webhook URL ใช้สำหรับ **ส่งข้อความจาก n8n ไป Discord**

1. ไปที่ Channel `#travel-plans`
2. คลิก **Edit Channel** (ไอคอนเฟือง)
3. ไปที่ **Integrations** → **Webhooks** → **New Webhook**
4. ตั้งชื่อเช่น `Travel Planner Bot`
5. คลิก **Copy Webhook URL**
6. **เก็บ URL นี้ไว้** — จะใช้ใน n8n HTTP Request Node

> **รูปแบบ URL**: `https://discord.com/api/webhooks/123456/abcdef...`

---

## 4. สร้าง Bot Application + Token

Bot Token ใช้สำหรับ **รับข้อความจาก Discord ผ่าน bot.py**

1. ไปที่ [Discord Developer Portal](https://discord.com/developers/applications)
2. กด **New Application** → ตั้งชื่อ `Travel Planner Bot`
3. ไปที่เมนู **Bot** ด้านซ้าย
4. กด **Reset Token** → **Copy Token**
5. **เก็บ Token นี้ไว้** — จะใช้ใน `bot.py`

> **สำคัญ**: ห้ามแชร์ Bot Token กับใคร! ถ้าหลุด ให้ Reset ทันที

---

## 5. เปิด Message Content Intent

**จำเป็น!** ไม่งั้น Bot จะอ่านข้อความของ user ไม่ได้

1. ใน Discord Developer Portal → Application ที่สร้าง
2. ไปที่เมนู **Bot**
3. เลื่อนลงหา **Privileged Gateway Intents**
4. เปิด **Message Content Intent** ✅
5. กด **Save Changes**

---

## 6. Invite Bot เข้า Server

1. ไปที่เมนู **OAuth2** → **URL Generator**
2. เลือก Scopes: ✅ `bot`
3. เลือก Bot Permissions: ✅ `Send Messages`, ✅ `Read Message History`
4. คัดลอก **Generated URL** ด้านล่าง
5. เปิด URL ในเบราว์เซอร์ → เลือก Server → **Authorize**

---

## 7. สมัคร OpenWeatherMap API Key

1. ไปที่ [openweathermap.org/api](https://openweathermap.org/api)
2. กด **Sign Up** สร้างบัญชี (ฟรี)
3. ยืนยัน email
4. ไปที่ **API Keys** → คัดลอก key
5. **รอ 10 นาที** หลังสมัคร (key ต้อง activate ก่อน)

> **ทดสอบ**:
> ```
> curl "https://api.openweathermap.org/data/2.5/weather?q=Bangkok&appid=YOUR_KEY&units=metric"
> ```
> ถ้าได้ JSON กลับมา = สำเร็จ!

---

## 8. สมัคร Geoapify API Key

1. ไปที่ [myprojects.geoapify.com](https://myprojects.geoapify.com)
2. สร้างบัญชี (ฟรี)
3. กด **Create New Project** → ตั้งชื่อ `Lab05`
4. คัดลอก API Key

> **ทดสอบ**:
> ```
> curl "https://api.geoapify.com/v2/places?categories=tourism.sights&filter=circle:100.5167,13.75,5000&limit=3&apiKey=YOUR_KEY"
> ```
> ถ้าได้ JSON กลับมา = สำเร็จ!

---

## 9. สมัคร OpenRouter API Key

1. ไปที่ [openrouter.ai](https://openrouter.ai)
2. สร้างบัญชี (ฟรี — ใช้ Google/GitHub login ได้)
3. ไปที่ **Keys** → **Create Key**
4. ตั้งชื่อ `lab05` → คัดลอก key

> **Model ฟรีที่ใช้**: `google/gemma-3-27b-it:free`
>
> **ทดสอบ**:
> ```bash
> curl https://openrouter.ai/api/v1/chat/completions \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer YOUR_KEY" \
>   -d '{"model":"google/gemma-3-27b-it:free","messages":[{"role":"user","content":"Hello"}]}'
> ```

---

## 10. รัน n8n

### วิธีที่ 1: Docker (แนะนำ)
```bash
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

### วิธีที่ 2: npx
```bash
npx n8n
```

### วิธีที่ 3: n8n Cloud / n8n Hub
ใช้ URL ที่ผู้สอนให้

เปิด n8n ที่: `http://localhost:5678`

---

## 11. สร้าง Workflow: Chat Command

### 11.1 เพิ่ม Webhook Node
1. กด **+** → ค้นหา `Webhook`
2. ตั้งค่า:
   - **HTTP Method**: POST
   - **Path**: `travel-planner`
3. จด URL ไว้: `http://localhost:5678/webhook-test/travel-planner`

### 11.2 เพิ่ม Basic LLM Chain — AI Extract Info ⭐ หัวใจ Agentic!
> **Node นี้คือหัวใจของ Agentic Workflow** — ให้ AI แยก city/days จากข้อความอิสระของ user

1. กด **+** → ค้นหา `Basic LLM Chain`
2. ตั้งค่า Prompt:
   - **Prompt Type**: Define
   - **Text**:
```
You are a helpful assistant that extracts travel information from user messages. Extract the city name and number of travel days from the following message. If the user doesn't specify the number of days, default to 3. The city name MUST be in English.

IMPORTANT: You MUST respond with ONLY a valid JSON object in this exact format, nothing else:
{"city": "CityName", "days": 3}

Examples:
- "อยากไปเที่ยวเชียงใหม่ 3 วัน" → {"city": "Chiang Mai", "days": 3}
- "Plan a trip to Tokyo for 5 days" → {"city": "Tokyo", "days": 5}
- "อยากไปโตเกียว" → {"city": "Tokyo", "days": 3}
- "แนะนำที่เที่ยวกรุงเทพ" → {"city": "Bangkok", "days": 3}

User message: {{ $json.body.content }}

Respond with ONLY the JSON object:
```
3. เพิ่ม **OpenRouter Chat Model** sub-node:
   - คลิกที่ **+** ใต้ Basic LLM Chain → เลือก **OpenRouter Chat Model**
   - เลือก Model: `google/gemma-3-27b-it:free`
   - ตั้งค่า **Credentials**: กด **Create New** → ใส่ OpenRouter API Key
4. กด **Test step** → ดูว่า AI ตอบเป็น JSON ถูกต้อง

### 11.3 เพิ่ม Code Node — Parse Extract Result
> แปลง AI response เป็น JSON ที่ node ถัดไปใช้ได้

1. กด **+** → ค้นหา `Code`
2. ใส่ JavaScript:
```javascript
// Parse AI Extract Info response to get city and days
const aiResponse = $input.first().json;
const text = aiResponse.text || aiResponse.output || JSON.stringify(aiResponse);

let city = 'Bangkok';
let days = 3;

try {
  const jsonMatch = text.match(/\{[^}]+\}/);
  if (jsonMatch) {
    const parsed = JSON.parse(jsonMatch[0]);
    city = parsed.city || 'Bangkok';
    days = parsed.days || 3;
  }
} catch (e) {
  city = 'Bangkok';
  days = 3;
}

days = Math.min(Math.max(days, 1), 7);

return [{ json: { city, days } }];
```

### 11.4 เพิ่ม HTTP Request — Get Weather
1. กด **+** → ค้นหา `HTTP Request`
2. ตั้งค่า:
   - **Method**: GET
   - **URL**: `https://api.openweathermap.org/data/2.5/weather?q={{ $json.city }}&appid=YOUR_API_KEY&units=metric&lang=th`

> **สังเกต**: URL ใช้ `{{ $json.city }}` ที่ได้จาก Parse Extract Result

### 11.5 เพิ่ม HTTP Request — Get Places
1. กด **+** → ค้นหา `HTTP Request`
2. ตั้งค่า:
   - **Method**: GET
   - **URL**: `https://api.geoapify.com/v2/places?categories=tourism.sights&filter=circle:{{ $json.coord.lon }},{{ $json.coord.lat }},5000&limit=5&apiKey=YOUR_GEOAPIFY_KEY`

### 11.6 เพิ่ม Basic LLM Chain — AI Plan Trip
1. กด **+** → ค้นหา `Basic LLM Chain`
2. ตั้งค่า Prompt:
   - **Prompt Type**: Define
   - **Text**:
```
You are an expert travel planner. Create a day-by-day travel itinerary in Thai language based on weather data and tourist attractions provided. For each day, suggest morning, afternoon, and evening activities. Consider the weather when recommending outdoor vs indoor activities. Keep each day's plan concise.

Plan a trip to the city.

Weather: Temperature {{ $json.main.temp }}°C, Humidity {{ $json.main.humidity }}%, Condition: {{ $json.weather[0].description }}.

Tourist attractions nearby:
{{ $json.features ? $json.features.map(f => f.properties.name).join(', ') : 'No data' }}

Please create the itinerary.
```
3. เพิ่ม **OpenRouter Chat Model** sub-node:
   - คลิกที่ **+** ใต้ Basic LLM Chain → เลือก **OpenRouter Chat Model**
   - เลือก Model: `google/gemma-3-27b-it:free`
   - ใช้ **Credentials** เดิมที่สร้างไว้

### 11.7 เพิ่ม Code Node — Format Embed
1. กด **+** → ค้นหา `Code`
2. สร้าง Discord Embed จากผลลัพธ์ AI

### 11.8 เพิ่ม HTTP Request — Send to Discord
1. กด **+** → ค้นหา `HTTP Request`
2. ตั้งค่า:
   - **Method**: POST
   - **URL**: Discord Webhook URL ของคุณ
   - **Body**: `{{ $json }}`

### 11.9 เชื่อม Node ทั้ง 8 ตามลำดับ
```
Webhook → AI Extract Info → Parse Extract Result → Get Weather → Get Places → AI Plan Trip → Format Embed → Send to Discord
```

---

## 12. ตั้งค่า bot.py + ทดสอบ

### 12.1 ติดตั้ง dependencies
```bash
pip install discord.py aiohttp
```

### 12.2 แก้ไข bot.py
เปิดไฟล์ `bot.py` แล้วใส่ค่า:
```python
BOT_TOKEN = "ใส่_Bot_Token_ของคุณ"
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/travel-planner"
```

> **หมายเหตุ**: ตอน production ให้เปลี่ยน `/webhook-test/` เป็น `/webhook/`

### 12.3 รัน bot
```bash
python bot.py
```

### 12.4 ทดสอบใน Discord
พิมพ์อะไรก็ได้ใน `#travel-plans`:
```
อยากไปเที่ยวเชียงใหม่ 3 วัน
Plan a trip to Tokyo for 5 days
แนะนำที่เที่ยวกรุงเทพ
```

> **สังเกต**: bot.py ส่งข้อความดิบไป n8n — AI Extract Info จะแยก city/days ให้เอง!

### 12.5 Export Workflow
1. ใน n8n กดเมนู **...** → **Export**
2. เลือก **Download as JSON**
3. นำไฟล์ JSON มาวางทับ `workflow.json`

### 12.6 รัน Tests
```bash
pytest tests/ -v --tb=short
```

ต้องผ่านทั้ง 10 tests (100 คะแนน)

---

## Troubleshooting

| อาการ | สาเหตุ | วิธีแก้ |
|-------|--------|---------|
| Bot ไม่ตอบ | ไม่ได้เปิด Message Content Intent | ดูข้อ 5 |
| n8n รับ webhook ไม่ได้ | ใช้ path ผิด | ดูข้อ 11.1 |
| OpenWeather 401 | API key ยังไม่ active | รอ 10 นาที |
| AI แยก city ผิด | Prompt ไม่ชัด | ปรับ prompt ของ AI Extract Info |
| Parse Extract ได้ Bangkok ตลอด | AI ไม่ตอบเป็น JSON | ตรวจ prompt ว่าบอกให้ตอบ JSON เท่านั้น |
| Gemini ตอบช้า | free model มี latency สูง | เพิ่ม timeout เป็น 60s |
| Discord embed ไม่ขึ้น | JSON format ผิด | ตรวจสอบ Content-Type |
| pytest fail | ยังไม่ได้ export workflow | ทำตามข้อ 12.5 |
