from model.google_sheets import connect_sheet


class UploadData:
    def __init__(self):
        self.sheet = connect_sheet()

    def clean_value(self, value):
        """
        Remove newlines, extra spaces and make everything one clean string.
        """
        if not value:
            return ""

        value = str(value)
        value = value.replace("\n", " ")
        value = value.replace("\r", " ")
        value = " ".join(value.split())  # remove extra spaces
        return value.strip()

    def save(self, data):
        row = [
            self.clean_value(data.get("Name")),
            self.clean_value(data.get("Type")),
            self.clean_value(data.get("id")),
            self.clean_value(data.get("date")),
            self.clean_value(data.get("DSLID")),
            self.clean_value(data.get("Tariff plan")),
            self.clean_value(data.get("TEL")),
            self.clean_value(data.get("Address"))
        ]

        print("FINAL ROW BEING SENT:", row)

        self.sheet.append_row(row, value_input_option="RAW")