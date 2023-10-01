# standard libraries
import json
from pathlib import Path
from typing import List

# third party libraries
from mgclient import Cursor

# kbllm libraries
from kbllm.kb.base import Encounter
from kbllm.kb.context import MemgraphConnection

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"


@MemgraphConnection
def clear_database(cursor: Cursor):
    """Clear all data from Memgraph database."""

    # Delete all nodes and relationships
    cursor.execute("MATCH (n) DETACH DELETE n")


@MemgraphConnection
def insert_into_memgraph(cursor: Cursor, encounters: List[Encounter]) -> None:
    """
    Insert encounters, patients, providers, diagnoses, tests, and treatments into Memgraph.

    Args:
        encounters (List[Encounter]): List of encounters to insert into Memgraph.
    """

    for encounter in encounters:
        # Insert the patient if not exists
        cursor.execute(
            f"""
            MERGE (p:Patient {{name: '{encounter.patient.name}', MRN: '{encounter.patient.MRN}'}})
            RETURN id(p) AS patient_id
        """
        )
        patient_id = cursor.fetchone()[0]

        # Insert the provider if not exists
        cursor.execute(
            f"""
            MERGE (pr:Provider {{id: '{encounter.provider.id}'}})
            ON CREATE SET pr.name = '{encounter.provider.name}', pr.type = '{encounter.provider.type}',
            pr.specialty = '{encounter.provider.specialty}'
            RETURN id(pr) AS provider_id
        """
        )
        provider_id = cursor.fetchone()[0]

        # Insert the encounter and link it to the patient and provider
        cursor.execute(
            f"""
            MATCH (p:Patient) WHERE id(p) = {patient_id}
            MATCH (pr:Provider) WHERE id(pr) = {provider_id}
            CREATE (e:Encounter {{date: '{encounter.date}', summary: '{encounter.summary}'}})
            CREATE (p)-[:HAD_ENCOUNTER]->(e)
            CREATE (pr)-[:PROVIDED_ENCOUNTER]->(e)
            RETURN id(e) AS encounter_id
        """
        )
        encounter_id = cursor.fetchone()[0]

        for diagnosis in encounter.patient_diagnoses:
            # Insert each diagnosis and link it to the encounter
            cursor.execute(
                f"""
                MATCH (e:Encounter) WHERE id(e) = {encounter_id}
                MERGE (d:Diagnosis {{ICD10: '{diagnosis.ICD10}'}})
                ON CREATE SET d.name = '{diagnosis.name}'
                CREATE (e)-[:HAS_DIAGNOSIS]->(d)
            """
            )

        for test in encounter.patient_tests:
            # Insert each test and link it to the encounter
            cursor.execute(
                f"""
                MATCH (e:Encounter) WHERE id(e) = {encounter_id}
                CREATE (t:Test {{name: '{test.name}', result: '{test.result}'}})
                CREATE (e)-[:HAD_TEST]->(t)
            """
            )

        for treatment in encounter.treatment_plans:
            # Insert each treatment and link it to the encounter
            cursor.execute(
                f"""
                MATCH (e:Encounter) WHERE id(e) = {encounter_id}
                MERGE (tr:Treatment {{RXCUI: '{treatment.RXCUI}'}})
                ON CREATE SET tr.name = '{treatment.name}', tr.dosage = '{treatment.dosage}'
                CREATE (e)-[:PRESCRIBED_TREATMENT]->(tr)
            """
            )


def main():
    """Main function."""

    # Clear database
    clear_database()  # TODO: Remove this line in production

    # Load data
    with open(DATA_DIR / "data.json", "r") as f:
        data = json.load(f)

    # Parse data
    encounters = []
    for encounter_data in data["encounters"]:
        encounter = Encounter(
            date=encounter_data["date"],
            patient=encounter_data["patient"],
            provider=encounter_data["provider"],
            summary=encounter_data["summary"],
            patient_diagnoses=encounter_data["patient_diagnoses"],
            patient_tests=encounter_data["patient_tests"],
            treatment_plans=encounter_data["treatment_plans"],
        )
        encounters.append(encounter)

    # Insert into Memgraph
    insert_into_memgraph(encounters)
    print("Done!")


if __name__ == "__main__":
    main()
