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
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

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
    # สร้าง application และกำหนดให้มี job_queue
    application = ApplicationBuilder().token(TOKEN).build()
    
    # เพิ่ม handler สำหรับคำสั่ง
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("report", report_command))
    
    # เพิ่ม callback handler สำหรับปุ่ม
    application.add_handler(CallbackQueryHandler(button_callback))
    
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