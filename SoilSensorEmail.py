
import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage

# Hardware configuration
CHANNEL = 4  # The D0 pin is connected to GPIO 4 (BCM numbering)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL, GPIO.IN)

# Email configuration (with your information filled in)
FROM_EMAIL = "2806058107@qq.com"
APP_PASSWORD = "ylwphpddfiandhbb"
TO_EMAIL = FROM_EMAIL  # Send to yourself

# Email sending function (optimized exception handling)
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
                print(f"Email sent successfully: {subject}")

    except (smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError) as e:
        print(f"Email sending failed: Core error - {str(e)}")
    except Exception as e:
        pass  # Ignore non - critical exceptions (such as incomplete responses when the connection is closed)

# Sensor status detection
def check_moisture_status():
    return "The soil is dry and needs watering!" if GPIO.input(CHANNEL) else "The soil is moist and no watering is required."

# Main loop (4 detections per day, with a 6 - hour interval)
if __name__ == "__main__":
    try:
        while True:
            for _ in range(4):
                status = check_moisture_status()
                send_email("Real - Time Moisture Detection", f"Current status: {status}")
                time.sleep(14400)  # 6 - hour interval

            # Daily summary (optional, add as needed)
            # send_email("Daily Moisture Report", "All 4 detections today were normal...")

    except KeyboardInterrupt:
        print("\nProgram terminated, cleaning up GPIO resources...")
        GPIO.cleanup()
