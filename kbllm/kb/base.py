# standard libraries
from datetime import date
from typing import List, Literal, Optional

# third party libraries
from pydantic import BaseModel, Field


class Provider(BaseModel):
    """Represents a Healthcare Provider."""

    name: str
    id: str = Field(min_length=10, max_length=10)
    type: Literal["Doctor", "Nurse", "Physician Assistant"]
    specialty: str


class Test(BaseModel):
    """Represents a test."""

    name: str
    result: str


class Diagnosis(BaseModel):
    """Represents a diagnosis."""

    name: str
    ICD10: str  # International Classification of Diseases, 10th Revision


class Treatment(BaseModel):
    """Represents a treatment."""

    name: str
    RXCUI: str  # RxNorm Concept Unique Identifier
    dosage: str


class Patient(BaseModel):
    """Represents a patient."""

    name: str
    MRN: str  # Medical Record Number


class Encounter(BaseModel):
    """Represents an encounter."""

    date: date
    patient: Patient
    provider: Provider
    summary: str
    patient_diagnoses: Optional[List[Diagnosis]] = None
    patient_tests: Optional[List[Test]] = None
    treatment_plans: Optional[List[Treatment]] = None
