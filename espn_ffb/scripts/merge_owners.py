import argparse
from espn_ffb import util
from espn_ffb.db.merge_owners import merge_owners
from flask import Flask

app = Flask(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Generates weekly recap templates.")
    parser.add_argument(
        "-e",
        "--environment",
        help="The development environment",
        type=str,
        required=True,
        choices=util.SUPPORTED_ENVIRONMENTS,
    )
    parser.add_argument(
        "-o",
        "--old_owner_id",
        help="The old owner id to be removed",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-n",
        "--new_owner_id",
        help="The new owner id with merged data",
        type=str,
        required=True,
    )
    return vars(parser.parse_args())


def main():
    args = parse_args()
    old_owner_id = args.get("old_owner_id")
    new_owner_id = args.get("new_owner_id")

    util.configure_app(app, args.get("environment"), set_logging=True)
    with app.app_context():
        merge_owners(old_owner_id, new_owner_id)


if __name__ == "__main__":
    main()
