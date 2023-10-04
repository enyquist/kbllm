KBLLM Overview
==============================
Knowledge Base Large Language Model (KBLLM) explores the integration of LLMs and knowledge bases. The intent is to design a system that can extract data from source documents, build a knowledge graph, then refer to this knowledge graph during inference. This system will enable LLMs to be factually grounded during a chat session.


## Features

* **Encounter-Centric Views**: Easily trace the entire patient's healthcare journey, from encounters with providers to prescribed treatments.

* **Data Integration**: Effortlessly merge scattered data from different sources into a coherent and unified view.

* **Complex Querying**: Use Cypher query language to extract insights, such as all diagnoses associated with a specific patient.

* **Scalable**: Designed to handle large datasets, ensuring smooth performance as the data grows.

## Installation and Setup

Assumes you have Python3.10 and python3.10-venv installed. Also assumes you have [Memgraph](https://memgraph.com/) set up and running.

Clone the repository:

```sh
git clone https://github.com/enyquist/kbllm.git
```
Navigate to the directory:

```sh
cd kbllm
```

Create venv:

```sh
make init
```

Populate Memgraph:

```sh
python scripts/main.py
```

## Explore Data

You can checkout `notebooks/memgraph_demo.ipynb` for an introduction of how to query Memgraph.

A demo video is available [here](https://youtu.be/ObpOV2dRnTY).

## TODO

* Design LLM Agent for data insertion
* Design LLM Agent for data queries

## Contributing

This repository was created as part of [Advanced Artificial Intelligence](https://ep.jhu.edu/courses/605743-advanced-artificial-intelligence/) from Johns Hopkins Fall 2023. Until completion late 2023, no contributions can be accepted unless directed by Johns Hopkins Faculty.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contact

For any questions or feedback, please reach out to enyquis1@jh.edu.

