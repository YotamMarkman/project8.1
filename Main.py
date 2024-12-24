from VMTranslator import VMTranslator
import os
import sys


def main():
    input_path = sys.argv[1]

    if os.path.isfile(input_path):
        translator = VMTranslator(input_path)
        translator.translate()

    elif os.path.isdir(input_path):
        vm_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.vm')]
        num_of_vm_files = len(vm_files)
        if num_of_vm_files>1:
            if not vm_files:
                print("No .vm files found in the directory!")
                return
            dir_name = os.path.basename(input_path)
            output_file_path = os.path.join(input_path, f"{dir_name}.asm")

            for i, vm_file_path in enumerate(vm_files):
                translator = VMTranslator(vm_file_path)

                if i==0:
                    translator.write_bootstrap()

                translator.translate()

            with open(output_file_path, 'w') as output_file:
                for vm_file_path in vm_files:
                    asm_file_path = vm_file_path.replace('.vm', '.asm')
                    with open(asm_file_path, 'r') as asm_file:
                        output_file.write(asm_file.read() + "\n")
                    os.remove(asm_file_path)
        else:
            vm_file_path = vm_files[0]
            translator = VMTranslator(vm_file_path)
            translator.translate()

            dir_name = os.path.basename(input_path)
            output_file_path = os.path.join(input_path, f"{dir_name}.asm")

            asm_file_path = vm_file_path.replace('.vm', '.asm')
            os.rename(asm_file_path, output_file_path)


if __name__ == "__main__":
    main()
