import json
from .const import ID, WRITEABLE, VALUE, ALLOWED_VALUES


class BoschScan:
    def __init__(self, file_to_open):
        self._json = self.open_json(file_to_open)
        self._uris = {}
        self.create_uri()

    def create_uri(self):
        for arr in self._json:
            for line in arr:
                if ID in line:
                    self._uris[line[ID][1:]] = line

    def get_response(self, path):
        line = self._uris.get(path)
        if path == "gateway/uuid":
            print("path")
            if line[VALUE] == -1:
                line[VALUE] = "01010101"
                line[ALLOWED_VALUES] = "01010101"
        if line:
            return json.dumps(line, indent=None, separators=(',', ':'))

    def update_value(self, path, value):
        line = self._uris.get(path, None)
        is_writable = line.get(WRITEABLE, False)
        if line and line.get(WRITEABLE, False):
            line[VALUE] = value
            return True

    def open_json(self, file):
        """Open json file."""
        with open(file, "r") as db_file:
            datastore = json.load(db_file)
            return datastore
        return None