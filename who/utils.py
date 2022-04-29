import logging


def set_log_level(logger, level):

    logger.setLevel(
        logging.INFO
        if level == "info"
        else (logging.DEBUG if level == "debug" else logging.WARN)
    )


def get_logger(name):

    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
