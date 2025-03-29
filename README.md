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

## Installation / การติดตั้ง

### For CasaOS (Raspberry Pi 5)

1. Clone this project:
   ```
   git clone https://github.com/job12345/bot_checkid_telegram.git
   cd bot_checkid_telegram
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```
   python bot.py
   ```

### สำหรับ CasaOS (Raspberry Pi 5)

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
