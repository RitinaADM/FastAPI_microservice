import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryId:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Category ID cannot be empty")

    @classmethod
    def new(cls):
        return cls(str(uuid.uuid4()))

    def __str__(self):
        return self.value