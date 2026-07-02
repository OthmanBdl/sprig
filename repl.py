from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Environment


def main():
    print("Mini-language REPL. Type 'exit' to quit.")

    # A single shared environment persists across all lines of the session,
    # so variables and functions defined earlier stay available.
    env = Environment()

    while True:
        try:
            line = input("calc> ")
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D / Ctrl+C: exit cleanly instead of crashing.
            print("\nGoodbye!")
            break

        line = line.strip()
        if line == "":
            continue
        if line == "exit":
            print("Goodbye!")
            break

        # Run the full pipeline; a try/except keeps one bad line from
        # crashing the whole session.
        try:
            tokens = Lexer(line).tokenize()
            tree = Parser(tokens).parse()
            result = Interpreter(tree, env).interpret()
            if result is not None:
                print(result)
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()