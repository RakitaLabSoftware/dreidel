from pydantic import BaseModel


class Config(BaseModel):
    @classmethod
    def from_json(cls, path: str) -> "Config":
        return Config()
