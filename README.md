# bot_checkid_telegram

บอทสำหรับแสดงข้อมูลไอดีเทเลแกรมเมื่อมีคนเพิ่มเป็นเพื่อน โดยบอทจะแสดงไอดี ชื่อผู้ใช้ และข้อมูลอื่นๆ ของผู้ใช้งาน

## คุณสมบัติ

- แสดงไอดีเทเลแกรมของผู้ใช้
- แสดงชื่อผู้ใช้ (username) ถ้ามี
- แสดงข้อมูลผู้ใช้เมื่อมีการส่งข้อความใดๆ หรือเริ่มต้นการสนทนา

## วิธีการติดตั้ง

### สำหรับการรันบน CasaOS (Raspberry Pi 5)

1. โคลนโปรเจคนี้:
   ```
   git clone https://github.com/job12345/bot_checkid_telegram.git
   cd bot_checkid_telegram
   ```

2. ติดตั้ง dependencies:
   ```
   pip install -r requirements.txt
   ```

3. รันบอท:
   ```
   python bot.py
   ```

### คำสั่งเฉพาะสำหรับ CasaOS บน Raspberry Pi 5

1. การเข้าถึง CasaOS:
   - เปิดเว็บเบราว์เซอร์และเข้าสู่ IP ของ Raspberry Pi 5 ที่รัน CasaOS 
     (เช่น http://raspberrypi.local หรือ http://[IP-ADDRESS])

2. การรันผ่าน Docker ใน CasaOS:
   - ใช้ Terminal ใน CasaOS หรือเชื่อมต่อผ่าน SSH:
     ```
     ssh pi@[IP-ADDRESS]
     ```
   - นำเข้าไปยังโฟลเดอร์ที่มีไฟล์บอท:
     ```
     cd /path/to/bot_checkid_telegram
     ```
   - สร้าง Docker container:
     ```
     docker build -t telegram-id-bot .
     docker run -d --name telegram-id-bot --restart always telegram-id-bot
     ```

3. การใช้ CasaOS Container Apps:
   - เข้าไปที่หน้า Apps ใน CasaOS
   - เลือก "New App" หรือ "Add Container"
   - ใช้ตัวเลือก "Custom" และกรอกข้อมูลดังนี้:
     - Container Name: telegram-id-bot
     - Image: ให้เลือกจาก local image ที่สร้างไว้ หรือใช้ path ไปยังไฟล์ Dockerfile
     - Network Mode: bridge
     - Restart Policy: always
   - กด "Deploy" เพื่อรันบอท

4. การตรวจสอบสถานะ:
   - ดูล็อกของบอท:
     ```
     docker logs -f telegram-id-bot
     ```
   - ตรวจสอบว่าคอนเทนเนอร์กำลังทำงาน:
     ```
     docker ps | grep telegram-id-bot
     ```

## คำสั่งที่สามารถใช้ได้

- `/start` - เริ่มใช้งานบอทและแสดงข้อมูลบัญชี
- `/id` - แสดงข้อมูลไอดีของคุณ
- `/help` - แสดงคำสั่งที่ใช้ได้

## สำหรับการรันเป็น service

คุณสามารถตั้งค่าให้บอททำงานเป็น service บน Raspberry Pi ได้ดังนี้:

1. สร้างไฟล์ service:
   ```
   sudo nano /etc/systemd/system/telegrambot.service
   ```

2. เพิ่มเนื้อหาต่อไปนี้:
   ```
   [Unit]
   Description=Telegram Bot ID Checker
   After=network.target

   [Service]
   User=<ชื่อผู้ใช้ของคุณ>
   WorkingDirectory=/path/to/bot_checkid_telegram
   ExecStart=/usr/bin/python3 /path/to/bot_checkid_telegram/bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. เปิดใช้งานและเริ่มต้น service:
   ```
   sudo systemctl enable telegrambot.service
   sudo systemctl start telegrambot.service
   ```

4. ตรวจสอบสถานะ:
   ```
   sudo systemctl status telegrambot.service
   ```

## การ Deploy ทางเลือกอื่นๆ

### การใช้ Docker บน CasaOS

1. สร้างไฟล์ Dockerfile:
   ```
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD ["python", "bot.py"]
   ```

2. สร้างและรัน Docker Container:
   ```
   docker build -t telegram-id-bot .
   docker run -d --name telegram-id-bot telegram-id-bot
   ```

3. หากใช้ CasaOS สามารถสร้าง App Container ใหม่และเลือก docker-compose ดังนี้:
   ```yaml
   version: '3'
   services:
     telegram-bot:
       build: .
       restart: always
       container_name: telegram-id-bot
   ```

### หมายเหตุเกี่ยวกับ Cloudflare Workers

โปรเจคนี้เป็น Python Bot ซึ่งไม่สามารถ deploy บน Cloudflare Workers ได้โดยตรง เนื่องจาก Cloudflare Workers รองรับเฉพาะ JavaScript/TypeScript
หากต้องการใช้ Cloudflare คุณสามารถลองตัวเลือกอื่นๆ เช่น:
- Cloudflare Pages ร่วมกับ Functions (แต่ยังมีข้อจำกัดสำหรับการรันแอปพลิเคชัน Python)
- บริการ Cloud ทั่วไปที่รองรับ Python เช่น Heroku, Railway, Render, หรือ AWS Lambda

## พัฒนาโดย

MR.j

ติดต่อ: [@paybot2025](https://t.me/paybot2025)

บริจาค: [ทรูมันนี่วอเลต](https://tmn.app.link/UMso6vUFORb)
