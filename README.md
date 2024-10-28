# Automated Electrode-Placement Optimizer

abstract here.

<img src="./demo.gif" alt="User interface of the optimization system" style="max-width: 80%; height: auto;">


# Features

features description here.

# Requirement

* Python 3.11.9
* COMSOL Multiphysics 6.0 &copy;
* COMSOL LiveLink for MATLAB &copy;

This program can be used with COMSOL Multiphysics &copy; and COMSOL LiveLink for MATLAB &copy;. If only limited cached calculation results are utilized, it can be used without them.

Environments under [Anaconda for Windows](https://www.anaconda.com/distribution/) is tested.

```bash
cd [project root directory]
conda create -f env_elec_optim.yml
conda activate elecOptim
```

# Data preparation

Install Pyxel with pip command.

```bash
pip install pyxel
```

# Usage

Please create python code named "demo.py".
And copy &amp; paste [Day4 tutorial code](https://cpp-learning.com/pyxel_physical_sim4/).

Run "demo.py"

```bash
python demo.py
```

# Note

We don't test environments under Linux and Mac.

# Authors

* Takashi Ota
* The University of Tokyo

# License

This project is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
