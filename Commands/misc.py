import asyncio
import random

async def ping(update,context):
    await update.message.reply_text("🤖 MACHINE BOT \n \n\n🏓 Pong! Je suis en ligne ✅")

async def pin(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    
    code = "".join([str(random.randint(0, 9)) for _ in range(4)])
    await update.message.reply_text(f"🔑 Ton code PIN : {code}")
    print("Un code PIN a été generer")