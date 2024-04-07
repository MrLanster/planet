import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_verification_email(recipient_email, verification_link):
    sender_email = "notescratchonline@gmail.com"
    subject = "Account Verification"

    greeting = "Hello!"
    
    button_html = f'<a href="{verification_link}" style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;">Verify Account</a>'

    html_content = f"""
    <html>
      <body>
        <p>{greeting}</p>
        <p>Please click the button below to verify your account:</p>
        {button_html}
      </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587  

    smtp_username = "notescratchonline@gmail.com"
    smtp_password = "tkjs cmsk zzrk vugc"  

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Verification email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


