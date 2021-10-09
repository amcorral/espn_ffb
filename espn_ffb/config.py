import os


def get_db_uri(user, password, host, port, dbname):
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    # return f"mysql://{user}:{password}@{host}:{port}/{dbname}"
    # return f"oracle://{user}:{password}@{host}:{port}/{dbname}"


class Config(object):
    LEAGUE_ID = 384382
    CURRENT_YEAR = 2021
    DB_URI = ""
    COOKIES = {
        "swid": "{9F7CAD79-6266-43E7-BCAD-79626633E790}",
        "espn_s2": "AEChgJ78ombbkmGNc2tEuokQnaOeQgpeq9gZGzhIijmWKSxXuHF1hF8oA04mzUhOby3AFrD%2B3Qi20oofpcnaig90%2Bf8WJq6hwOwJU%2BJnBOthtJ5tueva2rid7pUwbaPafL7Bad7GAzcV%2B7PalB0b670IIPKAkc7eHH%2BCnTii7fSWdWYkOan64ABJw4QMD93o98x9Jokb5iPWNcRfNJ6LdZPWL%2BdxqlczqoiU54w5mu165TSlSD3Gp6zMhDVExbewW1mOwGp1A4uj2BYNl0mQgxtiuUZsCGyXs5oC%2BOcpLsZTp%2FiJZti1veAqmqYOSy6mj50%3D"
    }
    config_dir = "/etc/opt/espn-ffb"
    log_base_dir = "/var/log/espn-ffb"

    log_format = "%(asctime)s %(levelname)s %(pathname)s %(lineno)d: %(message)s"
    log_interval = 1
    console_level = 20
    rootlogger_level = 10
    filelog_level = 20
    log_backup_count = 90
    log_when = "midnight"


class DevConfig(Config):
    config_dir = "conf"
    log_base_dir = "log"
    # console_level = 10

    dbname = "your_dev_db"
    user = "your_dev_user"
    password = "your_dev_pw"
    host = "localhost"
    port = "5432"

    DB_URI = get_db_uri(user=user, password=password, host=host, port=port, dbname=dbname)


class DockerConfig(Config):
    dbname = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')

    DB_URI = get_db_uri(user=user, password=password, host=host, port=port, dbname=dbname)


class ProdConfig(Config):
    dbname = "your_prod_db"
    user = "your_prod_user"
    password = "your_prod_pw"
    host = "localhost"
    port = "5432"

    DB_URI = get_db_uri(user=user, password=password, host=host, port=port, dbname=dbname)
