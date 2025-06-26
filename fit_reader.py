from fitparse import FitFile


class FitReader:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_heart_rate(self):
        seconds = 0
        fit_file = FitFile(self.file_name)
        start_time = None
        time_delta = None
        heart_rate = None

        for record in fit_file.get_messages("record"):
            for field in record:
                if field.name == "timestamp":
                    timestamp = field.value  # This is already a datetime object
                    if start_time is None:
                        start_time = field.value
                    time_delta = timestamp - start_time
                elif field.name == "heart_rate":
                    heart_rate = field.value
            while time_delta.seconds >= seconds:
                seconds = yield heart_rate
        while True:
            yield None  # yield None if there is no new data
