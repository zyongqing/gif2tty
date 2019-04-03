from .gif import gif_tty


def main():
    import argparse

    parser = argparse.ArgumentParser(description="show gif in console mode")
    parser.add_argument("file", help="gif file name")
    parser.add_argument("--width", help="output width", type=int, default=60)
    parser.add_argument("--height", help="output height", type=int, default=30)
    parser.add_argument("--sleep", help="sleep time", type=float, default=0.02)
    parser.add_argument("--fill", help="fill empty", action="store_true")
    parser.add_argument("--color", help="show color", action="store_true")
    args = parser.parse_args()
    gif_tty(
        args.file,
        args.width,
        args.height,
        sleep=args.sleep,
        fill=args.fill,
        color=args.color,
    )


if __name__ == "__main__":
    main()
