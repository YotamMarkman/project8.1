import sys

from CodeWriter import *
from Parser import *

class Main:
    def __init__(self):
        self.path = sys.argv[1]
        if os.path.isdir(self.path):
            dir_file_path = os.path.join(self.path, "dir.vm")
            open(dir_file_path, 'w').close()
            for file in os.listdir(self.path):
                if file.endswith(".vm"):
                    full_file_path = os.path.join(self.path, file)
                    with open(full_file_path, 'r') as vm_file, open(dir_file_path, 'a') as dir_file:
                        if not full_file_path.endswith("dir.vm"):
                            dir_file.write(vm_file.read())
            self.input_file = Parser(dir_file_path)
            self.output_file = CodeWriter(dir_file_path)
        else:
            self.input_file = Parser(self.path)
            self.output_file = CodeWriter(self.path)

    def main(self):
        while self.input_file.has_more_lines():
            self.input_file.advance()
            command_type = self.input_file.command_type().value
            self.output_file.write_arithmetic(self.input_file.arg1()) if command_type == 'C_ARITHMETIC' else (
                self.output_file.write_push_pop(
                    command_type,
                    self.input_file.arg1(),
                    self.input_file.arg2(),
                ))
        self.output_file.close()

if __name__ == "__main__":
    translator = Main()
    translator.main()