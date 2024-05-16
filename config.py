import logging

SIZE = 800, 600


def get_boundaries():
    return 0 + 75, 0 + 75, SIZE[0] - 75, SIZE[1] - 75


logger = logging.getLogger("game")
logger.setLevel(logging.DEBUG)
