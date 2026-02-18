import math
import shutil



def print_adaptive_grid(items, padding=4, min_col_width=18):
    term_width = shutil.get_terminal_size().columns

    longest = max(len(i) for i in items) if items else 0
    col_width = max(min_col_width, longest + 2)

    cols = max(1, term_width // (col_width + padding))
    rows = math.ceil(len(items) / cols)

    for r in range(rows):
        line = ""
        for c in range(cols):
            idx = r + c * rows
            if idx < len(items):
                line += items[idx].ljust(col_width) + " " * padding
        print(line.rstrip())
