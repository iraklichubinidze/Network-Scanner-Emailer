from scanner import scan_ips
from report_generator import generate_html_report
from emailer import send_email
import os

# Configuration
INPUT_FILE = "ips.txt"
OUTPUT_DIR = "output"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_LOGIN = "<SMTP-EMAIL>"
SMTP_PASSWORD = "<YOUR-PASSWORD>"
SENDER_EMAIL = "<SENDER-EMAIL>"
RECEIVER_EMAILS = ["<RECEIVER1>@example.com", "<RECEIVER2>@example.com"]

def main():
    print("Starting Nmap scan...")
    scan_results = scan_ips(INPUT_FILE, OUTPUT_DIR)
    print("Nmap scan completed.")

    print("Generating HTML report...")
    html_report_path = generate_html_report(scan_results, OUTPUT_DIR)
    print(f"HTML report saved at: {html_report_path}")

    print("Sending email with the report...")
    send_email(SMTP_SERVER, SMTP_PORT, SMTP_LOGIN, SMTP_PASSWORD, SENDER_EMAIL, RECEIVER_EMAILS, html_report_path)
    print("Email sent successfully.")

if __name__ == "__main__":
    main()
