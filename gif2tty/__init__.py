from .gif import extract_frames, tty_frame, tty_gif


def main():
    import argparse

    parser = argparse.ArgumentParser(description="show gif in console mode")
    parser.add_argument("file", help="gif file name")
    parser.add_argument("--width", help="width", type=int, default=60)
    parser.add_argument("--height", help="height", type=int, default=30)
    parser.add_argument("--sleep", help="sleep time", type=float, default=0.02)
    parser.add_argument("--fill", help="fill empty", action="store_true")
    args = parser.parse_args()
    try:
        tty_gif(
            args.file,
            width=args.width,
            height=args.height,
            sleep=args.sleep,
            fill_empty=args.fill,
        )
    except Exception as e:
        print(e)


__all__ = [extract_frames, tty_frame, tty_gif, main]
