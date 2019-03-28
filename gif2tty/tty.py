import sys


def write_lines(lines):
    sys.stdout.writelines(lines)
    sys.stdout.flush()


def move_up(n_lines):
    sys.stdout.write("\033[F" * n_lines)
    sys.stdout.flush()
