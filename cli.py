import argparse

from swrelogs.log_analyzer import log_analyzer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "input",
        default="",
        help="Path to one plain-text file, or a directory. If directory, take all files as input.",
        type=str,
    )
    arguments = parser.parse_args()

    report = log_analyzer(arguments.input)
    print(report)
