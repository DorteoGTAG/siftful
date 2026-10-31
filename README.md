# SIFTFUL

SIFTFUL is a beginner-friendly, general-purpose programming language with a strong focus on game development and an extensible interpreter architecture.

This repository contains the first working prototype of SIFTFUL version 0.1:

- a real lexer/tokenizer
- a parser
- an interpreter runtime
- standard library helpers
- a command-line runner
- a minimal SIFTFUL Studio prototype built with Tkinter
- sample .sft programs

## Current status

Version 0.1 supports:
- print.inst()
- new.varible()
- variables
- numeric arithmetic
- assignment and compound assignment
- if/else blocks
- basic game state helpers like game.title(), game.player(), game.score, game.win(), game.lose()

## Files

- `siftful/lexer.py` - tokenization for SIFTFUL statements and expressions
- `siftful/parser.py` - statement parsing and block handling
- `siftful/interpreter.py` - interpreter runtime
- `siftful/runtime.py` - variable and game state management
- `siftful/cli.py` - command-line runner for .sft files
- `siftful/studio.py` - minimal editor / IDE prototype
- `examples/hello.sft` - demonstration script
- `examples/game_demo.sft` - simple game state example

## Run a script

From the project root:

```bash
python -m siftful examples/hello.sft
```

## Launch the Studio prototype

```bash
python -m siftful.studio
```

## Windows notes

This prototype uses Python 3 and Tkinter, which is included with standard Python installs on Windows. The project is designed to be easy to run on Windows without external dependencies.

## Example program

```siftful
new.varible("score")
score = 100
score += 10
print.inst("Score is:")
print.inst(score)

if.inst(score > 50) {
    print.inst("You win!")
} else.inst() {
    print.inst("Try again")
}
```

## Long-term roadmap

This is intentionally structured so it can evolve into later SIFTFUL versions.

- v0.1: interpreter, variables, arithmetic, printing, basic conditions
- v0.2: loops, functions, input
- v0.3: arrays, classes, modules
- v0.4: Studio editor, file management, syntax highlighting, error reporting
- v0.5: engine libraries, graphics, input
- v1.0: stable release

## License

MIT
