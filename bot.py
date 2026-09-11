import os
import telebot
from openai import OpenAI

# 1. Khởi tạo mã bảo mật
TELEGRAM_TOKEN = os.environ.get('')
OPENROUTER_API_KEY = os.environ.get('AI_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(
    base_url="https://openrouter.ai",
    api_key=OPENROUTER_API_KEY,
)

# Tạo một biến để nhớ model đang chọn (mặc định ban đầu là DeepSeek R1)
CURRENT_MODEL = "deepseek/deepseek-r1:free"

# Lệnh /change để bạn đổi sang AI khác trực tiếp trên Telegram
@bot.message_handler(commands=['change'])
def change_model(message):
    global CURRENT_MODEL
    # Lấy tên model người dùng gõ sau lệnh /change
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, f"🤖 AI hiện tại: `{CURRENT_MODEL}`\n\nMẹo: Để đổi AI, hãy gõ theo cú pháp:\n`/change tên_model_mới`\n\nVí dụ:\n`/change meta-llama/llama-3.3-70b-instruct:free`", parse_mode="Markdown")
        return
    
    new_model = args[1].strip()
    CURRENT_MODEL = new_model
    bot.reply_to(message, f"✅ Đã chuyển thành công sang AI: `{CURRENT_MODEL}`", parse_mode="Markdown")

# Xử lý tin nhắn chat thông thường
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        sent_msg = bot.reply_to(message, f"⌛ ({CURRENT_MODEL.split('/')[-1]}) đang suy nghĩ...")
        
        # Gọi mô hình đang được lựa chọn lưu trong biến CURRENT_MODEL
        response = client.chat.completions.create(
            model=CURRENT_MODEL, 
            messages=[{"role": "user", "content": message.text}]
        )
        
        ai_reply = response.choices.message.content
        bot.edit_message_text(ai_reply, chat_id=message.chat.id, message_id=sent_msg.message_id)
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi khi gọi model `{CURRENT_MODEL}`:\n{str(e)}", parse_mode="Markdown")

print("Bot Telegram đa model đang chạy...")
bot.infinity_polling()
