import argparse
from espn_ffb import util
from espn_ffb.db.database import db
# noinspection PyUnresolvedReferences
from espn_ffb.db.model import champions, matchups, owners, records, sackos, teams
from flask import Flask
import logging
from typing import Mapping

app = Flask(__name__)


def parse_args() -> Mapping:
    """

    :return: dict of parsed arguments
    """
    parser = argparse.ArgumentParser(description="Create tables and insert into database.")
    parser.add_argument('-e', '--environment', help="The development environment", type=str, required=True,
                        choices=util.SUPPORTED_ENVIRONMENTS)
    return vars(parser.parse_args())


# noinspection DuplicatedCode
def main():
    util.configure_app(app, parse_args().get("environment"), set_logging=True)

    with app.app_context():
        logging.info("Dropping tables")
        db.drop_all()
        logging.info("Creating tables")
        db.create_all()


if __name__ == "__main__":
    main()
