import datetime
import json
import logging
import os

logger = logging.getLogger(__name__)


class JsonFile:
    """About .json file."""

    def __init__(self, filepath):
        self.filepath = filepath

    @property
    def data(self):
        return self.read()

    def read(self, nulldata=[]):
        if not os.path.exists(self.filepath):
            return nulldata

        try:
            with open(self.filepath, "r", encoding="utf-8") as _file:
                return json.load(_file)
        except Exception as err:
            logger.warning("read file failed.%s", err)

        return nulldata

    def write(self, data, indent=1, is_cover=True):

        filepath = self.filepath
        if os.path.exists(self.filepath) and is_cover is False:
            filepath += f"_{datetime.date.today()}_temp.json"

        # check the dirpath exists and makedirs.
        dirpath = os.path.dirname(os.path.abspath(filepath))
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        with open(filepath, "w", encoding="utf-8") as _file:
            try:
                json.dump(
                    data, _file, indent=indent, sort_keys=False, ensure_ascii=False
                )
            except:
                json.dump(
                    data,
                    _file,
                    indent=indent,
                    sort_keys=False,
                    ensure_ascii=False,
                )
