from typing import Any, Optional

from pydantic import BaseModel


class SERPResult(BaseModel):
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
