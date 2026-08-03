A basic compiler written in python.

Made as a learning exercise following this [blog](https://austinhenley.com/blog/teenytinycompiler1.html) by Austin Henley.


# Installation

Clone the repo:
```
git clone https://github.com/dhityl/tiny-compiler.git
```


# Compilation
## Bash Script

Build executable using the bash script
```bash
./build.sh <path_to_file>
```

Run executable
```
./name_of_file
```


Using `aveerage.tiny` from `examples/`

```bash
./build.sh examples/average.tiny
```

```bash
./average
```


## Manual

Run the python file to get C code in `out.c`
```
python tiny.py <path_to_file>
```

Use a C compiler to compile then run the C code

### Using gcc
Compile `out.c`
```
gcc out.c
```

Run the output executable
```
./a.out
```


Using `average.tiny` from `examples/`

```bash
$ python tiny.py examples/average.tiny
```

```bash
$ gcc out.c
```

```bash
$ ./a.out
```

# Syntax

Class/Enum `TokenType` in `lex.py` has all the keywords and symbols that are supported by the compiler. The syntax is similar to C, but with some differences. `grammar.txt` contains the grammar of the language, used by the parser to parse the code.

From those two files, you can see the syntax of the language.

