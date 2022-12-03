import argparse
import io
from pathlib import Path
import sys
from typing import List

from swrelogs.log_analyzer import log_analyzer
from swrelogs.metrics import BytesCounter, EventRate, IPCounter
from swrelogs.formatter import JSONFormatter


def resolve_sources(path: Path) -> List[Path]:
    # TODO: maybe restrict to interesting/supported files path.rglob("*.[log csv]")
    return list(path.iterdir()) if path.is_dir() else [path]


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

    parser.add_argument(
        "--output",
        type=str,
        help="Path to a file to save output in plain text JSON format.",
        default=None,
    )
    arguments = parser.parse_args()

    input_paths = resolve_sources(Path(arguments.input))

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
        for path in input_paths:
            log_analyzer(str(path), metrics)

        report = {}
        for metric in metrics:
            label = metric.label()
            report[label] = metric.report()

        formatter = JSONFormatter(report)
        if arguments.output:
            output_path = formatter.get_path(arguments.output)
            with open(output_path, "w", encoding="UTF8", newline="") as f:
            formatter.write(f)
