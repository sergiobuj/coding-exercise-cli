import argparse
import io
import sys
from pathlib import Path
from typing import List

from swrelogs.formatter import CSVFormatter, JSONFormatter
from swrelogs.log_analyzer import run_log_analyzer
from swrelogs.metrics import BytesCounter, EventRate, IPCounter


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
        help="Path to one plain-text file, or a directory. If the path is to a directory, take all files as input.",
        type=str,
    )

    metrics_group = parser.add_argument_group("metrics")
    metrics_group.add_argument(
        "--mfip",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Most frequent IP",
        type=bool,
    )

    metrics_group.add_argument(
        "--lfip",
        action=argparse.BooleanOptionalAction,
        type=bool,
        help="Least frequent IP",
        default=False,
    )

    metrics_group.add_argument(
        "--eps",
        action=argparse.BooleanOptionalAction,
        type=bool,
        help="Events per second",
        default=False,
    )

    metrics_group.add_argument(
        "--bytes",
        action=argparse.BooleanOptionalAction,
        type=bool,
        help="Total amount of bytes exchanged",
        default=False,
    )

    output_group = parser.add_argument_group("output")
    output_group.add_argument(
        "--output",
        type=str,
        help="Path to a file to save output (JSON by default)",
        default=None,
    )

    parser.add_argument(
        "--output-fmt",
        type=str,
        choices=["json", "csv"],
        help="File format to save output.",
        default="json",
    )
    arguments = parser.parse_args()

    input_paths = resolve_sources(Path(arguments.input))

    formatter_class = JSONFormatter
    if arguments.output_fmt == "csv":
        formatter_class = CSVFormatter

    metrics = []
    if arguments.mfip:
        metrics.append(IPCounter())

    if arguments.lfip:
        metrics.append(IPCounter(least_frequent=True))

    if arguments.eps:
        metrics.append(EventRate())

    if arguments.bytes:
        metrics.append(BytesCounter())

    if not metrics:
        parser.print_help(sys.stderr)
        parser.error("select at least one metric to gather")

    for path in input_paths:
        run_log_analyzer(str(path), metrics)

    report = {}
    for metric in metrics:
        label = metric.label()
        report[label] = metric.report()

    formatter = formatter_class(report)
    if arguments.output:
        output_path = Path(arguments.output).with_suffix(
            f".{formatter.file_extension()}"
        )
        with open(output_path, "w", encoding="UTF8", newline="") as f:
            formatter.write(f)

    else:
        with io.StringIO() as dest:
            formatter.write(dest)
            print(dest.getvalue(), file=sys.stdout)
