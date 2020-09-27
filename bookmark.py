import datetime


class Bookmark:
    def __init__(self):
        self.datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    def read(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    def str_to_date(self, bookmark_str):
        return datetime.datetime.strptime(bookmark_str, self.datetime_format)


class FileBookmark(Bookmark):
    def read(self):
        with open("bookmark.txt", "r") as f:
            bookmark_str = f.read()
        return self.str_to_date(bookmark_str)

    def write(self, new_bookmark):
        with open("bookmark.txt", "w") as f:
            f.write(new_bookmark.strftime(self.datetime_format))
