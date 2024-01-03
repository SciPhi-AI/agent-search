from typing import Any, Optional

from pydantic import BaseModel


class AgentSearchResult(BaseModel):
    """A dataclass to store the search result"""

    score: float
    url: str
    title: Optional[str]
    dataset: Optional[str]
    # TODO - Add dict(str, [str, float, ..]) validation
    metadata: Any
    text: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.title and self.title == self.text[0 : len(self.title)]:
            self.text = self.text[len(self.title) :]
        self.text = self.text.strip()

    def to_string_dict(self) -> dict:
        """Returns a dictionary representation with all values as strings."""
        return {
            "score": str(self.score),
            "url": self.url,
            "title": self.title,
            "dataset": self.dataset,
            "metadata": self.metadata,
            "text": self.text,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
