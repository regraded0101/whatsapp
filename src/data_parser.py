import re
from datetime import datetime


class ChatParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.datetime_format = "%d/%m/%Y, %H:%M"
        self.dateTimeRegex = "^\d{2}/\d{2}/\d{4}\,\s+\d{2}:\d{2}"
        self.nameRegex = "^[^:]+"
        self.raw_data = self.load_data()
        self._chat = self.raw_data
        self.nonStandardRows = []

    def load_data(self):
        with open(self.filepath, "r") as file:
            return [line for i, line in enumerate(file) if i > 0]

    def extract_datetimes(self):
        messageDateTimes = []
        for row, message in enumerate(self._chat):
            messageDateTime = re.findall(self.dateTimeRegex, message)
            messageDateTime = (
                datetime.strptime(messageDateTime[0], self.datetime_format)
                if len(messageDateTime) > 0
                else None
            )
            self.nonStandardRows.append(row) if messageDateTime is None else None
            messageDateTimes.append(messageDateTime)

        for i, message in enumerate(self._chat):
            message = re.sub(self.dateTimeRegex, "", message)
            message = re.sub(" - ", "", message)
            self._chat[i] = message
        return messageDateTimes

    def extract_names(self):
        messageNames = []
        for row, message in enumerate(self._chat):
            if row not in self.nonStandardRows:
                messageNames.append(re.findall(self.nameRegex, message)[0])

            else:
                messageNames.append(None)

        for i, message in enumerate(self._chat):
            message = re.sub(self.nameRegex + ": ", "", message)
            self._chat[i] = message.strip()

        return messageNames

    def parse_data(self):
        dateTimes = self.extract_datetimes()
        names = self.extract_names()

        return {
            row: [dateTimes[row], names[row], self._chat[row]]
            for row in range(0, len(self._chat))
        }


if __name__ == "__main__":
    Chat = ChatParser("data/WhatsApp Chat with Izzie Fuller.txt")
    print(Chat.parse_data())
