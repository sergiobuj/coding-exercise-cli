import argparse

from swrelogs.log_analyzer import log_analyzer
from swrelogs.metrics import BytesCounter, EventRate, IPCounter

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

    parser.add_argument(
        "--mfip",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Most frequent IP",
        type=bool,
    )

    parser.add_argument(
        "--lfip",
        action=argparse.BooleanOptionalAction,
        type=bool,
        help="Least frequent IP",
        default=False,
    )

    parser.add_argument(
        "--eps",
        action=argparse.BooleanOptionalAction,
        type=bool,
        help="Events per second",
        default=False,
    )

    parser.add_argument(
        "--bytes",
        action=argparse.BooleanOptionalAction,
        type=bool,
        help="Total amount of bytes exchanged",
        default=False,
    )
    arguments = parser.parse_args()

    metrics = []
    if arguments.mfip:
        metrics.append(IPCounter())

    if arguments.lfip:
        metrics.append(IPCounter(least_frequent=True))

    if arguments.eps:
        metrics.append(EventRate())

    if arguments.bytes:
        metrics.append(BytesCounter())

    if metrics:
        log_analyzer(arguments.input, metrics)

        report = {}
        for metric in metrics:
            label = metric.label()
            report[label] = metric.report()
        print(report)
