# Lab 05: AI Travel Planner Bot — Agentic Workflow with n8n

> **n8n + Discord Bot + OpenRouter (Gemini AI) + OpenWeatherMap + Geoapify**

## วัตถุประสงค์การเรียนรู้

เมื่อทำ Lab นี้สำเร็จ นักศึกษาจะสามารถ:

1. **เข้าใจ Agentic Workflow** — ใช้ AI/LLM เป็นตัวตัดสินใจในกระบวนการอัตโนมัติ
2. **เรียก LLM API ผ่าน n8n** — ส่ง prompt ไป OpenRouter/Gemini และรับผลลัพธ์
3. **ออกแบบ Prompt Engineering** — เขียน system/user message ที่ได้ผลลัพธ์ตรงประเด็น
4. **ให้ AI แยกข้อมูลจากข้อความ** — AI Extract Info จากข้อความอิสระของ user
5. **รวมข้อมูลหลายแหล่ง** — ดึง weather + places แล้วส่งให้ AI สังเคราะห์
6. **สร้าง Workflow แบบ Chat Command** — ใช้ Webhook รับข้อความจาก Discord Bot
7. **จัดรูปแบบ Discord Embed** — แสดงผลลัพธ์ AI อย่างสวยงามใน Discord
8. **จัดการ API Key อย่างปลอดภัย** — ใช้ Environment Variables ไม่ commit ลง Git

---

## โจทย์

### Chat Command (ถามอะไรก็ได้)

สร้าง Workflow ที่ตอบข้อความจาก Discord Bot:
1. รับข้อความจาก bot.py (พิมพ์อะไรก็ได้เกี่ยวกับการท่องเที่ยว)
2. **AI แยกข้อมูล** — ใช้ AI Extract Info ดึง city/days จากข้อความอิสระ
3. ดึงข้อมูลสภาพอากาศของเมืองที่ AI แยกได้
4. ดึงสถานที่ท่องเที่ยวใกล้เคียง
5. ส่งข้อมูลทั้งหมดให้ Gemini AI วางแผนทริปรายวัน
6. จัดรูปแบบเป็น Discord Embed แล้วส่งกลับ

---

## สถาปัตยกรรม

```
Webhook (รับข้อความดิบจาก bot.py)
    ↓
AI Extract Info (Basic LLM Chain + OpenRouter Chat Model) ← Agentic! แยก city/days
    ↓
Parse Extract Result (Code Node) ← แปลง AI response เป็น JSON
    ↓
Get Weather (HTTP → OpenWeatherMap)
    ↓
Get Places (HTTP → Geoapify)
    ↓
AI Plan Trip (Basic LLM Chain + OpenRouter Chat Model) ← Agentic!
    ↓
Format Embed (Code Node)
    ↓
Send to Discord (HTTP → Discord Webhook)
```

---

## Node ที่ต้องมี (8 Nodes + 2 Sub-nodes)

| # | Node Name | Type | หน้าที่ |
|---|-----------|------|---------|
| 1 | Webhook | Webhook | รับข้อความดิบจาก bot.py |
| 2 | AI Extract Info | **Basic LLM Chain** | **AI แยก city/days จากข้อความ** |
| ↳ | OpenRouter Chat Model | Sub-node (LLM) | เชื่อมต่อ OpenRouter/Gemini |
| 3 | Parse Extract Result | Code | แปลง AI response เป็น JSON |
| 4 | Get Weather | HTTP Request | ดึงข้อมูลอากาศ |
| 5 | Get Places | HTTP Request | ดึงสถานที่ท่องเที่ยว |
| 6 | AI Plan Trip | **Basic LLM Chain** | AI วางแผนทริป |
| ↳ | OpenRouter Chat Model | Sub-node (LLM) | เชื่อมต่อ OpenRouter/Gemini |
| 7 | Format Embed | Code | จัดรูปแบบ Discord Embed |
| 8 | Send to Discord | HTTP Request | ส่งข้อความไป Discord |

> **หมายเหตุ**: OpenRouter Chat Model เป็น sub-node ที่เชื่อมเข้ากับ Basic LLM Chain ผ่าน `ai_languageModel` connection
> Workflow ไม่มี IF Node — รับข้อความอะไรก็ได้จาก user แล้ว AI จะแยกข้อมูลและวางแผนให้เอง

---

## ทำไมต้องให้ AI แยกข้อมูล?

**ปัญหาเดิม**: User ต้องพิมพ์ตาม format เช่น `!plan Bangkok 3` — bot.py จะ parse city/days ส่งให้ n8n

**แนวทางใหม่ (Agentic)**: User พิมพ์อะไรก็ได้ เช่น:
- `อยากไปเที่ยวเชียงใหม่ 3 วัน`
- `Plan a trip to Tokyo for 5 days`
- `แนะนำที่เที่ยวกรุงเทพ`
- `I want to visit Paris`

**AI Extract Info** node จะแยกข้อมูลเอง:
```json
{"city": "Chiang Mai", "days": 3}
```

นี่คือ **Agentic Workflow** จริงๆ — AI เป็นตัวตัดสินใจ ไม่ใช่ rule-based!

---

## API Reference

### 1. OpenWeatherMap (สภาพอากาศ)
- **URL**: `https://api.openweathermap.org/data/2.5/weather?q={{ $json.city }}&appid=YOUR_API_KEY&units=metric&lang=th`
- **Method**: GET
- **API Key**: สมัครฟรีที่ [openweathermap.org](https://openweathermap.org/api)

### 2. Geoapify Places (สถานที่ท่องเที่ยว)
- **URL**: `https://api.geoapify.com/v2/places?categories=tourism.sights&filter=circle:{lon},{lat},{radius}&limit=5&apiKey={API_KEY}`
- **Method**: GET
- **API Key**: สมัครฟรีที่ [myprojects.geoapify.com](https://myprojects.geoapify.com)

### 3. OpenRouter (Gemini AI) — ผ่าน Basic LLM Chain
- **Node**: Basic LLM Chain + OpenRouter Chat Model (sub-node)
- **Model**: `google/gemma-3-27b-it:free`
- **Credentials**: ตั้งค่า OpenRouter API Key ใน n8n Credentials
- **API Key**: สมัครฟรีที่ [openrouter.ai](https://openrouter.ai)
- **Docs**: [n8n Basic LLM Chain](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.chainllm/) | [OpenRouter Chat Model](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatopenrouter/)

### 4. Discord Webhook
- **URL**: `https://discord.com/api/webhooks/{ID}/{TOKEN}`
- **Method**: POST

---

## Discord Embed — สีตามสภาพอากาศ

| สภาพอากาศ | Emoji | สี | Decimal |
|-----------|-------|-----|---------|
| Clear (แจ่มใส) | ☀️ | Gold | 15844367 |
| Clouds (มีเมฆ) | ☁️ | Gray | 9807270 |
| Rain (ฝนตก) | 🌧️ | Blue | 3447003 |
| Drizzle (ฝนปรอย) | 🌦️ | Blue | 3447003 |
| Thunderstorm (พายุฝน) | ⛈️ | Purple | 7419530 |
| Snow (หิมะ) | ❄️ | White-Blue | 12370112 |
| Default | 🌤️ | Teal | 1752220 |

---

## เกณฑ์คะแนน (100 คะแนน)

| Test | คะแนน | ตรวจสอบ |
|------|--------|---------|
| test_01: workflow.json exists | 8 | มีไฟล์ workflow.json |
| test_02: valid JSON | 8 | เป็น JSON + มี nodes, connections |
| test_03: Webhook Node | 10 | มี Webhook Node |
| test_04: Webhook POST | 8 | Webhook ใช้ POST method |
| test_05: Weather API | 10 | HTTP Node เรียก openweathermap.org |
| test_06: AI Node | 14 | Basic LLM Chain + OpenRouter หรือ HTTP Request |
| test_07: Places API | 10 | HTTP Node เรียก geoapify.com |
| test_08: Code Node | 10 | มี Code Node |
| test_09: Discord Webhook | 10 | HTTP Node ส่ง Discord |
| test_10: Embed Format | 12 | Code มี embed, fields, color, travel data |
| **รวม** | **100** | |

> **ทดสอบ**: `pytest tests/ -v --tb=short`

---

## Common Errors

| ปัญหา | สาเหตุ | วิธีแก้ |
|--------|--------|---------|
| OpenRouter 401 Unauthorized | API key ไม่ถูกต้อง | ตรวจสอบ API key ใน n8n Credentials |
| OpenWeather 401 | API key ไม่ถูกหรือยังไม่ active | รอ 10 นาทีหลังสมัคร |
| Geoapify 403 | API key ผิดหรือเกิน quota | ตรวจสอบ key + quota |
| Discord 400 Bad Request | JSON format ผิด | ตรวจสอบ Content-Type: application/json |
| LLM Timeout | Gemini ตอบช้า | เพิ่ม timeout ใน OpenRouter Chat Model options |
| AI แยก city ผิด | Prompt ไม่ชัด | ปรับ prompt ของ AI Extract Info ให้เฉพาะเจาะจง |
| AI ตอบไม่ตรง | Prompt ไม่ชัด | ปรับ system message ให้เฉพาะเจาะจง |
| Webhook 404 | ใช้ /webhook-test/ หลัง Activate | เปลี่ยนเป็น /webhook/ |
| bot.py อ่านข้อความไม่ได้ | ไม่ได้เปิด Message Content Intent | เปิดใน Discord Developer Portal |
| JSON parse error ใน Parse Extract | AI ตอบไม่เป็น JSON | Code Node มี fallback เป็น Bangkok/3 วัน |

---

## โครงสร้างโปรเจกต์

```
lab05-n8n-ai-travel-planner/
├── .github/workflows/
│   └── autograding.yml        ← CI/CD Pipeline
├── bot.py                     ← Discord Bot (Python) — ส่งข้อความดิบ
├── workflow.json               ← [นักศึกษาทำ] Export จาก n8n
├── requirements.txt            ← Python Dependencies
├── README.md                   ← เอกสารนี้
├── SETUP_GUIDE.md              ← คู่มือติดตั้งทีละขั้นตอน
├── examples/
│   ├── sample-bot-payload.json       ← ตัวอย่าง payload จาก bot.py
│   ├── sample-weather-response.json  ← ตัวอย่าง OpenWeatherMap response
│   ├── sample-places-response.json   ← ตัวอย่าง Geoapify response
│   ├── sample-openrouter-response.json ← ตัวอย่าง Gemini AI response
│   └── test-commands.md              ← คำสั่ง curl ทดสอบ
├── tests/
│   ├── conftest.py
│   └── test_workflow.py       ← 10 Auto-grading Tests
└── quiz/
    └── quiz.md                ← 10 คำถาม Quiz
```

---

## ขั้นตอนการทำงาน

1. ศึกษา `README.md` และ `SETUP_GUIDE.md`
2. สมัคร API key ทั้ง 3 ตัว (OpenWeather, Geoapify, OpenRouter)
3. ตั้งค่า Discord Server + Webhook + Bot
4. สร้าง Workflow (Chat Command) ใน n8n — **ใช้ AI Extract Info แยก city/days**
5. Export workflow เป็น JSON → วางทับ `workflow.json`
6. ตั้งค่า `bot.py` แล้วทดสอบ
7. รัน `pytest tests/ -v --tb=short` ให้ผ่าน 100 คะแนน
8. Push ขึ้น GitHub

---

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Basic LLM Chain](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.chainllm/)
- [n8n OpenRouter Chat Model](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatopenrouter/)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [OpenWeatherMap API](https://openweathermap.org/current)
- [Geoapify Places API](https://apidocs.geoapify.com/docs/places/)
- [Discord Webhook Guide](https://discord.com/developers/docs/resources/webhook)
- [discord.py Documentation](https://discordpy.readthedocs.io/)
