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
pyclacker [-h] [-v] [program]
```
Program should be provided as a string with commands separated by a space. Running without providing a program will enter interactive mode. In interactive mode, type a number and press enter to push to the stack. Enter an operator and press enter to perform the operation on the stack. Enter multiple commands separated by a space and press enter to execute them in order. Enter `help` to view available operators.
