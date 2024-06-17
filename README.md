# Kubernetes Resource Checker

This project is a Python script for checking various Kubernetes resources such as Persistent Volumes (PVs), pods using hostPath volumes, ConfigMaps mounted in pods, and Network Policies. The script interacts with the Kubernetes API to gather information and can output the results in either CSV or table format.

## Features

- Check for Persistent Volumes (PVs) using hostPath.
- Check for pods using hostPath volumes.
- Check for ConfigMaps mounted in pods and their mount paths.
- Check for Network Policies.
- Modular design for easy addition of new checks.
- Log messages for detailed information.
- Output results in CSV or table format.

## Requirements

- Python 3.6+
- Kubernetes cluster access

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ozkanpoyrazoglu/kubeinspector.git
    cd kubeinspector
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the script with the desired options:
```sh
python main.py [-o OUTPUT] [-m MODULE]
