from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print_document(self):
        pass


class Scanner(ABC):
    @abstractmethod
    def scan_document(self):
        pass


class BasicPrinter(Printer):
    def print_document(self):
        print("Printing document")


class AdvancedPrinter(Printer, Scanner):
    def print_document(self):
        print("Printing document")

    def scan_document(self):
        print("Scanning document")


printer = BasicPrinter()
printer.print_document()

machine = AdvancedPrinter()
machine.scan_document()