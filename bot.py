#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
บอทเช็คไอดีเทเลแกรม
พัฒนาโดย: MR.j
ติดต่อ: @paybot2025
บริจาค: https://tmn.app.link/UMso6vUFORb (ทรูมันนี่วอเลต)
"""

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

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
    user_info = f"""
สวัสดี {user.first_name}!

🔍 *ข้อมูลบัญชีของคุณ*
👤 ชื่อ: {user.first_name} {user.last_name if user.last_name else ""}
🆔 ไอดี: `{user.id}`
👤 ชื่อผู้ใช้: @{user.username if user.username else "ไม่มี"}

_เก็บข้อมูลนี้ไว้อ้างอิงได้เลย!_

*พัฒนาโดย:* MR.j
*ติดต่อ:* @paybot2025
*บริจาค:* [ทรูมันนี่วอเลต](https://tmn.app.link/UMso6vUFORb)
"""
    await update.message.reply_markdown(user_info)

# ฟังก์ชันสำหรับคำสั่ง /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
*คำสั่งที่ใช้ได้:*
/start - เริ่มใช้งานบอทและแสดงข้อมูลบัญชี
/id - แสดงข้อมูลไอดีของคุณ
/help - แสดงคำสั่งที่ใช้ได้

*พัฒนาโดย:* MR.j
*ติดต่อ:* @paybot2025
*บริจาค:* [ทรูมันนี่วอเลต](https://tmn.app.link/UMso6vUFORb)
"""
    await update.message.reply_markdown(help_text)

# ฟังก์ชันสำหรับคำสั่ง /id
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = f"🆔 ไอดีของคุณคือ: `{user.id}`"
    await update.message.reply_markdown(user_id)

# ฟังก์ชันตอบกลับข้อความทั่วไป
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = f"""
ข้อความของคุณ: "{update.message.text}"

🔍 *ข้อมูลบัญชีของคุณ*
👤 ชื่อ: {user.first_name} {user.last_name if user.last_name else ""}
🆔 ไอดี: `{user.id}`
👤 ชื่อผู้ใช้: @{user.username if user.username else "ไม่มี"}

พิมพ์ /help เพื่อดูคำสั่งที่ใช้ได้
"""
    await update.message.reply_markdown(message)

def main():
    # สร้าง application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # เพิ่ม handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # เริ่มการทำงานของบอท
    print("บอทเริ่มทำงานแล้ว...")
    application.run_polling()

if __name__ == '__main__':
    main()