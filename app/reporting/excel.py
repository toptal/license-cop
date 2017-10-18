import xlsxwriter

from app.reporting.report import Report


class ExcelReport(Report):

    def __init__(self, file, max_depth=None):
        super().__init__(max_depth)
        workbook = xlsxwriter.Workbook(file, {'constant_memory': True})
        self.__workbook = workbook
        self.__worksheet = workbook.add_worksheet()
        self.__row = 1
        self.__header_format = workbook.add_format({'bold': True})
        self.__empty_licenses_format = workbook.add_format({'bg_color': 'yellow'})
        self.__write_headers()

    def _write(self, resolution):
        for dependency in resolution.reverse_dependencies():
            self.__write_row(resolution.package_descriptor, dependency)

    def close(self):
        return self.__workbook.close()

    def __write_row(self, descriptor, dependency):
        version = dependency.version
        self.__worksheet.write_string(self.__row, 0, descriptor.repository.name)
        self.__worksheet.write_string(self.__row, 1, str(descriptor.platform))
        self.__worksheet.write_string(self.__row, 2, descriptor.formatted_paths)
        self.__worksheet.write_string(self.__row, 3, str(version.name))
        self.__worksheet.write_string(self.__row, 4, version.formatted_number)
        self.__worksheet.write_string(self.__row, 5, version.formatted_licenses, (
            None if version.licenses else self.__empty_licenses_format))
        self.__worksheet.write_string(self.__row, 6, dependency.formatted_runtime_references)
        self.__worksheet.write_string(self.__row, 7, dependency.formatted_development_references)
        self.__row += 1

    def __write_headers(self):
        self.__worksheet.write_string(0, 0, 'Repository', self.__header_format)
        self.__worksheet.write_string(0, 1, 'Platform', self.__header_format)
        self.__worksheet.write_string(0, 2, 'Package Descriptor', self.__header_format)
        self.__worksheet.write_string(0, 3, 'Package Name', self.__header_format)
        self.__worksheet.write_string(0, 4, 'Package Version', self.__header_format)
        self.__worksheet.write_string(0, 5, 'Package Licenses', self.__header_format)
        self.__worksheet.write_string(0, 6, 'Runtime References', self.__header_format)
        self.__worksheet.write_string(0, 7, 'Development References', self.__header_format)
