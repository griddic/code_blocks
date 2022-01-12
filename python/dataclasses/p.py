from structlog import get_logger

if __name__ == '__main__':
    log = get_logger()
    log.info("key_value_logging", out_of_the_box=True, effort=0)
