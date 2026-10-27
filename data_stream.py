
from typing import Any

from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
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


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")

    stream = DataStream()
    stream.print_processors_stats()

    numeric = NumericProcessor()
    text = TextProcessor()
    logs = LogProcessor()

    print("\nRegistering Numeric Processor")
    stream.register_processor(numeric)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access!",
            },
            {
                "log_level": "INFO",
                "log_message": "User connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    print("\nSend first batch of data on stream")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    stream.register_processor(text)
    stream.register_processor(logs)

    print("\nSend the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nConsume some processed data")

    for _ in range(3):
        print("Numeric:", numeric.output())

    for _ in range(2):
        print("Text:", text.output())

    print("Log:", logs.output())

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
