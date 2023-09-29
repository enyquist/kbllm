# standard libraries
from datetime import date
from typing import List

# third party libraries
from pydantic import BaseModel


class Test(BaseModel):
    """Represents a test."""

    name: str
    result: str


class Encounter(BaseModel):
    """Represents an encounter."""

    date: date
    diagnosis: str
    tests: List[Test]


class Patient(BaseModel):
    """Represents a patient."""

    name: str
    MRN: str  # Medical Record Number
    encounters: List[Encounter]
