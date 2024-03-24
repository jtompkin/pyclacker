# Changelog

- [0.1.0 - 2024-03-02](#010---2024-03-02)
- [0.1.1 - 2024-03-02](#011---2024-03-02)
- [1.0.0 - 2024-03-02](#100---2024-03-02)
- [1.0.1 - 2024-03-03](#101---2024-03-03)
- [1.0.2 - 2024-03-22](#102---2024-03-22)
- [1.0.3 - 2024-03-22](#103---2024-03-22)
- [1.1.0 - 2024-03-23](#110---2024-03-23)

## TODO

- [ ] Trig

## [0.1.0](https://github.com/jtompkin/pyclacker/releases/tag/v0.1.0) - 2024-03-02

Initial release

### Added

- Interactive mode
- Program input (buggy)

## [0.1.1](https://github.com/jtompkin/pyclacker/releases/tag/v0.1.1) - 2024-03-02

Minor patch for program input

### Added

- square root word: `sqrt`

### Fixed

- Providing program on command line did not always work

## [1.0.0](https://github.com/jtompkin/pyclacker/releases/tag/v1.0.0) - 2024-03-02

Big boy release

### Added

- Support for providing custom words in file
- Word definition using `=` in interactive mode
- pi word: `pi`

### Changed

- Now prints stack after last push in command
- Entering `\` no longer exits interactive mode (Use `<Ctrl-d>` (`<Ctrl-z>` on Windows))

## [1.0.1](https://github.com/jtompkin/pyclacker/releases/tag/v1.0.1) - 2024-03-03

Errors and stuff

### Added

- `pop` operator: Remove one item from the stack

### Fixed

- No longer attemts to calculate invalid exponentiation or division

## Changed

- Encountering an invalid calculation will now stop command parsing

## [1.0.2](https://github.com/jtompkin/pyclacker/releases/tag/v1.0.2) - 2024-03-22

Quittin' time

### Added

- `quit` operator: Exits interactive mode

## Changed

- `,` now pops one item from the stack. Use the `clear` operator to clear the entire stack

## [1.0.3](https://github.com/jtompkin/pyclacker/releases/tag/v1.0.3) - 2024-03-22

Le refactor

## Changed

- Rewrote most of the code
- Actions now return integers if they can

## Fixed

- Using `,` to pop an item when the stack is empty no longer raises an error
- Attempting to delete a word that is not defined no longer raises an error

## [1.1.0](https://github.com/jtompkin/pyclacker/releases/tag/v1.1.0) - 2024-03-23

I can never type factroial right

### Added

- `!` operator: Take factorial of value from stack
