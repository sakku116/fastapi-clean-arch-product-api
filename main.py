import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pytz import timezone

from config.env import Env

# logging config
logging.Formatter.converter = lambda *args: datetime.now(
    tz=timezone(Env.TIMEZONE)
).timetuple()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelprefix)s \033[92m%(message)s  ...[%(pathname)s@%(funcName)s():%(lineno)d]\033[0m",
    datefmt="%d/%m/%Y %H:%M:%S",
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Env.HOST,
        port=Env.PORT,
        reload=Env.RELOAD,
    )
