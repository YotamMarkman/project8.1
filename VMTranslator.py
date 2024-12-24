from Parser import Parser
from CodeWriter import CodeWriter
import sys

class VMTranslator:
    def __init__(self, input_file: str):

        self.parser = Parser(input_file)
        self.output_file = input_file.replace(".vm", ".asm") #creates the output file
        self.code = CodeWriter(self.output_file)

    def write_bootstrap(self):
        self.code.sys_init()

    def translate(self):
        while self.parser.has_more_lines():
            self.parser.advance()
            command_type = self.parser.command_type().value
            if command_type == 'C_ARITHMETIC':
                self.code.write_arithmetic(self.parser.arg1())

            elif command_type == 'C_PUSH' or command_type == 'C_POP':
                self.code.write_push_pop(
                    command_type,
                    self.parser.arg1(),
                    self.parser.arg2(), )

            elif command_type == 'C_LABEL':
                self.code.write_label(self.parser.arg1())

            elif command_type == 'C_GOTO':
                self.code.write_go_to(self.parser.arg1())

            elif command_type == 'C_IF':
                self.code.write_if(self.parser.arg1())

            elif command_type == 'C_FUNCTION':
                self.code.write_function(self.parser.arg1(), self.parser.arg2())

            elif command_type == 'C_RETURN':
                self.code.write_return()

            else:
                self.code.write_call(self.parser.arg1(), self.parser.arg2())
        self.code.close()

