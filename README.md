# bike-prediction-ml - Instructions
This repository contains a production-ready Machine Learning model for forecasting bike demand for the Capital bikeshare system.
## 1. Repository contents

```
.
├── README.md                                       > Contains instructions on what the repository contains, how to set up the modules and how to use them.
├── data                                            > Contains all csv and excel files and model.pkl
|    ├── models                                     >> Folder with trained models
|    |      └── catboost_model.cbm                  >>> Trained  and serialized model
|    ├── training_data.csv                          >> Master training data
|    ├── config.yaml.csv                            >> Model features
├── app                                             > Folder for Prediction api code
|    ├── prediction.py                              >> Prediction module and command line API
|    ├── get_prediction.py                          >> Python script to test prediciton API
|
├──tests                                            > Folder with python unit tests for repository      
|    ├── test_prediction_api.py                     >> API endpoint tests
├── config.ini                                      >> Configuration file with all the initialized values and paths
├── Dockerfile                                      >> Dockerfile for building image and spawning container for prediction API
├── requirements.txt                                >> Requirements file with all dependencies
```  

## 2. Docker installation (skip if you already have Docker installed)

Docker installation depends on the host OS. Please refer [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/) for OS specific instructions. The following example is for Linux 7 installation:

- Run the following commands on terminal
    1. sudo yum install -y yum-utils zip unzip
    2. sudo yum-config-manager --enable ol7\_optional\_latest
    3. sudo yum-config-manager --enable ol7\_addons
    4. sudo yum install -y oraclelinux-developer-release-el7
    5. sudo yum-config-manager --enable ol7\_developer
    6. sudo yum install -y docker-engine btrfs-progs btrfs-progs-devel
    7. sudo systemctl enable --now docker
    8. sudo chmod 666 /var/run/docker.sock

- Check if docker is properly installed by running the command:

        docker run hello-world

## 3. Setting up Prediction and Retraining Service

1. Move into Scraping-module folder (the scraping and prediction module):

    	cd bike-prediction-ml/

2.  Run docker build command

        docker build --tag bike-prediction-ml . #rename as required

    - This command should download all the required dependencies and libraries automatically.

3. Run the docker image (replace {PATH} with the path to this repository)
    - To run docker container in Interactive mode:

            docker run -it -p {HOST_PORT_CHOICE}:5555 bike-prediction-ml

    - To run docker container in Detached mode: **(Recommended)**

            docker run -d -p {HOST_PORT_CHOICE}:5555 bike-prediction-m

4. Predictions can also be accessed via the terminal with the following command:
    ```
    curl -X POST http://127.0.0.1:5000/prediction \-H "Content-Type: application/json" \-d '{"date": "2024-03-17"}'
    ```
    Or by running the `test_prediction_app.py` script in the `test` folder.

## API Documentation

### Endpoint: `/prediction/`

<a name="prediction"></a>

- **Method**: POST
- **Purpose**: Fetches the hourly forecast on bike rental demand for the given date.

- **Request**:
  - **Body**:
    - `date`: date in the format "YYYY-MM-DD".

- **Response**: A dictionary with the hours of the day as the keys and the forecasted demand as the values.

- **Example**:

  **Request**:
  ```json
  {
    "date": "2025-06-17'"
  }
  ```

  **Response**:
  
    ```json
    {"0": 122.61645440871234, "1": 90.421508067395, "2": 68.23767079434626, "3": 33.817141596024385, "4": 24.418046302801486, "5": 31.40367799480748, "6": 55.83285229964325, "7": 123.39448565725763, "8": 228.00894382430394, "9": 285.79271912890874, "10": 392.38677788603593, "11": 455.8238122110369, "12": 513.0105588192546, "13": 516.6045843676111, "14": 508.3662804962507, "15": 514.3626031538838, "16": 532.9201113724275, "17": 529.33354355843, "18": 489.8726974745671, "19": 388.7894078735194, "20": 341.68015521930096, "21": 269.28715935410673, "22": 181.03138714804314, "23": 116.27599805626227}
    ```
    - Model is not retrained regularly so valid dates can be found in valid_dates.csv.

## 4. Testing

### Tests in the `tests` folder

The `tests` folder contains unit tests designed to ensure the robustness and accuracy of the prediction module:

- **`test_prediction_api.py`**: Contains tests for the prediction API endpoints. These tests simulate API requests and check for correct status codes, response formats, and the accuracy of predictions for known inputs.

To run these tests, spawn the docker container, navigate to the repository root and execute:


## 5. CI/CD Pipeline

The CI/CD pipeline for this project is defined in the `.github` folder, which contains GitHub Actions workflows for automated testing, Docker image building, and deployment.

### Key Components:

- **Automated Testing**: On every push or pull request, the CI pipeline runs unit tests defined in the `tests` folder to ensure code changes do not break existing functionality.

- **Docker Image Building**: For merges into the main branch, the CI pipeline automatically builds a Docker image for the prediction API using the `Dockerfile`.

- **Deployment**: The CD pipeline can be configured to automatically deploy the latest Docker image to a production environment, ensuring that the prediction service is always up-to-date.

To customize the CI/CD pipeline for your environment, modify the workflow files in the `.github/workflows` directory.

```bash
python -m unittest discover -s tests