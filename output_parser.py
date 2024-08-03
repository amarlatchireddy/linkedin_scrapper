from typing import List, Dict, Any
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel,Field

class Summary(BaseModel):

    summary: str = Field(description="Summary text")
    fact: List[str] = Field(description="Fact text")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "fact": self.fact}

summary_parser = PydanticOutputParser(pydantic_object=Summary)