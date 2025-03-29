# บอทเช็คไอดีเทเลแกรม

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

## พัฒนาโดย

MR.j

ติดต่อ: [@paybot2025](https://t.me/paybot2025)

บริจาค: [ทรูมันนี่วอเลต](https://tmn.app.link/UMso6vUFORb)