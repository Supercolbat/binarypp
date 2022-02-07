![Binary++ header image](https://user-images.githubusercontent.com/24477470/152656210-5d1d0168-7de3-480a-a981-b746820a55a5.png)

<p align="center">
  <a href="https://github.com/psf/black" target="_blank"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
  <img src="https://img.shields.io/badge/i%20need%20another-badge-651cdb.svg" alt="i need another badge">
</p>

Binary++ is an esoteric programming language based on* binary.

\* It's meant to be based on binary, but you can write Binary++ code using different means.

## Features
- Stack and heap(?) based.
  - I don't think this is actually a heap but I don't have a better term for it.
- Full STDIN/OUT access
- A free, unlimited use "I code in Binary" pass

## Examples
To clarify, the examples shown here are in the binary representations of each character. The code itself usually contains unprintable characters which cannot be displayed. Think of it like a `hexdump` of the file but in binary.

### Hello, world!
Raw:
```
00000101 01001000 01100101 01101100 01101100 01101111 00101100 00100000 01110111 01101111 01110010 01101100 01100100 00100001 00001010 00000000
00001001 00000000
```
Translated:
```
PUSH_STRING_STACK Hello, world
WRITE_TO 00000000 (stdout)
```

## TODO
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
