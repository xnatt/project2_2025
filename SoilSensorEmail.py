import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage

# 传感器配置
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

# 邮件配置
from_email = "2806058107@qq.com"  # 替换为你的QQ邮箱地址
app_password = "ylwphpddfiandhbb"  # 替换为你的QQ邮箱授权码
to_email = "2806058107@qq.com"  # 替换为接收邮件的邮箱地址


def send_water_notification():
    msg = EmailMessage()
    msg.set_content("警告：植物土壤干燥，需要浇水！")
    msg['Subject'] = "浇水提醒 - 树莓派监测系统"
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(from_email, app_password)
            server.send_message(msg)
    except Exception as e:
        print(f"发送浇水提醒邮件时出错: {e}")


def moisture_callback(channel):
    if not GPIO.input(channel):  # 干燥状态（D0输出低电平）
        send_water_notification()


GPIO.add_event_detect(channel, GPIO.FALLING, bouncetime=300)  # 仅在干燥时触发
GPIO.add_event_callback(channel, moisture_callback)


def send_daily_report(min_reading, max_reading):
    msg = EmailMessage()
    msg.set_content(f"今日传感器读数：最小值 {min_reading}，最大值 {max_reading}。")
    msg['Subject'] = "每日传感器读数报告 - 树莓派监测系统"
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(from_email, app_password)
            server.send_message(msg)
    except Exception as e:
        print(f"发送每日报告邮件时出错: {e}")


while True:
    daily_readings = []
    for _ in range(5):
        reading = GPIO.input(channel)  # 0=干燥，1=湿润
        daily_readings.append(reading)
        time.sleep(3600)
    min_reading = min(daily_readings)
    max_reading = max(daily_readings)
    send_daily_report(min_reading, max_reading)
    