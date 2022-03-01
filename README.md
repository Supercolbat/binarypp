![Binary++ header image](https://user-images.githubusercontent.com/24477470/152656210-5d1d0168-7de3-480a-a981-b746820a55a5.png)

<p align="center">
  <a href="https://github.com/psf/black" target="_blank"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
  <img src="https://img.shields.io/badge/i%20need%20another-badge-651cdb.svg" alt="i need another badge">
</p>

Binary++ is a multi-paradigm, esoteric programming language that is based on binary.

Specifically, Binary++ is an interpreted esoteric, stack-based, imperative, dual-structured programming language.

To clarify on that last one, Binary++ supports both structured and unstructured programs.

**Disclaimer**: The instruction set may change as Binary++ is still in early development, meaning that code in one version may not work in another.

## Features
- Turing complete
  - I don't think this is actually a heap but I don't have a better term for it.
- Full STDIN/OUT access (mostly)
- A free, unlimited use "I code in Binary" pass

## Examples
To clarify, the examples shown here are in the binary representations of each character. The code itself usually contains unprintable characters which cannot be displayed. Think of it like a `hexdump` of the file but in binary.

### Hello, world!
Raw:
```
00000101 01001000 01100101 01101100 01101100 01101111 00101100 00100000 01110111 01101111 01110010 01101100 01100100 00100001 00001010 00000000
00001010 00000000
```
Mnemonics:
```
PUSH_STRING_STACK Hello, world
WRITE_TO 00000000 (stdout)
```

## Running
If you already have a compiled Binary++ program, you can run it with:
```sh
binarypp path/to/your/code.bin
```

If you wrote your code in plaintext ("Raw" in Examples), you can either compile it or interpret it.

To compile:
```sh
binarypp --compile path/to/your/plaintext.raw output.bin
binarypp output.bin
```

To interpet:
```sh
binarypp --interpret path/to/your/plaintext.raw
```

The file extensions `.raw` and `.bin` are not required and are only used to highlight the difference between plaintext and compiled.

## TODO
An up-to-date TODO list can be found in the [Projects](https://github.com/Supercolbat/binarypp/projects/1) tab.

**Language related**
- [x] Full STDIN/OUT support
- [x] Jumps (markers)
  - [x] MAKE_MARKER and GOTO_MARKER
  - [x] Initialize markers before execution
- [x] Conditionals
  - [x] Implement IF_NEXT_SKIP and SKIP_NEXT 
  - [x] IF_NEXT_SKIP and SKIP_NEXT should skip instructions and ignore arguments

**Tools**
- [ ] Proper CLI argument parsing
  - [x] Translate a "raw binary" file into characters
  - [ ] Verbosity for debugging
  - [ ] REPL mode?
- [ ] Port to C (or to Rust)
- [x] Syntax checker
  - Verify no arguments are missing
  - Missing terminator checker (PUSH_STRING_STACK)
- [ ] Compiler?
  - A compiler for binary sounds cool, but I have no knowledge in writing compilers

## Inspiration
While recreating the CPython VM, I came across the idea of not only just creating my own bytecode, but creating my own language. In VMs, bytecode is generally represented with either hexadecimal or decimal, but I chose the route of representing them in binary because...

**who doesnt want to code in binary?**
