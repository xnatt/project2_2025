import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage

# 硬件配置
CHANNEL = 4  # D0引脚连接到GPIO 4（BCM编号）
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL, GPIO.IN)

# 邮件配置（已填入你的信息）
FROM_EMAIL = "2806058107@qq.com"
APP_PASSWORD = "ylwphpddfiandhbb"
TO_EMAIL = FROM_EMAIL  # 发送给自己

# 邮件发送函数（优化异常处理）
def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(FROM_EMAIL, APP_PASSWORD)
            response = server.send_message(msg)
            if not response:
                print(f"邮件发送成功：{subject}")
                
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError) as e:
        print(f"邮件发送失败：核心错误 - {str(e)}")
    except Exception as e:
        pass  # 忽略非关键异常（如连接关闭时的不完整响应）

# 传感器状态检测
def check_moisture_status():
    return "土壤干燥，需要浇水！" if GPIO.input(CHANNEL) else "土壤湿润，无需浇水。"

# 主循环（每天4次检测，间隔6小时）
if __name__ == "__main__":
    try:
        while True:
            for _ in range(4):
                status = check_moisture_status()
                send_email("实时湿度检测", f"当前状态：{status}")
                time.sleep(21600)  # 6小时间隔
                
            # 每日总结（可选，根据需求添加）
            # send_email("每日湿度报告", "今日4次检测均正常...")
            
    except KeyboardInterrupt:
        print("\n程序终止，清理GPIO资源...")
        GPIO.cleanup()