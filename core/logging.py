import logging
import os

class PackagePathFilter(logging.Filter):
    def filter(self, record):
        record.pathname = record.pathname.replace(os.getcwd(), "")
        return True
