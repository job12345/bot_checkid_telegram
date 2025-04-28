#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
บอทเช็คไอดีเทเลแกรม
พัฒนาโดย: MR.j
"""

import os
import logging
from datetime import datetime, timedelta, time
import pytz
from collections import defaultdict, Counter
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    JobQueue
)

# โหลดค่าจาก .env file
load_dotenv()

# ตั้งค่า logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ใช้ค่าจาก environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', '805215455'))
RATE_LIMIT = int(os.getenv('RATE_LIMIT', '5'))
TIME_WINDOW = int(os.getenv('TIME_WINDOW', '60'))

# เก็บข้อมูลการใช้งานและ rate limiting
usage_data = defaultdict(int)
user_message_count = Counter()
user_last_reset = defaultdict(datetime.now)

# ฟังก์ชันตรวจสอบ rate limit
async def check_rate_limit(user_id: int) -> bool:
    now = datetime.now()
    if (now - user_last_reset[user_id]).seconds > TIME_WINDOW:
        user_message_count[user_id] = 0
        user_last_reset[user_id] = now
    
    user_message_count[user_id] += 1
    return user_message_count[user_id] <= RATE_LIMIT

# ฟังก์ชันตรวจสอบความถูกต้องของผู้ใช้
def is_valid_user(user) -> bool:
    if not user:
        return False
    
    if user.is_bot:
        return False
    
    if user.username:
        unsafe_chars = '<>{}[]()\'"`'
        if any(c in user.username for c in unsafe_chars):
            return False
    
    return True

# Decorator สำหรับจัดการข้อผิดพลาด
def error_handler(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await func(update, context)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            if context.bot:
                await context.bot.send_message(
                    chat_id=OWNER_ID,
                    text=f"❌ เกิดข้อผิดพลาด: {str(e)}"
                )
            await update.message.reply_text(
                "ขออภัย เกิดข้อผิดพลาดบางอย่าง กรุณาลองใหม่อีกครั้งในภายหลัง"
            )
    return wrapper

@error_handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # ตรวจสอบ rate limit
    if not await check_rate_limit(user.id):
        await update.message.reply_text(
            "คุณส่งคำขอมากเกินไป กรุณารอสักครู่แล้วลองใหม่อีกครั้ง"
        )
        return
    
    # ตรวจสอบความถูกต้องของผู้ใช้
    if not is_valid_user(user):
        await update.message.reply_text(
            "ไม่สามารถดำเนินการได้ กรุณาติดต่อผู้ดูแลระบบ"
        )
        return
    
    usage_data[datetime.date.today().isoformat()] += 1

    # สร้างปุ่ม inline ทั่วไป
    keyboard = [
        [
            InlineKeyboardButton("บริจาค (ทรูมันนี่วอเลต)", url="https://tmn.app.link/UMso6vUFORb"),
            InlineKeyboardButton("ติดต่อผู้พัฒนา", url="https://t.me/paybot2025")
        ]
    ]
    
    # เพิ่มปุ่มพิเศษสำหรับ owner
    if user.id == OWNER_ID:
        keyboard.extend([
            [InlineKeyboardButton("📊 รายงานวันนี้", callback_data="report_today")],
            [InlineKeyboardButton("📅 รายงานรายสัปดาห์", callback_data="report_week")],
            [InlineKeyboardButton("📈 รายงานรายเดือน", callback_data="report_month")],
            [InlineKeyboardButton("👥 จำนวนผู้ใช้ทั้งหมด", callback_data="report_users")]
        ])
    
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

# ฟังก์ชันสำหรับการจัดการกับปุ่ม callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    
    # ตรวจสอบว่าผู้ใช้เป็น owner หรือไม่
    if user.id != OWNER_ID:
        await query.answer("คุณไม่มีสิทธิ์ใช้งานส่วนนี้", show_alert=True)
        return
    
    await query.answer()  # ตอบกลับ callback query เพื่อหยุดการโหลด
    
    today = datetime.date.today()
    
    if query.data == "report_today":
        # รายงานวันนี้
        today_iso = today.isoformat()
        count = usage_data[today_iso]
        message = f"📊 *รายงานวันนี้ ({today_iso})*\n\nจำนวนผู้ใช้งานวันนี้: *{count}* คน"
        await query.edit_message_text(text=message, parse_mode="Markdown", reply_markup=get_owner_keyboard())
        
    elif query.data == "report_week":
        # รายงานสัปดาห์นี้
        start_of_week = today - datetime.timedelta(days=today.weekday())
        report = "📅 *รายงานรายสัปดาห์*\n\n"
        total = 0
        
        for i in range(7):
            date = start_of_week + datetime.timedelta(days=i)
            date_iso = date.isoformat()
            count = usage_data[date_iso]
            total += count
            day_name = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"][i]
            report += f"วัน{day_name} ({date_iso}): *{count}* คน\n"
        
        report += f"\nรวมทั้งสัปดาห์: *{total}* คน"
        await query.edit_message_text(text=report, parse_mode="Markdown", reply_markup=get_owner_keyboard())
        
    elif query.data == "report_month":
        # รายงานเดือนนี้
        first_day = today.replace(day=1)
        month_name = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", 
                      "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"][today.month - 1]
        
        report = f"📈 *รายงานเดือน{month_name}*\n\n"
        total = 0
        
        # สรุปเป็นรายสัปดาห์
        current_week = 1
        week_start = first_day
        while week_start.month == today.month:
            week_end = min(week_start + datetime.timedelta(days=6), 
                          today.replace(day=1, month=today.month+1) - datetime.timedelta(days=1))
            
            week_count = 0
            for i in range((week_end - week_start).days + 1):
                date = week_start + datetime.timedelta(days=i)
                date_iso = date.isoformat()
                week_count += usage_data[date_iso]
            
            total += week_count
            report += f"สัปดาห์ที่ {current_week} ({week_start.day}-{week_end.day}): *{week_count}* คน\n"
            
            current_week += 1
            week_start = week_end + datetime.timedelta(days=1)
        
        report += f"\nรวมทั้งเดือน: *{total}* คน"
        await query.edit_message_text(text=report, parse_mode="Markdown", reply_markup=get_owner_keyboard())
        
    elif query.data == "report_users":
        # จำนวนผู้ใช้ทั้งหมด
        total_users = sum(usage_data.values())
        active_days = len(usage_data)
        
        message = f"👥 *รายงานผู้ใช้ทั้งหมด*\n\n"
        message += f"จำนวนผู้ใช้ทั้งหมด: *{total_users}* คน\n"
        message += f"จำนวนวันที่มีการใช้งาน: *{active_days}* วัน\n"
        
        if active_days > 0:
            avg_users = total_users / active_days
            message += f"เฉลี่ยผู้ใช้ต่อวัน: *{avg_users:.2f}* คน"
        
        await query.edit_message_text(text=message, parse_mode="Markdown", reply_markup=get_owner_keyboard())

# ฟังก์ชันสร้างปุ่มสำหรับ owner
def get_owner_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("บริจาค (ทรูมันนี่วอเลต)", url="https://tmn.app.link/UMso6vUFORb"),
            InlineKeyboardButton("ติดต่อผู้พัฒนา", url="https://t.me/paybot2025")
        ],
        [InlineKeyboardButton("📊 รายงานวันนี้", callback_data="report_today")],
        [InlineKeyboardButton("📅 รายงานรายสัปดาห์", callback_data="report_week")],
        [InlineKeyboardButton("📈 รายงานรายเดือน", callback_data="report_month")],
        [InlineKeyboardButton("👥 จำนวนผู้ใช้ทั้งหมด", callback_data="report_users")]
    ]
    return InlineKeyboardMarkup(keyboard)

def main():
    # สร้าง application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # เพิ่ม handler สำหรับคำสั่ง
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # ตั้งเวลาสรุปยอดรายวันเวลา 12:00 น. เวลาประเทศไทย (UTC+7)
    thai_tz = pytz.timezone('Asia/Bangkok')
    target_time = time(hour=12, minute=0)  # ไม่ต้องใส่ tzinfo ใน time object
    
    # ตั้งค่า job queue
    if application.job_queue:
        try:
            application.job_queue.run_daily(daily_summary, time=target_time)
            print("ตั้งค่าการแจ้งเตือนรายวันสำเร็จ")
        except Exception as e:
            print(f"ไม่สามารถตั้งค่าการแจ้งเตือนรายวัน: {e}")
    
    # เริ่มการทำงานของบอท
    print("บอทเริ่มทำงานแล้ว...")
    application.run_polling()

if __name__ == '__main__':
    main()