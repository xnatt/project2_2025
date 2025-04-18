import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage

# ------------------- 硬件配置 -------------------
CHANNEL = 4  # D0引脚连接到GPIO 4（BCM编号）
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL, GPIO.IN)

# ------------------- 邮件配置（以QQ邮箱为例） -------------------
FROM_EMAIL = "2806058107@qq.com"
APP_PASSWORD = "ylwphpddfiandhbb"
TO_EMAIL = FROM_EMAIL

# ------------------- 邮件发送函数 -------------------
def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.set_debuglevel(1)  # 开启调试模式，打印详细的服务器响应信息
            server.login(FROM_EMAIL, APP_PASSWORD)
            response = server.send_message(msg)
            if not response:
                print(f"邮件发送成功：{subject}")
            else:
                print(f"邮件发送部分失败：{response}")
    except smtplib.SMTPAuthenticationError:
        print("邮件发送失败：认证错误，请检查邮箱账号和授权码。")
    except smtplib.SMTPConnectError:
        print("邮件发送失败：无法连接到SMTP服务器，请检查网络连接和服务器配置。")
    except smtplib.SMTPException as e:
        # 捕获SMTP相关的异常
        print(f"邮件发送失败：SMTP异常 - {str(e)}")
    except Exception as e:
        # 捕获其他未知异常
        print(f"发生未知异常：{str(e)}，但邮件可能已成功发送。")


# ------------------- 传感器状态检测 -------------------
def check_moisture_status():
    status = GPIO.input(CHANNEL)
    if status == GPIO.HIGH:
        return "土壤湿润，无需浇水"
    else:
        return "土壤干燥，需要浇水！"


# ------------------- 主循环（每天4次检测，间隔6小时） -------------------
if __name__ == "__main__":
    try:
        while True:
            daily_readings = []
            for _ in range(4):  # 每天记录4次读数（文档要求）
                status = check_moisture_status()
                daily_readings.append(status)
                # 发送单次状态邮件（可选：根据需求决定是否每次检测都发邮件）
                send_email("实时湿度检测", f"当前状态：{status}")
                time.sleep(21600)  # 间隔6小时（6*3600秒）

            # 发送每日总结邮件（包含4次检测结果）
            summary = "\n".join([f"{i + 1}. {reading}" for i, reading in enumerate(daily_readings)])
            send_email("每日湿度报告", f"今日4次检测结果：\n{summary}")

    except KeyboardInterrupt:
        print("\n程序终止，正在清理GPIO资源...")
    finally:
        GPIO.cleanup()
    