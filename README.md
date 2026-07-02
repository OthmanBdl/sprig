# Sprig

**A small programming language and interpreter, built from scratch in Python.**

Sprig is a tree-walking interpreter for a little language of my own design. It has variables, arithmetic with proper operator precedence, booleans and logical operators, `if`/`else`, `while` and `for` loops, and functions with parameters, local scope, and `return`. It's small enough to read in an afternoon, but complete enough to be **Turing-complete** — it can express any computation.

I built it end to end to understand how programming languages actually work: how source text becomes tokens, how tokens become a syntax tree, and how that tree is executed.

```
fun fact(n) {
    r = 1
    for (i = 1; i <= n; i = i + 1) {
        r = r * i
    }
    return r
}

print("5! =", fact(5))   // 5! = 120
```

---

## How it works

Sprig follows the classic interpreter pipeline. Source code flows through three stages before it runs:

```
source text  →  Lexer  →  tokens  →  Parser  →  AST  →  Interpreter  →  result
```

- **Lexer** (`lexer.py`) scans the raw text character by character and groups it into *tokens* (numbers, operators, keywords, identifiers).
- **Parser** (`parser.py`) turns the flat token list into an *abstract syntax tree* (AST) using recursive descent, so operator precedence is captured by the shape of the tree.
- **Interpreter** (`interpreter.py`) walks the tree and evaluates it, managing variables and function scopes along the way.

The AST node types live in `ast_nodes.py`, and `repl.py` wires everything together into an interactive prompt.

---

## Running Sprig

Sprig needs only Python 3 — no external dependencies.

Start the interactive REPL:

```bash
python repl.py
```

Then type code at the prompt:

```
sprig> x = 10
10
sprig> x * x
100
sprig> print("hello", "world")
hello world
```

Type `exit` (or press Ctrl+D) to quit.

---

## Language tour

### Values

Sprig has three kinds of values: numbers, strings, and booleans.

```
42
"hello, world"
true
```

### Variables

```
name = "Sprig"
count = 3
```

### Arithmetic and comparison

Operator precedence works as you'd expect — multiplication before addition, and so on.

```
2 + 3 * 4        // 14
(2 + 3) * 4      // 20
10 > 3           // true
5 == 5           // true
```

### Logical operators

`and`, `or`, and `not`, with short-circuit evaluation.

```
x > 0 and x < 10
a == 1 or a == 2
not (done)
```

### Conditionals

```
if (score >= 60) {
    print("pass")
} else {
    print("fail")
}
```

### Loops

Both `while` and `for` are available.

```
i = 0
while (i < 3) {
    print(i)
    i = i + 1
}

for (i = 0; i < 3; i = i + 1) {
    print(i)
}
```

### Functions

Functions take parameters, have their own local scope, and can `return` a value.

```
fun add(a, b) {
    return a + b
}

print(add(2, 3))   // 5
```

### Printing

`print` is a built-in that displays its arguments, separated by spaces.

```
print("the answer is", 42)   // the answer is 42
```

---

## Project structure

```
sprig/
├── lexer.py         # source text  -> tokens
├── parser.py        # tokens       -> AST
├── ast_nodes.py     # the AST node definitions
├── interpreter.py   # AST          -> result (tree-walking evaluator)
├── repl.py          # interactive prompt
├── examples/        # sample programs written in Sprig
└── tests/           # automated tests
```

---

## Language reference

| Category   | Supported                                             |
|------------|-------------------------------------------------------|
| Types      | numbers, strings, booleans                            |
| Arithmetic | `+`  `-`  `*`  `/`                                     |
| Comparison | `<`  `>`  `<=`  `>=`  `==`  `!=`                       |
| Logic      | `and`  `or`  `not` (short-circuit)                     |
| Control    | `if` / `else`, `while`, `for`                         |
| Functions  | definition, parameters, local scope, `return`         |
| Built-ins  | `print`                                               |

---

## Design notes and limitations

Sprig is a **tree-walking interpreter**: it executes the AST directly. This is the same architecture as `jlox` from Robert Nystrom's *Crafting Interpreters*, and it's the simplest way to get a working language. Production languages like CPython go one step further and compile the AST to bytecode that a virtual machine executes, which is faster — a natural next step for a version 2.

Current limitations, kept deliberately to keep the codebase small and readable: no data structures (lists, dictionaries) yet, integer/float division follows Python's rules, and errors don't yet report line numbers. These are good candidates for future work.

---

## Possible next steps

- Line numbers in error messages
- Running `.sprig` files directly (not just the REPL)
- More built-ins (`len`, `input`, math helpers)
- Data structures: lists and dictionaries
- A bytecode compiler and virtual machine (the `clox` approach)

---

## Author

Built by **Othman Boudeliou** as a from-scratch exploration of interpreter design.

GitHub: [OthmanBdl](https://github.com/OthmanBdl?tab=repositories)
