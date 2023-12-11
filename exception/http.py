class CustomHTTPExc(Exception):
    def __init__(self, status_code=500, message="exception", data=None, detail=""):
        self.status_code = status_code
        self.message = message
        self.data = data
        self.detail = detail

        super().__init__(message if not detail else detail)