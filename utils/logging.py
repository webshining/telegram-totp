import logging
import json

from loguru import logger

from data.config import DIR


# def serialize(record):
#     subset = {
#         "timestamp": record["time"].timestamp(),
#         "level": record["level"].name,
#         "message": record["message"],
#     }
#     return json.dumps(subset)
#
#
# def patching(record):
#     record["extra"]["serialized"] = serialize(record)
#
#
# logger.remove(0)
# logger = logger.patch(patching)
# logger.add(
#     f"{DIR}/logs/app.json",
#     format="{extra[serialized]}",
#     rotation="1 day",
#     retention="1 month",
# )
#
#
# def setup_logger(name: str) -> None:
#     class CustomFilter(logging.Filter):
#         def filter(self, record):
#             return "Failed to fetch updates" not in record.getMessage()
#
#     log = logging.getLogger(name)
#     log.addFilter(CustomFilter())
#     log.setLevel(logging.ERROR)
#
#
# setup_logger("aiogram")
# setup_logger("aiogram.dispatcher")
