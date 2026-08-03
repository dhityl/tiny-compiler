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

```bash
$ python tiny.py examples/average.tiny
tiny compiler
Compilation completed.
$ gcc out.c
$ ./a.out
Enter number of scores: 
4
Enter one value at a time: 
6
7
6
7
Average: 
6.50

```
