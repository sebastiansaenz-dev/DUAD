

class ExportToCsv:
    def export_file(self):
        print('exporting to csv')

class Document:
    def __init__(self, content):
        self.content = content

class Report(Document, ExportToCsv):
    pass

class AnotherReport(Document, ExportToCsv):
    pass


my_report = Report('multiple inheritance')
my_report.export_file()

my_second_report = Report('multiple inheritance 2.0')
my_second_report.export_file()