import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pytz import timezone
from uvicorn.config import LOGGING_CONFIG

from config.env import Env
from config.mongodb import getMongoDB
from exception.http import CustomHTTPExc
from utils import exception as exception_utils
from utils import mongodb as mongodb_utils

# logging config
logging.Formatter.converter = lambda *args: datetime.now(
    tz=timezone(Env.TIMEZONE)
).timetuple()
logging.basicConfig(
    level=logging.DEBUG if Env.DEBUG else logging.INFO,
    format="%(asctime)s %(levelname)s: \033[92m%(message)s  ...[%(pathname)s@%(funcName)s():%(lineno)d]\033[0m",
    datefmt="%d-%m-%Y %H:%M:%S",
)

# default uvicorn logging format
LOGGING_CONFIG["formatters"]["default"][
    "fmt"
] = "%(asctime)s %(levelprefix)s %(message)s"
LOGGING_CONFIG["formatters"]["default"]["datefmt"] = "%d-%m-%Y %H:%M:%S"
# api call format
LOGGING_CONFIG["formatters"]["access"][
    "fmt"
] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
LOGGING_CONFIG["formatters"]["access"]["datefmt"] = "%d-%m-%Y %H:%M:%S"

app = FastAPI()

# register exception handlers
app.add_exception_handler(CustomHTTPExc, exception_utils.customHttpExceptionHandler)
app.add_exception_handler(Exception, exception_utils.defaultHttpExceptionHandler)

# register middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    mongodb = getMongoDB()
    mongodb_utils.ensureIndexes(db=mongodb)

    uvicorn.run(
        "main:app",
        host=Env.HOST,
        port=Env.PORT,
        reload=Env.RELOAD,
    )
