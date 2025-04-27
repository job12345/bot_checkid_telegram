# bot_checkid_telegram

This bot displays the Telegram ID of users when they add the bot. It also provides daily, monthly, and yearly usage summaries to the bot owner.

# บอทเช็คไอดีเทเลแกรม

บอทนี้จะแสดงไอดีเทเลแกรมของผู้ใช้เมื่อมีการเพิ่มบอท พร้อมทั้งสรุปยอดการใช้งานรายวัน รายเดือน และรายปีให้เจ้าของบอท

## Features / คุณสมบัติ

- Display Telegram ID of users in both Thai and English.
- Notify the bot owner when a new user starts using the bot.
- Provide daily, monthly, and yearly usage summaries to the bot owner.

- แสดงไอดีเทเลแกรมของผู้ใช้ทั้งภาษาไทยและภาษาอังกฤษ
- แจ้งเตือนเจ้าของบอทเมื่อมีผู้ใช้งานใหม่
- สรุปยอดการใช้งานรายวัน รายเดือน และรายปีให้เจ้าของบอท

## Installation on CasaOS / การติดตั้งบน CasaOS

### วิธีที่ 1: ติดตั้งผ่าน Docker (แนะนำ)

1. เข้าไปที่ CasaOS Dashboard และเลือก "App Store"

2. กดปุ่ม "New App" หรือ "Add Container"

3. เลือก "Custom" และกรอกข้อมูลดังนี้:
   - Container Name: telegram-id-bot
   - Image: python:3.9-slim
   - Network Mode: bridge
   - Restart Policy: always
   - Environment Variables:
     - `TOKEN`: ใส่ Token ของบอทเทเลแกรม
   - Volumes:
     - Host Path: /opt/casaos/telegram-bot
     - Container Path: /app

4. หลังจากสร้าง Container แล้ว เชื่อมต่อเข้าไปที่ Container Terminal:
   ```bash
   cd /app
   git clone https://github.com/job12345/bot_checkid_telegram.git .
   pip install -r requirements.txt
   python bot.py
   ```

### วิธีที่ 2: ติดตั้งโดยตรงบน CasaOS

1. เข้าถึง CasaOS Terminal:
   ```bash
   # เข้าไปที่ CasaOS Dashboard > Terminal
   # หรือ SSH เข้า CasaOS:
   ssh username@your-casaos-ip
   ```

2. ติดตั้ง Python และ dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git python3-venv python3-full
   ```

3. โคลนและติดตั้งบอท:
   ```bash
   mkdir -p /opt/casaos/telegram-bot
   cd /opt/casaos/telegram-bot
   git clone https://github.com/job12345/bot_checkid_telegram.git .
   
   # สร้างและใช้งาน virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # ติดตั้ง dependencies
   pip install -r requirements.txt
   ```

4. สร้าง systemd service เพื่อให้บอททำงานตลอดเวลา:
   ```bash
   sudo nano /etc/systemd/system/telegrambot.service
   ```
   
   ใส่เนื้อหาต่อไปนี้:
   ```ini
   [Unit]
   Description=Telegram Bot ID Checker
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/opt/casaos/telegram-bot
   ExecStart=/opt/casaos/telegram-bot/venv/bin/python bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

5. เปิดใช้งานและเริ่มต้น service:
   ```bash
   sudo systemctl enable telegrambot
   sudo systemctl start telegrambot
   ```

6. ตรวจสอบสถานะการทำงาน:
   ```bash
   sudo systemctl status telegrambot
   ```

### การตรวจสอบล็อก

- ดูล็อกของ systemd service:
  ```bash
  sudo journalctl -u telegrambot -f
  ```

- ดูล็อกของ Docker container:
  ```bash
  docker logs -f telegram-id-bot
  ```

### การอัปเดตบอท

1. สำหรับการติดตั้งผ่าน Docker:
   ```bash
   cd /opt/casaos/telegram-bot
   git pull
   docker restart telegram-id-bot
   ```

2. สำหรับการติดตั้งโดยตรง:
   ```bash
   cd /opt/casaos/telegram-bot
   git pull
   sudo systemctl restart telegrambot
   ```

### วิธีที่ 3: ติดตั้งด้วย PM2 (แนะนำสำหรับนักพัฒนา)

1. ติดตั้ง dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git python3-venv python3-full nodejs npm
   sudo npm install -g pm2
   ```

2. โคลนและติดตั้งบอท:
   ```bash
   cd ~
   git clone https://github.com/job12345/bot_checkid_telegram.git
   cd bot_checkid_telegram

   # สร้างและใช้งาน virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # ติดตั้ง dependencies
   pip install -r requirements.txt
   ```

3. รันบอทด้วย PM2 และตั้งค่าให้รันอัตโนมัติ:
   ```bash
   # รันบอท
   pm2 start bot.py --name "bot-check-id-telegram" --interpreter ./venv/bin/python

   # บันทึกการตั้งค่า PM2
   pm2 save

   # ตั้งค่าให้ PM2 รันอัตโนมัติเมื่อระบบบูต
   pm2 startup
   # รันคำสั่งที่ PM2 แนะนำหลังจากรัน startup
   ```

4. คำสั่งที่มีประโยชน์สำหรับ PM2:
   ```bash
   # ดูสถานะของบอท
   pm2 status

   # ดูล็อกของบอท
   pm2 logs bot-check-id-telegram

   # รีสตาร์ทบอท
   pm2 restart bot-check-id-telegram

   # หยุดบอท
   pm2 stop bot-check-id-telegram

   # ลบบอทออกจาก PM2
   pm2 delete bot-check-id-telegram
   ```

## Deployment on Railway / การ Deploy บน Railway

1. Ensure the project contains the following files:
   - `requirements.txt` (dependencies)
   - `Procfile` (start command)
   - `runtime.txt` (Python version)

2. File contents:
   - `Procfile`:
     ```
     worker: python bot.py
     ```
   - `runtime.txt`:
     ```
     python-3.9.18
     ```

3. Push the project to GitHub:
   ```
   git add .
   git commit -m "Prepare project for Railway deployment"
   git push origin main
   ```

4. Deploy on Railway:
   - Log in to [Railway Dashboard](https://railway.app/dashboard).
   - Click "New Project" and select "Deploy from GitHub repo."
   - Choose your repository.
   - Set Environment Variables:
     - `TOKEN` = `YOUR_TELEGRAM_BOT_TOKEN`
   - Click "Deploy" to start the deployment.

5. Check the bot's status:
   - Go to the "Deployments" page in Railway Dashboard.
   - Check the logs to ensure the bot is running correctly.

## Commands / คำสั่งที่สามารถใช้ได้

- `/start` - Display user information in Thai and English.
- `/help` - Show available commands.

- `/start` - แสดงข้อมูลผู้ใช้ทั้งภาษาไทยและภาษาอังกฤษ
- `/help` - แสดงคำสั่งที่สามารถใช้ได้

## Owner Notifications / การแจ้งเตือนเจ้าของบอท

- The bot notifies the owner (Telegram ID: 805215455) when a new user starts using the bot.
- Daily usage summaries are sent to the owner at 12:00 PM Thailand time every day, or the owner can directly message the bot to request a report immediately.

- บอทจะแจ้งเตือนเจ้าของ (Telegram ID: 805215455) เมื่อมีผู้ใช้งานใหม่
- สรุปยอดการใช้งานรายวันจะถูกส่งให้เจ้าของบอททุกวันเวลา 12:00 น. เวลาประเทศไทย หรือเจ้าของสามารถทักส่วนตัวไปหาบอทเพื่อกดเมนูขอดูรายงานได้เลยทันที

## Developer Information / ข้อมูลผู้พัฒนา

- Developed by: MR.j
- Contact: [@paybot2025](https://t.me/paybot2025)
- Donate: [TrueMoney Wallet](https://tmn.app.link/UMso6vUFORb)

- พัฒนาโดย: MR.j
- ติดต่อ: [@paybot2025](https://t.me/paybot2025)
- บริจาค: [ทรูมันนี่วอเลต](https://tmn.app.link/UMso6vUFORb)
