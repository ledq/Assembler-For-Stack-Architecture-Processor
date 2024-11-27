# Stack Architecture Assembler

This repository contains a Python-based assembler for **Kant**, a custom-designed stack architecture processor. The assembler translates human-readable assembly code into machine code that can be executed on the Kant processor. 
## Features

- **Assembly Language Support**: Converts assembly language instructions into binary machine code.
- **PC-Relative Addressing**: Simplifies branching and jump instructions with support for labels.
- **Error Handling**: Includes basic error handling for syntax and label resolution.
- **Easy-to-Use Interface**: Command-line tool that processes assembly code from `.txt` files.

## How It Works

### The Processor (Kant)

The assembler is designed for **Kant**, a stack-based architecture with the following features:
- **16 stack registers** with 2-byte word size.
- Instructions are 4 bytes, consisting of a 1-byte opcode and optional arguments.
- PC-relative addressing for branch and jump instructions.
- Separate data and instruction memory to prevent overwriting.

### Assembly Syntax

The assembler supports common stack-based instructions like:
- Arithmetic: `add`, `sub`
- Logical: `and`, `or`, `xor`
- Stack operations: `push`, `pop`
- Branching: `beq`, `blt`, `bgt`
- Control: `jal`, `jr`

Refer to the [Instruction Set Specification](#instruction-set-specification) for the complete list of supported instructions.

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

Clone the repository:
   ```bash
   git clone https://github.com/ledq/Assembler-For-Stack-Architecture-Processor.git
   cd Assembler-For-Stack-Architecture-Processor
   ```


## Usage

To run the assembler, use the following command:
```bash
python assembler.py <input_file>.txt
```

For example:
```bash
python assembler.py example_program.txt
```

The assembler generates a corresponding `.bin` file with the machine code output.

### Example Usage

Given the following input assembly code in `example_program.txt`:
```assembly
pushi 5
pushi 10
add
```

The assembler produces this machine code in `example_program.bin`:
```plaintext
00000100 00000101
00000100 00001010
00000101
```


## Acknowledgments

This assembler is inspired by the **Kant Processor** designed during the CSSE232 Final Project. Special thanks to:
- Curtis Knaack
- Matthew Greenberg
- Alex Sloan
- Duy Le


## Instruction Set Specification

Below is a summary of the instruction set the assembler supports. Each instruction is represented by an opcode and optional arguments.

| Instruction | Opcode      | Type | Description                                                               |
|-------------|-------------|------|---------------------------------------------------------------------------|
| `push`      | `00000000`  | I    | Push the value at the memory address to the top of the stack              |
| `pop`       | `00000001`  | I    | Pop the top of the stack to the memory address                            |
| `pushr`     | `00000010`  | I    | Push the value at the memory address to the top of the return stack       |
| `popr`      | `00000011`  | I    | Pop the top of the return stack to the memory address                     |
| `pushi`     | `00000100`  | I    | Push the immediate value to the top of the stack                          |
| `add`       | `00000101`  | S    | Add the top two values on the stack and push the result                   |
| `sub`       | `00000110`  | S    | Subtract the top value from the second value on the stack and push result |
| `or`        | `00000111`  | S    | Perform bitwise OR on the top two stack values and push result            |
| `and`       | `00001000`  | S    | Perform bitwise AND on the top two stack values and push result           |
| `xor`       | `00001001`  | S    | Perform bitwise XOR on the top two stack values and push result           |
| `sl`        | `00001010`  | S    | Shift the top of the stack left by 1                                      |
| `sr`        | `00001011`  | S    | Shift the top of the stack right by 1                                     |
| `jal`       | `00001100`  | I    | Jump to the address in the immediate and push the return address          |
| `jr`        | `00001101`  | I    | Jump to the address stored in the input register                          |
| `j`         | `00001110`  | I    | Jump to the address specified in the immediate                            |
| `beq`       | `00001111`  | I    | Branch if the top two stack values are equal                              |
| `blt`       | `00010000`  | I    | Branch if the top value is less than the second value on the stack        |
| `bgt`       | `00010001`  | I    | Branch if the top value is greater than the second value on the stack     |


## Future Enhancements

Potential improvements for this project include:
- Enhanced error handling for invalid syntax or unsupported instructions.
- Support for additional output formats (e.g., JSON or binary files).
- Development of debugging tools for assembly code.
