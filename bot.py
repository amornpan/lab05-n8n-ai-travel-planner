import discord
import aiohttp

# ╔══════════════════════════════════════════════════════════╗
# ║  ตั้งค่าตรงนี้ — ใส่ค่าของคุณเอง                          ║
# ╚══════════════════════════════════════════════════════════╝

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
N8N_WEBHOOK_URL = "YOUR_N8N_WEBHOOK_URL_HERE"

# ╔══════════════════════════════════════════════════════════╗
# ║  โค้ด Bot — ไม่ต้องแก้ไข                                   ║
# ╚══════════════════════════════════════════════════════════╝

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"")
    print(f"  ✅ Bot พร้อมใช้งาน!")
    print(f"  🤖 ชื่อ Bot: {client.user}")
    print(f"  📡 Webhook URL: {N8N_WEBHOOK_URL}")
    print(f"")
    print(f"  💬 วิธีใช้: พิมพ์อะไรก็ได้เกี่ยวกับการท่องเที่ยวใน Discord Channel:")
    print(f"     อยากไปเที่ยวเชียงใหม่ 3 วัน")
    print(f"     Plan a trip to Tokyo for 5 days")
    print(f"     แนะนำที่เที่ยวกรุงเทพ")
    print(f"     !plan Bangkok 3   — ใช้คำสั่งแบบเดิมก็ได้")
    print(f"")
    print(f"  กด Ctrl+C เพื่อหยุด Bot")
    print(f"  {'='*50}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()

    # ไม่ตอบข้อความว่าง
    if not content:
        return

    # ส่งข้อความดิบไป n8n — ให้ AI เป็นคนแยกข้อมูล city/days
    print(f"  📨 รับข้อความ '{content}' จาก {message.author.name}")

    payload = {
        "content": content,
        "author": {
            "username": message.author.name,
            "id": str(message.author.id)
        },
        "channel_id": str(message.channel.id),
        "guild_id": str(message.guild.id) if message.guild else None
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_WEBHOOK_URL, json=payload) as resp:
                print(f"  ✅ ส่งไป n8n แล้ว — Status: {resp.status}")
    except Exception as e:
        print(f"  ❌ ส่งไป n8n ไม่สำเร็จ: {e}")


if __name__ == "__main__":
    print(f"  {'='*50}")
    print(f"  ✈️ AI Travel Planner Bot — Starting...")
    print(f"  {'='*50}")
    client.run(BOT_TOKEN)
