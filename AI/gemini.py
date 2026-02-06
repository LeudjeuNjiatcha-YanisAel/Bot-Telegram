#ai/gemini
import asyncio
from google import genai
from google.genai import types 
from Config.config import GEMINI_API


async def ask(update,context):
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(3)
    question = " ".join(context.args)
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a poser cette question au bot : {question}")
    if not question:
        await update.message.reply_text("❌ Utilisation : /ask <ta question>")
        return
    async def thread():
        try:
            client = genai.Client(api_key=GEMINI_API)

            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=question
            )

            answer = response.text
            for i in range(0,len(answer),2000) :
                await update.message.reply_text("Machine_IA🤖 \n ")
                await update.message.reply_text("💡 Réponse : "+answer[i:i+4096])
        except Exception as e:
            await update.message.reply_text(f"⚠️ Machine IA : {e}")
    asyncio.create_task(thread())