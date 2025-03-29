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
     # เชื่อมต่อเข้า SSH ของ Raspberry Pi โดยเปลี่ยน [IP-ADDRESS] เป็น IP จริงของเครื่อง Pi
     ssh pi@[IP-ADDRESS]
     
     # หรือถ้าใช้ Terminal ในหน้าเว็บ CasaOS ให้คลิกที่ไอคอน Terminal
     ```
   - นำเข้าไปยังโฟลเดอร์ที่มีไฟล์บอท:
     ```
     # สร้างโฟลเดอร์ถ้ายังไม่มี
     mkdir -p /opt/casaos/telegram-bot
     
     # คัดลอกไฟล์จาก GitHub
     cd /opt/casaos/telegram-bot
     git clone https://github.com/job12345/bot_checkid_telegram.git .
     # หรือถ้ามีไฟล์อยู่แล้ว
     cd /path/to/bot_checkid_telegram
     ```
   - สร้างไฟล์ Dockerfile:
     ```
     # สร้างไฟล์ Dockerfile
     cat > Dockerfile << 'EOF'
     FROM python:3.9-slim
     
     WORKDIR /app
     
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     
     COPY . .
     
     CMD ["python", "bot.py"]
     EOF
     ```
   - สร้าง Docker container:
     ```
     # สร้าง Docker image
     docker build -t telegram-id-bot .
     
     # ตรวจสอบว่า image สร้างเสร็จแล้ว
     docker images | grep telegram-id-bot
     
     # รัน container จาก image ที่สร้าง
     docker run -d --name telegram-id-bot --restart always telegram-id-bot
     
     # ตรวจสอบว่า container กำลังทำงาน
     docker ps | grep telegram-id-bot
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

### การ Deploy บน Railway.com

Railway เป็นแพลตฟอร์ม cloud ที่เหมาะกับการ deploy แอปพลิเคชัน Python ที่ต้องทำงานตลอดเวลาเช่นบอทเทเลแกรม

1. ขั้นตอนการเตรียมโปรเจคให้พร้อมสำหรับ Railway:
   - ต้องมั่นใจว่าโปรเจคของคุณมีไฟล์ต่อไปนี้:
     - `requirements.txt` (มีอยู่แล้ว)
     - `Procfile` (สำหรับบอกว่าจะรันคำสั่งอะไร)
     - `railway.toml` (สำหรับกำหนดค่าการ deploy)
   
   - สร้างไฟล์ Procfile ในโฟลเดอร์โปรเจค:
     ```
     worker: python bot.py
     ```
     
   - สร้างไฟล์ railway.toml ในโฟลเดอร์โปรเจค:
     ```
     [build]
     builder = "nixpacks"
     buildCommand = "pip install -r requirements.txt"
     
     [deploy]
     startCommand = "python bot.py"
     healthcheckPath = "/"
     healthcheckTimeout = 100
     restartPolicyType = "always"
     ```

2. การอัปโหลดไฟล์ไปยัง GitHub:
   ```
   git add Procfile railway.toml
   git commit -m "เพิ่มไฟล์สำหรับ deploy บน Railway"
   git push origin main
   ```

### วิธีแก้ไขปัญหา "No start command could be found" บน Railway

1. การสร้างไฟล์ที่จำเป็นให้ถูกต้อง:
   - สร้างไฟล์ `Procfile` โดยไม่มีนามสกุล:
     ```
     # ต้องเป็นข้อความนี้เท่านั้น ไม่มีเว้นวรรคหรือบรรทัดว่าง
     worker: python bot.py
     ```
   
   - สร้างไฟล์ `runtime.txt`:
     ```
     python-3.9.18
     ```
     
   - สร้างไฟล์ `nixpacks.toml` (แทน railway.toml):
     ```
     [phases.setup]
     nixPkgs = ["python39"]

     [phases.install]
     cmds = ["python -m venv /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt"]

     [start]
     cmd = "python bot.py"
     ```

2. ดำเนินการอัปโหลดไฟล์เหล่านี้ทั้งหมดไปยัง GitHub:
   ```
   git add Procfile runtime.txt nixpacks.toml
   git commit -m "แก้ไขปัญหา No start command could be found"
   git push origin main
   ```

3. ขั้นตอนการ Deploy บน Railway ผ่านเว็บไซต์:
   - ล็อกอินที่ [Railway Dashboard](https://railway.app/dashboard)
   - คลิก "New Project"
   - เลือก "Deploy from GitHub repo"
   - เลือก repository ของคุณ (bot_checkid_telegram)
   - หากมีการร้องขอให้กำหนดค่าเพิ่มเติม ให้ระบุ:
     - Root Directory: / (หรือเว้นว่างไว้)
     - Service Name: telegrambot
   - ตั้งค่า Environment Variables (คลิกที่ "Variables"):
     - `TOKEN` = `7723527281:AAFvrx8JJbQjDASvcSNkKcwPkUXy3BeYmk8`
   - คลิก "Deploy" หรือ "Deploy Now" เพื่อเริ่มการ deploy

4. การตรวจสอบสถานะการทำงาน:
   - ไปที่หน้า "Deployments" ในโปรเจคของคุณบน Railway
   - คลิกที่ deployment ล่าสุดเพื่อดูล็อก
   - หากมีข้อผิดพลาด ให้ตรวจสอบล็อกและแก้ไขไฟล์ที่เกี่ยวข้อง
   - บอทควรทำงานโดยอัตโนมัติหลังจาก deploy สำเร็จ

5. การแก้ไขปัญหาที่พบบ่อย:
   - หากพบข้อผิดพลาด "No start command could be found" ให้ตรวจสอบว่าไฟล์ Procfile และ railway.toml มีข้อมูลถูกต้อง
   - หากต้องการรันคำสั่งเฉพาะบน Railway ให้ไปที่ "Deployments" > คลิก ">" ที่มุมขวาของ deployment > "Shell"
   - หากต้องการรีสตาร์ทบอท ให้คลิกที่ "Deployments" > "Redeploy"
