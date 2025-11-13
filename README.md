# Simple Text Editor

A tiny, line-based command-line text editor implemented in Python. It lets you
open or create a file, append or modify lines, and save changes explicitly by
typing the SAVE command.

## Quick start

Run the editor with Python 3:

```bash
python3 simple-text-editor.py [path/to/file.txt]
```

If you omit the filename, the program prompts you for one interactively.

## Interactive usage

When the editor starts you'll see a prompt. Commands are entered at the prompt.
Available commands (type at the prompt):

- SAVE — write the current buffer to disk and exit
- QUIT — exit without saving
- SHOW — display the current buffer with line numbers
- HELP — display help text
- INSERT N — insert a new line before line number N (1-based). You will be prompted for the text.
- DELETE N — delete line number N
- REPLACE N — replace line number N. You will be prompted for the new text.

Any other input will be appended as a new line to the end of the buffer.

Example session:

```
$ python3 simple-text-editor.py notes.txt
Editing file: notes.txt
Type HELP for available commands. Type SAVE to save and exit.
> Hello world
> SHOW
    1: Hello world
> INSERT 1
Insert text: First line
Inserted at line 1
> SHOW
    1: First line
    2: Hello world
> SAVE
Saved 2 lines to notes.txt
```

## Running automated (non-interactive) tests

This project contains no automated tests, but you can run quick checks by
running the script against a temporary file and ensuring it produces the
expected output.

## Ignored files

This repository contains a basic `.gitignore` that excludes Python bytecode
and common editor/OS artifacts (for example `__pycache__/`, `*.pyc`,
`.vscode/`, and `.DS_Store`). You can add more entries if you use other tools
or editors.

## Next steps / enhancements

- Add unit tests for load/save and command parsing
- Support multi-line paste or block editing
- Add search-and-replace functionality to find specific words or phrases and replace them across the buffer
- Add an option to choose whether saving overwrites the existing file or appends new text to the end
- Add an optional in-memory undo/redo stack

## Contributing

I would love your help! Contribute by forking the repo and opening pull requests. Please ensure that your code passes the existing tests and linting, and write tests to test your changes if applicable.

All pull requests should be submitted to the `main` branch.

## License

See the [LICENSE](LICENSE) file for details.