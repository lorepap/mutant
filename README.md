[![Kernel CI](https://github.com/Principe92/mimic/actions/workflows/kernel.yml/badge.svg)](https://github.com/Principe92/mimic/actions/workflows/kernel.yml)

# Introduction

MIMIC is a Machine Learning powered congestion control protocol. Using a pool of trained reinforcement learning models, it selects at each time instance the best protocol to handle congestion at the kernel level.

# Architecture
![system-1](https://github.com/lorepap/mutant/assets/56161227/98336005-256a-49dc-a053-f345f6becae2)

# Algorithm
![mutant_algorithm-1](https://github.com/lorepap/mutant/assets/56161227/1455ea1d-2dcd-440f-a2ee-39816bc80950)

# Set up

Follow the steps below to get started

### 1. Install dependencies

Run the following command to install required modules
```bash
~/mimic$ sh scripts/setup.sh
```

Make sure you have the latest pip version. Install the following requirements.
```bash
~/mimic$ cd src
~/mimic/src$ source venv/bin/activate
(venv) ~/src$ pip3 install --upgrade setuptools pip
(venv) ~/src$ pip3 install -r requirements.txt
```


### 2. Build kernel module

Open a new terminal and run the following bash scripts from the root of the project to build and install the kernel. This will also set _mimic_ as the default congestion avoidance protocol
```bash
~/mimic$ sh scripts/init_kernel.sh
```

# Train

## Start training

Run the following command to start training from zero. Check models.yml for the list of possible models
```bash
(venv) ~/mimic/src$ python3 ml/train.py [--all | --models=<bootstrapped_ucb> ...] [--trace="<name>"] [--retrain=False]
```

Run the following command to retrain latest model. Check models.yml for the list of possible models
```bash
(venv) ~/mimic/src$ python3 ml/train.py [--all | --models=<bootstrapped_ucb> ...] [--trace="<name>"] [--retrain=True]
```

# Test

Run the following command to test. Check models.yml for the list of possible models
```bash
(venv) ~/mimic/src$ python3 ml/test.py [--all | --models= <owl> ...] [--trace="<name>"]
```

# Harm Analysis

Run the following command to start harm analysis using cubic.
```bash
(venv) ~/mimic/src$ python3 ml/harm.py [--solo | --against] [--trace="<name>"]
```

