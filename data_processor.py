
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._queue: list[tuple[int, str]] = []
        self._next_rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._queue:
            raise IndexError("No data available")

        return self._queue.pop(0)

    def _store(self, value: str) -> None:
        self._queue.append((self._next_rank, value))
        self._next_rank += 1


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, bool):
            return False

        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(
                isinstance(item, (int, float))
                and not isinstance(item, bool)
                for item in data
            )

        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Invalid numeric data")

        if isinstance(data, list):
            for item in data:
                self._store(str(item))
        else:
            self._store(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Invalid text data")

        if isinstance(data, list):
            for item in data:
                self._store(item)
        else:
            self._store(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            )

        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )

        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Invalid log data")

        if isinstance(data, list):
            for item in data:
                level = item.get("log_level", "").strip()
                message = item.get("log_message", "").strip()
                self._store(f"{level}: {message}")
        else:
            level = data.get("log_level", "").strip()
            message = data.get("log_message", "").strip()
            self._store(f"{level}: {message}")


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    # Create processors
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    # Test NumericProcessor
    print("\nTesting Numeric Processor...")

    print("Valid 42:", numeric.validate(42))
    print("Invalid Hello:", numeric.validate("Hello"))

    print("Testing invalid ingestion:")
    try:
        numeric.ingest("foo")  # type: ignore[arg-type]
    except ValueError as error:
        print("Got exception:", error)

    numeric.ingest([1, 2, 3, 4, 5])

    print("Extracting numeric values:")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    # Test TextProcessor
    print("\nTesting Text Processor...")

    print("Valid Hello:", text.validate("Hello"))
    print("Invalid 42:", text.validate(42))

    if text.validate(["Hello", "Nexus", "World"]):
        text.ingest(["Hello", "Nexus", "World"])

    print("Extracting text values:")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    # Test LogProcessor
    print("\nTesting Log Processor...")

    valid_log = {
        "log_level": "NOTICE",
        "log_message": "Connection to server"
    }

    invalid_log = {
        "log_level": "ERROR",
        "log_message": 123
    }

    print("Valid log:", log.validate(valid_log))
    print("Invalid log:", log.validate(invalid_log))

    if log.validate([
        valid_log,
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access"
        }
    ]):
        log.ingest([
            valid_log,
            {
                "log_level": "ERROR",
                "log_message": "Unauthorized access"
            }
        ])

    print("Extracting log values:")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
