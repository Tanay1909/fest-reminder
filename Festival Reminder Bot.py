from datetime import datetime
import time
from plyer import notification
import json
import os
import smtplib
from email.mime.text import MIMEText

FILENAME = "festivals.json"

# Your email credentials
SENDER_EMAIL = "YOUR_EMAIL@gmail.com"
SENDER_PASSWORD = "YOUR_PASSWORD"  # Preferably an App Password
RECEIVER_EMAIL = "RECEIVER_EMAIL@gmail.com"

default_festivals = {
    "Makar Sankranti": "2025-01-14",
    "Republic Day": "2025-01-26",
    "Maha Shivaratri": "2025-02-26",
    "Holi": "2025-03-14",
    "Ram Navami": "2025-04-06",
    "Mahavir Jayanti": "2025-04-10",
    "Good Friday": "2025-04-18",
    "Eid al-Fitr": "2025-03-31",
    "Buddha Purnima": "2025-05-12",
    "Guru Purnima": "2025-06-30",
    "Raksha Bandhan": "2025-08-09",
    "Janmashtami": "2025-08-16",
    "Independence Day": "2025-08-15",
    "Ganesh Chaturthi": "2025-08-29",
    "Navratri (Start)": "2025-09-22",
    "Durga Ashtami": "2025-09-30",
    "Dussehra (Vijayadashami)": "2025-10-02",
    "Karwa Chauth": "2025-10-14",
    "Diwali": "2025-10-20",
    "Govardhan Puja": "2025-10-21",
    "Bhai Dooj": "2025-10-23",
    "Chhath Puja": "2025-10-28",
    "Guru Nanak Jayanti": "2025-11-05",
    "Christmas": "2025-12-25"
}

def check_festivals_this_month(festivals):
    today = datetime.now().date()
    current_month = today.month
    current_year = today.year
    found = False

    print("\n📆 Festivals in This Month:")
    for name, date_str in festivals.items():
        try:
            fest_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if fest_date.month == current_month and fest_date.year == current_year:
                days_left = (fest_date - today).days
                if days_left >= 0:
                    message = f"{name} is in {days_left} day(s) on {fest_date.strftime('%d %B %Y')}!"
                    send_notification(name, message)
                    send_email(name, message)
                    print(f"🔔 {message}")
                    found = True
        except ValueError:
            print(f"❌ Invalid date format for {name}: {date_str}")

    if not found:
        print("✅ No upcoming festivals this month.")

def send_notification(title, message):
    notification.notify(
        title=f"🎉 {title}",
        message=message,
        timeout=10
    )

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = f"🎉 Festival Reminder: {subject}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("📧 Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def load_festivals():
    if not os.path.exists(FILENAME):
        save_festivals(default_festivals)
        return default_festivals
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Error loading festival file. Starting with defaults.")
        return default_festivals

def save_festivals(festivals):
    with open(FILENAME, "w") as f:
        json.dump(festivals, f, indent=4)

def main():
    print("\n🔁 Festival Reminder Bot is running... (press Ctrl+C to stop)")
    while True:
        festivals = load_festivals()
        check_festivals_this_month(festivals)
        print("⏰ Sleeping for 24 hours...\n")
        time.sleep(86400)  # 24 hours

if __name__ == "__main__":
    main()
    