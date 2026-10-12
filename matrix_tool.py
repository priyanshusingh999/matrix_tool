

import numpy as np

def format_number(x, decimals=4):
    """Format a number compactly: integers without decimals, floats trimmed."""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.{decimals}f}".rstrip("0").rstrip(".")


def render_matrix(m, title=None):
    """Return a bordered, column-aligned string representation of a matrix."""
    m = np.atleast_2d(m)
    rows, cols = m.shape
    cells = [[format_number(v) for v in row] for row in m]
    width = max(len(c) for row in cells for c in row)

    lines = []
    if title:
        lines.append(f"{title}  ({rows} x {cols})")
    horizontal = "+" + "-" * ((width + 2) * cols + (cols - 1)) + "+"
    lines.append(horizontal)
    for row in cells:
        lines.append("| " + "   ".join(c.rjust(width) for c in row) + " |")
    lines.append(horizontal)
    return "\n".join(lines)


def show(m, title=None):
    print()
    print(render_matrix(m, title))
    print()


# ----------------------------------------------------------------------
# Input handling
# ----------------------------------------------------------------------

def read_matrix(name):
    """
    Prompt the user for a matrix. Rows are entered one per line with
    space- or comma-separated numbers. A blank line finishes input.
    Returns a NumPy array, or None if the user cancels with 'q'.
    """
    print(f"\nEnter matrix {name}. One row per line, values separated by spaces or commas.")
    print("Press Enter on an empty line when done, or type 'q' to cancel.")
    rows = []
    while True:
        line = input(f"  row {len(rows) + 1}> ").strip()
        if line.lower() == "q":
            return None
        if line == "":
            if not rows:
                print("  Matrix is empty, enter at least one row.")
                continue
            break
        try:
            values = [float(tok) for tok in line.replace(",", " ").split()]
        except ValueError:
            print("  Invalid input: use numbers only. Try that row again.")
            continue
        if rows and len(values) != len(rows[0]):
            print(f"  Expected {len(rows[0])} values per row, got {len(values)}. Try that row again.")
            continue
        rows.append(values)
    return np.array(rows, dtype=float)


# ----------------------------------------------------------------------
# Operations (each returns a result or raises ValueError with a clear message)
# ----------------------------------------------------------------------

def add(a, b):
    if a.shape != b.shape:
        raise ValueError(f"Addition needs equal shapes, got {a.shape} and {b.shape}.")
    return a + b


def subtract(a, b):
    if a.shape != b.shape:
        raise ValueError(f"Subtraction needs equal shapes, got {a.shape} and {b.shape}.")
    return a - b


def multiply(a, b):
    if a.shape[1] != b.shape[0]:
        raise ValueError(
            f"Multiplication needs columns of A to equal rows of B, "
            f"got A{a.shape} and B{b.shape}."
        )
    return a @ b


def transpose(a):
    return a.T


def determinant(a):
    if a.shape[0] != a.shape[1]:
        raise ValueError(f"Determinant needs a square matrix, got {a.shape}.")
    d = float(np.linalg.det(a))
    # Clean up floating-point noise such as 1.9999999999999996 or -1e-16
    return 0.0 if abs(d) < 1e-10 else round(d, 10)


# ----------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------

MENU = """
==============================================
            MATRIX OPERATIONS TOOL
==============================================
  1. Enter / replace matrix A
  2. Enter / replace matrix B
  3. View stored matrices
  4. Add          (A + B)
  5. Subtract     (A - B)
  6. Multiply     (A x B)
  7. Transpose    (choose A or B)
  8. Determinant  (choose A or B)
  0. Exit
----------------------------------------------"""


def pick_matrix(store, prompt="Which matrix (A/B)? "):
    while True:
        choice = input(prompt).strip().upper()
        if choice in ("A", "B"):
            if store[choice] is None:
                print(f"  Matrix {choice} is empty. Enter it first.")
                return None
            return choice
        print("  Please type A or B.")


def offer_save(store, result):
    answer = input("Save this result as A, B, or skip (A/B/Enter)? ").strip().upper()
    if answer in ("A", "B"):
        store[answer] = result
        print(f"  Saved as matrix {answer}.")


def run():
    store = {"A": None, "B": None}

    while True:
        print(MENU)
        choice = input("Select an option: ").strip()

        try:
            if choice == "0":
                print("Goodbye!")
                break

            elif choice in ("1", "2"):
                name = "A" if choice == "1" else "B"
                m = read_matrix(name)
                if m is not None:
                    store[name] = m
                    show(m, f"Matrix {name}")

            elif choice == "3":
                if store["A"] is None and store["B"] is None:
                    print("\nNo matrices stored yet.")
                for name in ("A", "B"):
                    if store[name] is not None:
                        show(store[name], f"Matrix {name}")

            elif choice in ("4", "5", "6"):
                if store["A"] is None or store["B"] is None:
                    print("\nBoth matrices A and B must be entered first.")
                    continue
                op, symbol, label = {
                    "4": (add, "+", "Sum"),
                    "5": (subtract, "-", "Difference"),
                    "6": (multiply, "x", "Product"),
                }[choice]
                result = op(store["A"], store["B"])
                show(store["A"], "A")
                print(f"      {symbol}")
                show(store["B"], "B")
                show(result, f"{label}: A {symbol} B")
                offer_save(store, result)

            elif choice == "7":
                name = pick_matrix(store)
                if name:
                    result = transpose(store[name])
                    show(store[name], f"Original {name}")
                    show(result, f"Transpose of {name}")
                    offer_save(store, result)

            elif choice == "8":
                name = pick_matrix(store)
                if name:
                    d = determinant(store[name])
                    show(store[name], f"Matrix {name}")
                    print(f"  det({name}) = {format_number(d, 6)}\n")

            else:
                print("\nInvalid option. Choose a number from the menu.")

        except ValueError as err:
            print(f"\n  Error: {err}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    run()