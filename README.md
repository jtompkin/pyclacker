# pyclacker

Command line reverse polish notation (RPN) calculator. Stack based and ready to party.

Josh Tompkin

<jtompkin-dev@pm.me>

https://github.com/jtompkin/pyclacker

## Installation

Install with pip
```
pip3 install pyclacker
```

## Usage

```bash
pyclacker [-h] [-v] [-w WORDS_FILE] [program]
```
If provided, `program` should be a single string with commands separated by a space. Running without providing a program will enter interactive mode. In interactive mode, type a number and press enter to push to the stack. Enter an operator and press enter to perform the operation on the stack. Enter multiple commands separated by a space and press enter to execute them in order. Enter `help` to view available operators.

### Words

Custom commands (called words) can be defined in interpretive mode or in a file. To define words in a file, provide one word definition on each line. A word definition consists of the word itself and its definition, all separated by spaces. Provide the path to this file when calling the program with `-w`. A file containing the following two lines would define two words: `sqrt`, which pushes 0.5 to the stack and then calls the exponent operator, and `pi`, which pushes the value of pi to the stack

```
sqrt 0.5 ^
pi 3.14159265358979323846
```

To define words in interactive mode, start your command with `=`, followed by a space, followed by the word itself, followed by the word definition, again all separated by spaces. The following commands would accomplish the same word definitions as the file above. (The `>` is not typed)

```
  > = sqrt 0.5 ^
  > = pi 3.14159265358979323846
```

You can undefine a word by providing its name without any definition. All currently defined words can be viewed by entering `words` at the interactive prompt.

```
  > = sqrt
```
