
from typing import Any, Protocol

from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)


class ExportPlugin(Protocol):
    def process_output(
        self,
        data: list[tuple[int, str]],
    ) -> None:
        ...


class CSVExportPlugin:
    def process_output(
        self,
        data: list[tuple[int, str]],
    ) -> None:
        values = [value for _, value in data]
        csv_line = ",".join(
            self._escape_csv(value) for value in values
        )
        print("CSV Output:")
        print(csv_line)

    @staticmethod
    def _escape_csv(value: str) -> str:
        if any(char in value for char in (",", '"', "\n")):
            return '"' + value.replace('"', '""') + '"'
        return value


class JSONExportPlugin:
    def process_output(
        self,
        data: list[tuple[int, str]],
    ) -> None:
        items = [
            f'"item_{rank}": "{self._escape_json(value)}"'
            for rank, value in data
        ]
        print("JSON Output:")
        print("{" + ", ".join(items) + "}")

    @staticmethod
    def _escape_json(value: str) -> str:
        return (
            value.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            handled = False

            for proc in self._processors:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break

            if not handled:
                print(
                    "DataStream error - Can't process "
                    f"element in stream: {item}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for proc in self._processors:
            name = proc.__class__.__name__.replace(
                "Processor", " Processor"
            )
            total = proc._next_rank
            remaining = len(proc._queue)

            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )

    def output_pipeline(
        self,
        nb: int,
        plugin: ExportPlugin,
    ) -> None:
        for proc in self._processors:
            data: list[tuple[int, str]] = []

            for _ in range(nb):
                try:
                    data.append(proc.output())
                except IndexError:
                    break

            plugin.process_output(data)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")

    stream = DataStream()
    stream.print_processors_stats()

    numeric = NumericProcessor()
    text = TextProcessor()
    logs = LogProcessor()

    print("\nRegistering all data processors")
    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(logs)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    print("\nSend first batch of data on stream:", batch)
    stream.process_stream(batch)
    stream.print_processors_stats()

    csv_plugin = CSVExportPlugin()
    print("\nExporting 3 elements with CSV plugin")
    stream.output_pipeline(3, csv_plugin)
    stream.print_processors_stats()

    second_batch: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]

    print("\nSend second batch of data on stream:", second_batch)
    stream.process_stream(second_batch)
    stream.print_processors_stats()

    json_plugin = JSONExportPlugin()
    print("\nExporting 5 elements with JSON plugin")
    stream.output_pipeline(5, json_plugin)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
