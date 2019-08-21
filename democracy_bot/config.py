"""Config module"""

import os
import dataclasses
from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class Config:
    """Application config"""

    bot_token: str

    @classmethod
    def from_environ(cls) -> "Config":
        """Constructs configuration from environment variables"""

        missing_variables = [
            f.name.upper()
            for f in fields(cls)
            if f.default == dataclasses.MISSING and get_environ(f.name) is None
        ]

        if missing_variables:
            raise Exception(f"Missing environment variables: {missing_variables}")

        return cls(**{f.name: f.type(get_environ(f.name)) for f in fields(cls)})


def get_environ(variable_name: str) -> Optional[str]:
    """Returns environment variable if available.

    Variable name is converted to uppercase if it's not already
    """

    return os.environ.get(variable_name.upper())
