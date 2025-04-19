# Network Anomaly Detector

## Overview
todo: add project desc here



## Setup

This project uses [Poetry](https://python-poetry.org/) to manage virtual environments and dependencies.

To setup and run the tool, run the following commands in order (WSL 2.0, Ubuntu):


Install poetry as a system-wide command tool.
```shell
sudo apt update && apt install python3-poetry
```

Make sure you are in the project's root location and run the following command to install the dependecies and initial venv setup.
```shell
poetry install
```

Run with poetry:
```shell
poetry run python main.py
```

Or run within venv:
```shell
poetry shell

python3 main.py
```


## Links & References

Dataset used: [Network Intrusion dataset(CIC-IDS- 2017)](https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset)


