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
    1. Activate the environment:
        ```bash
        conda activate ElecOptim
        ```

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

* **images/** contains all the images used by the client application.
* **model_data_cache/** contains all the static point cloud data used by the client application.
* **src/** contains the python code for the client application.
* **main.py** is the entry point of the client application.
* **config.py** is the setting file of the client application.

### Guidelines

#### Multilingual support
This project supports both English and Japanese using QTranslator from PyQt5. The translation definition files (.ts) are located under src/translations/. When updates are made to the translation definition files, running the following command will generate the .qm files from the updated definitions.
```bash
lrelease src/translations/ja.ts && lrelease src/translations/en.ts
```

