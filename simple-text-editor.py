from __future__ import annotations

import argparse
import os
import sys
import tempfile
from typing import List


# ----------------------
# Argument parsing and file selection
# This section handles CLI arguments and determines which file to open or create.
# ----------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple line-based text editor")
    parser.add_argument("filename", nargs="?", help="file to open or create")
    return parser.parse_args()


# ----------------------
# File load/save utilities
# Functions to load a file into an in-memory list of lines and to save it back
# safely using a temporary file and atomic rename where possible.
# ----------------------


def load_file(path: str) -> List[str]:
    """Read the file at `path` and return a list of lines (without trailing newlines)."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def save_file(path: str, lines: List[str]) -> None:
    """Write `lines` to `path` safely by writing to a temporary file first."""
    dirpath = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp_path = tempfile.mkstemp(prefix=".simple-text-editor-", dir=dirpath)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:
            for line in lines:
                tmp.write(f"{line}\n")
        # Move temp file into place (atomic on most Unix filesystems)
        os.replace(tmp_path, path)
    finally:
        # If something went wrong and tmp file still exists, remove it
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


# ----------------------
# Interactive editor core
# Implements the REPL loop, command parsing and buffer manipulation.
# ----------------------


def print_help() -> None:
    """Show help text describing available commands."""
    help_text = """
Available commands (enter at an empty prompt):
  SAVE           Save changes to disk and exit
  QUIT           Exit without saving
  SHOW           Display current buffer with line numbers
  HELP           Show this help text
  INSERT N       Insert a line before line number N (1-based). You will be
                 prompted for the inserted text.
  DELETE N       Delete line number N
  REPLACE N      Replace line number N. You will be prompted for the new text.

Any other input will be appended to the end of the buffer as a new line.
"""
    print(help_text)


def show_buffer(lines: List[str]) -> None:
    """Display the buffer with 1-based line numbers."""
    if not lines:
        print("[buffer is empty]")
        return
    for i, line in enumerate(lines, start=1):
        print(f"{i:4d}: {line}")


def repl(filename: str, lines: List[str]) -> int:
    """Read-eval-print loop for user editing. Returns exit code (0 on save).

    The loop accepts simple commands or appends free text lines to the buffer.
    Typing SAVE saves and exits. QUIT exits without saving.
    """
    saved = False
    print(f"Editing file: {filename}")
    print("Type HELP for available commands. Type SAVE to save and exit.")
    while True:
        try:
            user = input("> ").rstrip("\n")
        except (EOFError, KeyboardInterrupt):
            # Treat Ctrl-D/Ctrl-C as quit without saving prompt
            print()
            confirm = input("Exit without saving? (y/N): ").strip().lower()
            if confirm == "y":
                return 0
            else:
                continue

        if not user:
            # empty input -> ignore
            continue

        cmd = user.strip()
        # Handle SAVE and QUIT which are full-line commands
        if cmd.upper() == "SAVE":
            try:
                save_file(filename, lines)
                print(f"Saved {len(lines)} lines to {filename}")
                saved = True
                return 0
            except Exception as e:
                print(f"Error saving file: {e}")
                continue

        if cmd.upper() == "QUIT":
            confirm = input("Exit without saving? (y/N): ").strip().lower()
            if confirm == "y":
                print("Exiting without saving.")
                return 0
            else:
                continue

        if cmd.upper() == "SHOW":
            show_buffer(lines)
            continue

        if cmd.upper() == "HELP":
            print_help()
            continue

        parts = cmd.split(maxsplit=1)
        op = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""

        if op == "INSERT":
            if not arg.isdigit():
                print("Usage: INSERT N  (N is a 1-based line number)")
                continue
            idx = int(arg) - 1
            if idx < 0 or idx > len(lines):
                print("Line number out of range")
                continue
            text = input("Insert text: ")
            lines.insert(idx, text)
            print(f"Inserted at line {idx+1}")
            continue

        if op == "DELETE":
            if not arg.isdigit():
                print("Usage: DELETE N")
                continue
            idx = int(arg) - 1
            if idx < 0 or idx >= len(lines):
                print("Line number out of range")
                continue
            removed = lines.pop(idx)
            print(f"Deleted line {idx+1}: {removed}")
            continue

        if op == "REPLACE":
            if not arg.isdigit():
                print("Usage: REPLACE N")
                continue
            idx = int(arg) - 1
            if idx < 0 or idx >= len(lines):
                print("Line number out of range")
                continue
            text = input("Replacement text: ")
            lines[idx] = text
            print(f"Replaced line {idx+1}")
            continue

        # If we reach here, treat input as a new line to append
        lines.append(user)


# ----------------------
# Main entrypoint
# Parse arguments, load the file into the buffer, run the editor loop.
# ----------------------


def main(argv: List[str] | None = None) -> int:
    args = parse_args() if argv is None else parse_args()
    filename = args.filename if args and args.filename else None
    if not filename:
        # Prompt for filename if not provided on command line
        filename = input("Filename to open/create: ").strip()
        if not filename:
            print("No filename provided. Exiting.")
            return 1

    # Ensure parent directories exist (do not create if path is directory)
    parent = os.path.dirname(os.path.abspath(filename))
    if parent and not os.path.isdir(parent):
        try:
            os.makedirs(parent, exist_ok=True)
        except OSError:
            pass

    # Load the file into memory
    buffer = load_file(filename)

    # Start REPL
    return repl(filename, buffer)


if __name__ == "__main__":
    raise SystemExit(main())
