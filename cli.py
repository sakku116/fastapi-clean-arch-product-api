from config.mongodb import getMongoDB
from repository.user import UserRepo
from utils.seeder.users import seedUsers
import logging
import typer
from datetime import datetime
from pytz import timezone
from config.env import Env

# logging config
logging.Formatter.converter = lambda *args: datetime.now(
    tz=timezone(Env.TIMEZONE)
).timetuple()
logging.basicConfig(
    level=logging.DEBUG if Env.DEBUG else logging.INFO,
    format="%(asctime)s %(levelname)s \033[92m%(message)s  ...[%(pathname)s@%(funcName)s():%(lineno)d]\033[0m",
    datefmt="%d/%m/%Y %H:%M:%S",
)

database = getMongoDB()

# repositories
user_repo = UserRepo(database)

app = typer.Typer()


@app.command()
def ping():
    print("pong")


@app.command()
def seed_users():
    seedUsers(user_repo=user_repo)


if __name__ == "__main__":
    app()
