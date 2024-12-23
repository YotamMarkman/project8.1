import sys
from itertools import count

from CodeWriter import *
from Parser import *

class Main:
    def __init__(self):
        self.vm_counter = 0
        self.path = sys.argv[1]
        if os.path.isdir(self.path):
            dir_file_path = os.path.join(self.path, "dir.vm")
            open(dir_file_path, 'w').close()
            for file in os.listdir(self.path):
                if file.endswith(".vm"):
                    self.vm_counter += 1
                    full_file_path = os.path.join(self.path, file)
                    with open(full_file_path, 'r') as vm_file, open(dir_file_path, 'a') as dir_file:
                        if not full_file_path.endswith("dir.vm"):
                            dir_file.write(vm_file.read())
            self.input_file = Parser(dir_file_path)
            self.output_file = CodeWriter(dir_file_path, self.input_file.getname())
        else:
            self.input_file = Parser(self.path)
            self.output_file = CodeWriter(self.path, self.input_file.getname())

    def main(self):
        if self.vm_counter >= 1 or os.path.isdir(self.path):
            self.output_file.sys_init()
        while self.input_file.has_more_lines():
            self.input_file.advance()
            command_type = self.input_file.command_type().value
            if command_type == 'C_ARITHMETIC':
                self.output_file.write_arithmetic(self.input_file.arg1())

            elif command_type == 'C_PUSH' or command_type == 'C_POP':
                self.output_file.write_push_pop(
                    command_type,
                    self.input_file.arg1(),
                    self.input_file.arg2(),)

            elif command_type == 'C_LABEL':
                self.output_file.write_label(self.input_file.arg1())

            elif command_type == 'C_GOTO':
                self.output_file.write_go_to(self.input_file.arg1())

            elif command_type == 'C_IF':
                self.output_file.write_if(self.input_file.arg1())

            elif command_type == 'C_FUNCTION':
                self.output_file.write_function(self.input_file.arg1(), self.input_file.arg2())

            elif command_type == 'C_RETURN':
                self.output_file.write_return()

            else:
                self.output_file.write_call(self.input_file.arg1(), self.input_file.arg2())
        self.output_file.close()

if __name__ == "__main__":
    translator = Main()
    translator.main()