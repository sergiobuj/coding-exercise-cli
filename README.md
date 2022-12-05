# Log Analyzer

## Description

Command line tool (CLI) to analyze `access.log` files.

The tool reads a file or group of files and produces a summary for the provided arguments.

## Usage

```
usage: cli.py [-h] [--mfip | --no-mfip] [--lfip | --no-lfip] [--eps | --no-eps] [--bytes | --no-bytes] [--output OUTPUT] input

positional arguments:
  input                Path to one plain-text file, or a directory. If the path is to a directory, take all files as input.

options:
  -h, --help           show this help message and exit

metrics:
  --mfip, --no-mfip    Most frequent IP (default: False)
  --lfip, --no-lfip    Least frequent IP (default: False)
  --eps, --no-eps      Events per second (default: False)
  --bytes, --no-bytes  Total amount of bytes exchanged (default: False)

output:
  --output OUTPUT      Path to a file to save the output in plain text JSON format. (default: None)
```

## Supported formats
 - Squid's native log format. [See reference](https://wiki.squid-cache.org/Features/LogFormat).

## Metrics
### IP summary
Set the `--mfip` parameter to find the most frequent IP in the logs.

Set the `--lfip` parameter to find the least frequent IP in the logs.

### Event Rate

Set the `--eps` parameter to compute the events per second rate from the logs.

The event rate metric is computed as the average of the log events over the total number of seconds between the first and last log timestamp.

### Bytes count

Set the `--bytes` parameter to sum the number of bytes transferred based on the logs.

## Output

Set the `--output` parameter to save the summary to a file.

The file will contain a JSON object with the metrics collected.

If not output path is provided the summary is sent to the standard output.

## Usage

### Python

Install the tool dependencies.
```sh
pip install -r requirements.txt
```

Run the CLI tool for a single file:

```sh
python cli.py sample_data/access.log --lfip --mfip --eps --bytes

{"mfip": "127.0.0.1", "lfip": "210.10.215.171", "eps": 0.00546, "bytes": 2216979451}
```

Or a directory with multiple log files:
```sh
python cli.py sample_data/multiple_files --lfip --mfip --eps --bytes

{"mfip": "127.0.0.1", "lfip": "210.10.215.171", "eps": 0.00546, "bytes": 2216979451}
```

### Docker

Build the Docker container.

```sh
docker build --tag cli .
```

To run with the docker container, provide:
 - `--mount` point to access files in the host.

```sh
docker run --mount type=bind,source="$(pwd)",target=/home/swrelogs cli access.log --eps --output summary.json
```

## Development

### Tests

Run tests with make

```sh
make test
```
