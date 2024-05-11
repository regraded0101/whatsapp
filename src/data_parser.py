import re
from datetime import datetime


class ChatParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.datetime_format = "%d/%m/%Y, %H:%M"
        self.dateTimeRegex = "^\d{2}/\d{2}/\d{4}\,\s+\d{2}:\d{2}"
        self.raw_data = self.load_data()
        self._chat = self.raw_data

    def load_data(self):
        with open(self.filepath, "r") as file:
            return [line for i, line in enumerate(file) if i > 0]

    def extract_datetimes(self):
        messageDateTimes = []
        for message in self._chat:
            messageDateTime = re.findall(self.dateTimeRegex, message)
            messageDateTime = (
                datetime.strptime(messageDateTime[0], self.datetime_format)
                if len(messageDateTime) > 0
                else None
            )
            messageDateTimes.append(messageDateTime)

        for row, message in enumerate(self._chat):
            message = re.sub(self.dateTimeRegex, "", message)
            message = re.sub(" - ", "", message)
            self._chat[row] = message

        return messageDateTimes


if __name__ == "__main__":
    Chat = ChatParser("data/WhatsApp Chat with Izzie Fuller.txt")
    Chat.extract_datetimes()
    print(Chat._chat)
