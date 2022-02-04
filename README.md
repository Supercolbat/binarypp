**inspiration:** got bored of recreating the cpython vm, so im making my own *ʸᵃʸ*

well im using vm features to create a language

esolang, that is

hey at least you can say you code in binary now

assuming you have a binary editor

**features:**
- stack but also heap(?) based
- idk
- you can write to files i guess... i hope
- you got loops, conditionals, ..., wait how am i supposed to make it so you can open files
- idk how reading from stdin/file is gonna work
- oh right back to features
- ....
- you can do math


**concerns:**
- the claim of being a binary esolang falls apart when you use a hex edi- SHUT **SHUT**
- files are never closed after being opened

this is what it looks like after you convert everything into opcodes
```
PUSH_STACK 10 (00001010)
STORE_MEMORY 1 (00000001)
PUSH_STACK "file.txt"
STORE_MEMORY 2 (00000010)

MAKE_MARKER 1 (00000001)
READ_FROM 0 (00000000 - stdin)
WRITE_TO
GOTO_MARKER 1
PUSH_STACK "Hello, "
WRITE_TO 0 (00000000 - stdout)
WRITE_TO 0 (00000000 - stdout)

OPEN_FILE 2 ("file.txt" 00000010)
STORE_MEMORY 3 ()
READ_FROM 
```
```
00001000 00000000
00000010 01001000 01100101 01101100 01101100 01101111 00101100 00100000 00000000
00001001 00000000
00001001 00000000
```


```
POP_STACK    = 0b00000001
PUSH_STACK   = 0b00000100
PUSH_STRING_STACK = 0b00000101
PUSH_LONG_STACK   = 0b00000110
STORE_MEMORY = 0b00000011
READ_FROM    = 0b00001000
WRITE_TO     = 0b00001001
OPEN_FILE    = 0b00001100
MAKE_MARKER  = 0b00010000
GOTO_MARKER  = 0b00010001
BINARY_ADD          = 0b10000001
BINARY_SUBTRACT     = 0b10000010
BINARY_MULTIPLY     = 0b10000101
BINARY_POWER        = 0b10000110
BINARY_TRUE_DIVIDE  = 0b10001001
BINARY_FLOOR_DIVIDE = 0b10001010
BINARY_MODULO       = 0b10000100
BINARY_AND          = 0b11000001
BINARY_OR           = 0b11000010
BINARY_XOR          = 0b11000011
BINARY_NOT          = 0b11000100
```