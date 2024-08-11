from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field 

class CPEParser(BaseModel):
    cpe: List[str] = Field(description="List of CPE strings in 2.3 format")
