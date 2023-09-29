# standard libraries
import json
from pathlib import Path
from typing import List

# third party libraries
import mgclient

# kbllm libraries
from kbllm.base import Patient

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"


def insert_into_memgraph(patients: List[Patient]):
    """Insert patient and encounters into Memgraph."""
    # Create a connection object
    connection = mgclient.connect(host="127.0.0.1", port=7687)
    cursor = connection.cursor()

    for patient in patients:
        # Insert the patient
        cursor.execute(
            f"""
            CREATE (p:Patient {{name: '{patient.name}', MRN: '{patient.MRN}'}})
            RETURN id(p) AS patient_id
            """
        )
        patient_id = cursor.fetchone()[0]

        for encounter in patient.encounters:
            # Insert the encounter and link it to the patient
            cursor.execute(
                f"""
                MATCH (p:Patient) WHERE id(p) = {patient_id}
                CREATE (e:Encounter {{date: '{encounter.date}', diagnosis: '{encounter.diagnosis}'}})
                CREATE (p)-[:HAD_ENCOUNTER]->(e)
                RETURN id(e) AS encounter_id
                """
            )

            encounter_id = cursor.fetchone()[0]

            for test in encounter.tests:
                # Insert each test and link it to the encounter
                cursor.execute(
                    f"""
                    MATCH (e:Encounter) WHERE id(e) = {encounter_id}
                    CREATE (t:Test {{name: '{test.name}', result: '{test.result}'}})
                    CREATE (e)-[:HAD_TEST]->(t)
                    """
                )

    # Commit the transaction
    connection.commit()
    connection.close()


def main():
    """Main function."""

    # Load data
    with open(DATA_DIR / "data.json", "r") as f:
        data = json.load(f)

    # Parse data
    patients: List[Patient] = [Patient(**patient) for patient in data["patients"]]

    # Example usage
    insert_into_memgraph(patients)

    print("Done!")


if __name__ == "__main__":
    main()
