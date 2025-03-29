#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
บอทเช็คไอดีเทเลแกรม
พัฒนาโดย: MR.j
"""

import logging
import datetime
import pytz
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
    usage_data[datetime.date.today().isoformat()] += 1

    # สร้างปุ่ม inline
    keyboard = [
        [
            InlineKeyboardButton("บริจาค (ทรูมันนี่วอเลต)", url="https://tmn.app.link/UMso6vUFORb"),
            InlineKeyboardButton("ติดต่อผู้พัฒนา", url="https://t.me/paybot2025")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        f"สวัสดี {user.first_name}!\n"
        f"ไอดีของคุณคือ: {user.id}\n"
        f"ชื่อผู้ใช้: @{user.username if user.username else 'ไม่มี'}\n\n"
        f"Hello {user.first_name}!\n"
        f"Your ID is: {user.id}\n"
        f"Username: @{user.username if user.username else 'None'}\n\n"
        f"พัฒนาโดย: MR.j\nติดต่อ: @paybot2025"
    )
    await update.message.reply_text(message, reply_markup=reply_markup)

    # แจ้งเตือนเจ้าของบอทเมื่อมีผู้ใช้งานใหม่
    if context.bot:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"มีผู้ใช้งานใหม่: {user.first_name} (ID: {user.id})"
        )

# ฟังก์ชันสำหรับคำสั่ง /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
*คำสั่งที่ใช้ได้:*
/start - เริ่มใช้งานบอทและแสดงข้อมูลบัญชี
/help - แสดงคำสั่งที่ใช้ได้

*พัฒนาโดย:* MR.j
*ติดต่อ:* @paybot2025
*บริจาค:* [ทรูมันนี่วอเลต](https://tmn.app.link/UMso6vUFORb)
"""
    # สร้างปุ่ม inline
    keyboard = [
        [
            InlineKeyboardButton("บริจาค (ทรูมันนี่วอเลต)", url="https://tmn.app.link/UMso6vUFORb"),
            InlineKeyboardButton("ติดต่อผู้พัฒนา", url="https://t.me/paybot2025")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_markdown(help_text, reply_markup=reply_markup)

# ฟังก์ชันสำหรับการขอรายงานสรุป
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # ตรวจสอบว่าผู้ใช้เป็นเจ้าของบอทหรือไม่
    if user.id != OWNER_ID:
        await update.message.reply_text("คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
        return
    
    today = datetime.date.today().isoformat()
    count = usage_data[today]
    message = f"สรุปยอดการใช้งานวันนี้ ({today}): {count} คน"
    await update.message.reply_text(message)

# ฟังก์ชันสรุปยอดรายวัน
async def daily_summary(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today().isoformat()
    count = usage_data[today]
    message = f"สรุปยอดการใช้งานประจำวันที่ {today}: {count} คน"
    await context.bot.send_message(chat_id=OWNER_ID, text=message)

def main():
    # สร้าง application และกำหนดให้มี job_queue
    application = ApplicationBuilder().token(TOKEN).build()
    
    # เพิ่ม handler สำหรับคำสั่ง
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("report", report_command))
    
    # ตั้งเวลาสรุปยอดรายวันเวลา 12:00 น. เวลาประเทศไทย (UTC+7)
    thai_tz = pytz.timezone('Asia/Bangkok')
    target_time = datetime.time(hour=12, minute=0, tzinfo=thai_tz)
    
    # ถ้ามี job_queue (หากไม่มีก็ไม่ต้องตั้งเวลา)
    if hasattr(application, 'job_queue'):
        application.job_queue.run_daily(daily_summary, time=target_time)
    
    # เริ่มการทำงานของบอท
    application.run_polling()

if __name__ == '__main__':
    main()