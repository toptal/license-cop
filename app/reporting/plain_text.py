from app.reporting.report import Report


class PlainTextReport(Report):

    def __init__(self, filename):
        super().__init__()
        self.__file = open(filename, 'w')

    def _write(self, resolution):
        print(repr(resolution), file=self.__file)
        print('-' * 70, file=self.__file)
        print(file=self.__file)

    def close(self):
        self.__file.close()
