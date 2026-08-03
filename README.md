A basic compiler written in python.

Made as a learning exercise following this [blog](https://austinhenley.com/blog/teenytinycompiler1.html) by Austin Henley.


# Installation

Clone the repo:
```
git clone https://github.com/dhityl/tiny-compiler.git
```

# Compilation

Run the python file to get an C code in `out.c`
```
python tiny.py <path_to_file>
```

Use a c compiler like gcc to compiler the C code
```
gcc out.c -o a.out
```

On linux, run the output executable with
```
./a.out
```


Using example `average.tiny` from `examples/`

```
python tiny.py examples/average.tiny
```

```
```
```
