"""Bridge CLI prompts in career_mode to HTTP-driven UI inputs."""

from __future__ import annotations


class NeedInput(Exception):
    """Raised when the game needs a user choice before continuing."""

    def __init__(self, prompt: dict):
        self.prompt = prompt
        super().__init__(prompt.get("type", "input"))


class WebIO:
    def __init__(self) -> None:
        self.response_queue: list = []
        self.pending: dict | None = None
        self.logs: list[str] = []

    def clear_pending(self) -> None:
        self.pending = None

    def push_responses(self, values: list) -> None:
        self.response_queue.extend(values)

    def _log(self, message: str) -> None:
        if message:
            self.logs.append(str(message))

    def _take(self, default=None):
        if self.response_queue:
            return self.response_queue.pop(0)
        raise NeedInput(self.pending or {"type": "text", "message": "Input required"})

    def prompt_text(self, prompt: str, default=None):
        if not self.response_queue:
            self.pending = {
                "type": "text",
                "label": prompt.strip(),
                "default": default,
            }
            raise NeedInput(self.pending)
        value = self._take(default)
        text = str(value).strip() if value is not None else ""
        return text or default

    def prompt_int(self, prompt: str, minimum=None, maximum=None):
        if not self.response_queue:
            self.pending = {
                "type": "number",
                "label": prompt.strip(),
                "minimum": minimum,
                "maximum": maximum,
            }
            raise NeedInput(self.pending)
        raw = self._take(minimum if minimum is not None else 0)
        try:
            value = int(raw)
        except (TypeError, ValueError):
            value = int(minimum or 0)
        if minimum is not None:
            value = max(minimum, value)
        if maximum is not None:
            value = min(maximum, value)
        return value

    def input(self, prompt: str = ""):
        if prompt:
            self._log(prompt.rstrip())
        if not self.response_queue:
            self.pending = {"type": "confirm", "label": prompt.strip() or "Press continue"}
            raise NeedInput(self.pending)
        return str(self._take(""))

    def choose_from_list(self, title: str, options: list, allow_cancel: bool = False):
        if not self.response_queue:
            self.pending = {
                "type": "menu",
                "title": title,
                "options": list(options),
                "allow_cancel": allow_cancel,
            }
            raise NeedInput(self.pending)
        raw = self._take(None)
        if raw is None:
            return None
        if isinstance(raw, str) and raw.isdigit():
            choice = int(raw)
        else:
            choice = int(raw)
        if allow_cancel and choice == 0:
            return None
        # Accept 1-based menu pick from UI.
        if 1 <= choice <= len(options):
            return choice - 1
        return max(0, min(len(options) - 1, choice))
