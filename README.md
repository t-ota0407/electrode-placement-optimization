# Automated Electrode-Placement Optimizer

This project aims to efficiently optimize the parameters of transcutaneous electrical nerve stimulation (TENS) through numerical analysis. This system conduct FEM-based analyses across a large number of electrode placement conditions, identifying condition that effectively stimulate the target tissue.

[日本語版のREADMEはこちら](./README_ja.md)

<img src="./demo.gif" alt="User interface of the optimization system" style="max-width: 80%; height: auto;">

## Features

* **Support for Multiple Body Part:** This system supports optimizatation of TENS in the lower limb, upper limb, head.
* **Advanced Optimization Settings:** This system supports not only current density maximization for single target domain but also conditional optimization concerning current densities in other domains. In this mode, detailed constraint parameters can be configured.
* **Intuitive and Lightweight UI:** This system was implemented using VisPy and PyQt5. The UI operates efficiently by leveraging GPU resources for rendering processes.
* **Detailed Accessemnt:** Detailed results can be accessed through logs.

## Requirement

* Python 3.11.9
* COMSOL Multiphysics 6.0 &reg;
* COMSOL LiveLink for MATLAB &reg;

This program can be used with COMSOL Multiphysics &reg; and COMSOL LiveLink for MATLAB &reg;. If only limited cached calculation results are utilized, it can be used without them.

Environments under [Anaconda for Windows](https://www.anaconda.com/distribution/) is tested. The following script can recreate the Anaconda environment used for the test.

```bash
cd [project root directory]/client
conda create -f env_elec_optim.yml
conda activate elecOptim
```

## Data Preparation
### When Using the Cache
1. You need to prepare the cache data. Please contact the contributors mentioned later to request the use of the cache data.

### When Not Using the Cache
1. You need to prepare the FEM solver. Please set up [COMSOL Multiphysics &reg;](https://www.comsol.jp/comsol-multiphysics) and [COMSOL LiveLink for MATLAB &reg;](https://www.comsol.jp/livelink-for-matlab).
1. Please create appropriate models refering our research paper.
1. Please modify the program appropriately refering our research paper.

## Usage
### When Using the Cache
1. Please modify `client/src/config.py` as follows:
    ```python
    USE_CACHE = True

    LOWER_LIMB_CACHE_DIR_PATH = [path to cache]
    UPPER_LIMB_CACHE_DIR_PATH = [path to cache]
    HEAD_CACHE_DIR_PATH = [path to cache]
    ```
1. Please start the system by running the following commands:
    ```bash
    cd client/src
    python main.py
    ```

### When Not Using the Cache
1. Please modify the variables in `server/OptimizationServer.m` appropriately.
1. With COMSOL LiveLink for MATLAB &reg; running, execute `server/OptimizationServer.m`.
1. Please modify `client/src/config.py` as follows:
    ```python
    USE_CACHE = False

    REMOTE_HOST = [remote host name]
    REMOTE_PORT = [port number]
    ```
1. In a separate process, please start the system by running the following commands:
    ```bash
    cd client/src
    python main.py
    ```

## Note

* We have not tested the system under Linux and Mac environments.
* This repository aims to share part of the program in our research project. For details on the research, please refer the research paper.
* Technical details can be refered [here](./DEVELOPERS.md).

## Contributors

* Takashi Ota, The University of Tokyo (ota [at] cyber.t.u-tokyo.ac.jp)
* Kazuma Aoyama, The University of Tokyo (aoyama [at] vr.t.u-tokyo.ac.jp), Gunma University (aoyama [at] gunma-u.ac.jp)

If you need any information to confirm the reproducibility of this research, please contact us by email.

## License

This project is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
