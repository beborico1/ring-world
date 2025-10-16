from datetime import datetime


class NetworkLogger:
    @staticmethod
    def log(message: str) -> None:
        """Log messages with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
