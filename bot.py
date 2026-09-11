import os
import telebot
import google.generativeai as genai

# Lấy các khóa bí mật từ biến môi trường của Koyeb
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('AI_API_KEY')

# Khởi tạo cấu hình AI và Bot Telegram
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Phiên bản AI ổn định hiện tại
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Xử lý khi nhận được tin nhắn từ người dùng
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Phản hồi tạm thời để người dùng biết AI đang xử lý
        sent_msg = bot.reply_to(message, "AI đang suy nghĩ...")
        
        # Gọi AI tạo câu trả lời
        response = model.generate_content(message.text)
        
        # Cập nhật tin nhắn tạm bằng câu trả lời của AI
        bot.edit_message_text(response.text, chat_id=message.chat.id, message_id=sent_msg.message_id)
    except Exception as e:
        bot.reply_to(message, f"Có lỗi xảy ra: {str(e)}")

# Chạy Bot
print("Bot đang khởi động...")
bot.infinity_polling()
