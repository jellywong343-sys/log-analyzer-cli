# Log Analyzer CLI

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Analyze log levels, HTTP status codes, timestamps, and recurring message patterns from plain-text log files.

## Features

- Counts TRACE, DEBUG, INFO, WARN, ERROR, CRITICAL, and FATAL levels.
- Summarizes HTTP status codes found in log lines.
- Reports first and last ISO-like timestamps.
- Groups recurring messages after replacing timestamps and numbers.
- Exports detailed JSON and summary CSV reports.
- Reads files only; it never changes or deletes logs.

## Install

```bash
git clone https://github.com/jellywong343-sys/log-analyzer-cli.git
cd log-analyzer-cli
python -m pip install -e .
```

## Usage

```bash
log-analyze examples/application.log
log-analyze app.log server.log --top 20 --json report.json
log-analyze app.log --csv summary.csv
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT




