import os
from multiprocessing.forkserver import set_forkserver_preload


class CodeWriter:
    call_counter = 0
    def __init__(self, output_file: str, file_name: str = None):
        """
        Initializes the CodeWriter to write assembly code to the specified file.

        :param output_file: The path to the output assembly file.
        """
        self.current_file_name = ""
        normalized_path = os.path.normpath(output_file)
        self.file_base_name = os.path.splitext(os.path.basename(output_file))[0]
        self.file = open(normalized_path, 'w')
        self.label_counter = 0

        self.set_file_name(output_file)

    def set_file_name (self, file_name: str):
        self.current_file_name = os.path.splitext(os.path.basename(file_name))[0]

    def write_add(self):
        self.file.write(
            '@SP\n'
            'AM=M-1\n'
            'D=M\n'
            'A=A-1\n'
            'M=D+M\n'
        )

    def write_sub(self):
        self.file.write(
            '@SP\n'
            'AM=M-1\n'
            'D=M\n'
            'A=A-1\n'
            'M=M-D\n'
        )

    def write_and(self):
        self.file.write(
            '@SP\n'
            'AM=M-1\n'
            'D=M\n'
            'A=A-1\n'
            'M=D&M\n'
        )

    def write_or(self):
        self.file.write(
            '@SP\n'
            'AM=M-1\n'
            'D=M\n'
            'A=A-1\n'
            'M=D|M\n'
        )

    def write_neg(self):
        self.file.write(
            '@SP\n'
            'A=M-1\n'
            'M=-M\n'
        )

    def write_not(self):
        self.file.write(
            '@SP\n'
            'A=M-1\n'
            'M=!M\n'
        )

    def write_eq(self):
        self.write_compare_command('JNE')

    def write_gt(self):
        self.write_compare_command('JLE')

    def write_lt(self):
        self.write_compare_command('JGE')

    def write_compare_command(self, jump_type):
        self.file.write(
            '@SP\n'
            'AM=M-1\n'  
            'D=M\n'  
            'A=A-1\n'  
            'D=M-D\n'  
            f'@FALSE{self.label_counter}\n'
            f'D;{jump_type}\n' 
            '@SP\n'
            'A=M-1\n'
            'M=-1\n' 
            f'@CONTINUE{self.label_counter}\n'
            '0;JMP\n'
            f'(FALSE{self.label_counter})\n'
            '@SP\n'
            'A=M-1\n'
            'M=0\n' 
            f'(CONTINUE{self.label_counter})\n'
        )
        self.label_counter += 1

    def write_arithmetic(self, command: str):
        """
        Writes the assembly code for an arithmetic or logical command.

        :param command: The arithmetic/logical command.
        """
        two_args_commands = ['add', 'sub', 'eq', 'gt', 'lt', 'and', 'or']
        two_args_method_map = {
            'add': self.write_add,
            'sub': self.write_sub,
            'eq': self.write_eq,
            'lt': self.write_lt,
            'gt': self.write_gt,
            'and': self.write_and,
            'or': self.write_or,
        }
        one_arg_method_map = {
            'neg': self.write_neg,
            'not': self.write_not,
        }
        command = command.strip()
        self.file.write(f"// {command}\n")
        if command in two_args_commands:
            two_args_method_map[command]()
        elif command in one_arg_method_map:
            one_arg_method_map[command]()
        else:
            raise ValueError(f"Invalid arithmetic command: {command}")

    def write_push_pop(self, command_type: str, segment: str, index: int):
        """
        Writes the assembly code for a push or pop command.

        :param command_type: Either "C_PUSH" or "C_POP".
        :param segment: The memory segment (e.g., 'constant', 'local').
        :param index: The index in the segment.
        """
        command_name = "pop" if command_type == "C_POP" else "push"
        self.file.write(f"//{command_name.strip()} {segment} {str(index)}\n")
        if command_type == 'C_PUSH':
            if 'constant' in segment :
                self.file.write(f"@{index}\n")
                self.file.write("D=A\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            elif 'local' in segment :
                self.file.write("@" + str(index) + "\n")
                self.file.write("D=A\n")
                self.file.write("@LCL\n")
                self.file.write("A=D+M\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif 'argument' in segment :
                self.file.write("@" + str(index) + "\n")
                self.file.write("D=A\n")
                self.file.write("@ARG\n")
                self.file.write("A=D+M\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif 'this' in segment :
                self.file.write("@" + str(index) + "\n")
                self.file.write("D=A\n")
                self.file.write("@THIS\n")
                self.file.write("A=D+M\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif 'that' in segment :
                self.file.write("@" + str(index) + "\n")
                self.file.write("D=A\n")
                self.file.write("@THAT\n")
                self.file.write("A=D+M\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif 'temp' in segment :
                address = 5 + index
                self.file.write("@" + str(address) + "\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif 'pointer' in segment :
                if index == 0 :
                    self.file.write("@" + str(3) + "\n")
                    self.file.write("D=M\n")
                    self.file.write("@SP\n")
                    self.file.write("A=M\n")
                    self.file.write("M=D\n")
                    self.file.write("@SP\n")
                    self.file.write("M=M+1\n")
                else:
                    self.file.write("@" + str(4) + "\n")
                    self.file.write("D=M\n")
                    self.file.write("@SP\n")
                    self.file.write("A=M\n")
                    self.file.write("M=D\n")
                    self.file.write("@SP\n")
                    self.file.write("M=M+1\n")
            else:
                self.file.write(f"@{self.current_file_name}.{index}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
        else:
            if 'local' in segment :
                self.file.write("@" + str(index) + "\n")
                self.file.write("D=A\n")
                self.file.write("@LCL\n")
                self.file.write("D=D+M\n")
                self.file.write("@R13\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write("@R13\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
            elif 'argument' in segment :
                self.file.write("@" + str(index) + "\n")
                self.file.write("D=A\n")
                self.file.write("@ARG\n")
                self.file.write("D=D+M\n")
                self.file.write("@R13\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write("@R13\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
            elif 'this' in segment :
                self.file.write("@" + str(index) + "\n")
                self.file.write("D=A\n")
                self.file.write("@THIS\n")
                self.file.write("D=D+M\n")
                self.file.write("@R13\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write("@R13\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
            elif 'that' in segment :
                self.file.write("@" + str(index) + "\n")
                self.file.write("D=A\n")
                self.file.write("@THAT\n")
                self.file.write("D=D+M\n")
                self.file.write("@R13\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write("@R13\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
            elif 'static' in segment :
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write(f"@{self.file_base_name}.{index}\n")
                self.file.write("M=D\n")
            elif 'temp' in segment :
                address = 5 + index
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write("@"+ str(address)+"\n")
                self.file.write("M=D\n")
            else:
                if index == 0 :
                    self.file.write("@SP\n")
                    self.file.write("M=M-1\n")
                    self.file.write("A=M\n")
                    self.file.write("D=M\n")
                    self.file.write("@3\n")
                    self.file.write("M=D\n")
                else:
                    self.file.write("@SP\n")
                    self.file.write("M=M-1\n")
                    self.file.write("A=M\n")
                    self.file.write("D=M\n")
                    self.file.write("@4\n")
                    self.file.write("M=D\n")

    def write_function(self, function_name: str, num_local_vars: int):
        self.file.write(f"// function {function_name} {num_local_vars}\n")
        self.file.write(f"({function_name})\n")
        if num_local_vars is None:
            num_local_vars = 0
        for i in range(num_local_vars):
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=0\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")


    def write_label(self, label: str):
        self.file.write(f"// label {label}\n")
        self.file.write(f"({label})\n")

    def write_go_to(self, label: str):
        self.file.write(f"// goto {label}\n")
        self.file.write(f"@{label}\n")
        self.file.write("0;JMP\n")

    def write_if(self, label: str):
        self.file.write(f"// if-goto {label}\n")
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write(f"@{label}\n")
        self.file.write("D;JNE\n")

    def write_call(self, function_name: str, num_args: int):
        if num_args is None:
            num_args = 0
        new_label = f"{function_name}$ret.{CodeWriter.call_counter}"
        CodeWriter.call_counter += 1
        self.file.write(f"// call {function_name} {num_args}\n")
        self.file.write(f"@{new_label}\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self.file.write(f"@{segment}\n")
            self.file.write("D=M\n")
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")

        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@5\n")
        self.file.write("D=D-A\n")
        self.file.write(f"@{num_args}\n")
        self.file.write("D=D-A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")

        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")

        self.file.write(f"@{function_name}\n")
        self.file.write("0;JMP\n")
        self.file.write(f"({new_label})\n")

    def write_return(self):
        self.file.write("// return call\n")
        self.file.write("@LCL\n")
        self.file.write("D=M\n")
        self.file.write("@R13\n")
        self.file.write("M=D\n")
        self.file.write("@5\n")
        self.file.write("A=D-A\n")
        self.file.write("D=M\n")
        self.file.write("@R14\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@ARG\n")
        self.file.write("D=M+1\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
        for i, string in enumerate(["THAT", "THIS", "ARG", "LCL"], start=1):
            self.file.write("@R13\n")
            self.file.write("D=M\n")
            self.file.write(f"@{int(i)}\n")
            self.file.write("A=D-A\n")
            self.file.write("D=M\n")
            self.file.write(f"@{string}\n")
            self.file.write("M=D\n")

        self.file.write("@R14\n")
        self.file.write("A=M\n")
        self.file.write("0;JMP\n")

    def sys_init(self):
        self.file.write("// Bootstrap code\n")
        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
        self.write_call("Sys.init", 0)

    def close(self):
        """
        Closes the output file.
        """
        self.file.close()