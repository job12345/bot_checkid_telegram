#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
บอทเช็คไอดีเทเลแกรม
พัฒนาโดย: MR.j
"""

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ตั้งค่า logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token ของบอท
TOKEN = "7723527281:AAFvrx8JJbQjDASvcSNkKcwPkUXy3BeYmk8"

# ฟังก์ชันสำหรับคำสั่ง /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"สวัสดี {user.first_name}! ไอดีของคุณคือ {user.id}")

def main():
    # สร้าง application
    application = ApplicationBuilder().token(TOKEN).build()

    # เพิ่ม handler สำหรับคำสั่ง /start
    application.add_handler(CommandHandler("start", start))

    # เริ่มการทำงานของบอท
    application.run_polling()

if __name__ == '__main__':
    main()