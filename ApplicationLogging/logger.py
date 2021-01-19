from datetime import datetime

class AppLogeer:

    def __init__(self):
        pass

    def log(self, file_object, log_message):
        self.now = datetime.now()
        self.date = self.now.date()
        self.currentTime  =self.date.strftime("%H:%M:%S")
        file_object.write(
            str(self.date) + "/" +str(self.currentTime) + "\t\t" + log_message + "\n"
        )
