#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
บอทเช็คไอดีเทเลแกรม
พัฒนาโดย: MR.j
"""

import logging
import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

# ตั้งค่า logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token ของบอท
TOKEN = "7723527281:AAFvrx8JJbQjDASvcSNkKcwPkUXy3BeYmk8"

# เก็บข้อมูลการใช้งาน
usage_data = defaultdict(int)
OWNER_ID = 805215455

# ฟังก์ชันสำหรับคำสั่ง /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    usage_data[datetime.date.today()] += 1

    # สร้างปุ่ม inline
    keyboard = [
        [
            InlineKeyboardButton("Donate (TrueMoney Wallet)", url="https://tmn.app.link/UMso6vUFORb"),
            InlineKeyboardButton("Contact Developer", url="https://t.me/paybot2025")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        f"สวัสดี {user.first_name}!
"
        f"ไอดีของคุณคือ: {user.id}
"
        f"ชื่อผู้ใช้: @{user.username if user.username else 'ไม่มี'}

"
        "Hello {user.first_name}!
"
        "Your ID is: {user.id}
"
        "Username: @{user.username if user.username else 'None'}"
    )
    await update.message.reply_text(message, reply_markup=reply_markup)

    # แจ้งเตือนเจ้าของบอทเมื่อมีผู้ใช้งานใหม่
    if context.bot:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"มีผู้ใช้งานใหม่: {user.first_name} (ID: {user.id})"
        )

# ฟังก์ชันสรุปยอดรายวัน
async def daily_summary(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()
    count = usage_data[today]
    message = f"สรุปยอดการใช้งานประจำวันที่ {today}: {count} คน"
    await context.bot.send_message(chat_id=OWNER_ID, text=message)

def main():
    # สร้าง application พร้อม JobQueue
    application = ApplicationBuilder().token(TOKEN).post_init(lambda app: setattr(app, 'job_queue', JobQueue())).build()

    # เพิ่ม handler สำหรับคำสั่ง /start
    application.add_handler(CommandHandler("start", start))

    # ตั้งเวลาแจ้งเตือนสรุปยอดรายวันเวลา 12:00 น. เวลาประเทศไทย
    job_queue = application.job_queue
    job_queue.run_daily(daily_summary, time=datetime.time(hour=5, minute=0))  # 5:00 UTC = 12:00 Thailand time

    # เริ่มการทำงานของบอท
    application.run_polling()

if __name__ == '__main__':
    main()