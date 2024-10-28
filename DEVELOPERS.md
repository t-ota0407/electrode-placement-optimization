# DEVELOPERS.md

### Project Overview
**Project Name:** Automated   
**Purpose:** By automatically performing FEM analysis for multiple conditions, this system determines the optimized electrode placement.  
**Key Features:** hogehoge

### Setting Up the Development Environment
* Recommended Environment
    * **OS:** Windows 11
    * **Language Version:** Python3.11
    * **Tools:** COMSOL Multiphysis 6.0 &copy;, COMSOL LiveLink for MATLAB &copy;
* Installation Steps
    1. Clone the repository:
        ```bash
        git clone https://github.com/t-ota0407/electrode-placement-optimization.git
        ```
    2. Activate the environment:
        ```bash
        conda activate ElecOptim
        ```
    3. hogehoge

### Project Structure
The directory structure of the project is outlined below.

```plaintext
electrode-placement-optimization/
├─── client/
|    ├─── resources/
|    |    ├─── images/
|    |    ├─── model_data_cache/
|    |    ......
|    ├─── src/
|    |    ├─── main.py
|    |    ├─── config.py
|    |    ......
|    ......
├─── server/

```

* **images/** 
* **model_data_cache/**
* **src/**
* **main.py**
* **config.py**

### Guidelines

##### Multilingual support
This project supports both English and Japanese using QTranslator from PyQt5. The translation definition files (.ts) are located under src/translations/. When updates are made to the translation definition files, running the following command will generate the .qm files from the updated definitions.
```bash
lrelease src/translations/ja.ts && lrelease src/translations/en.ts
```

