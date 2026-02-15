"Author: M Danish Zaheer (Roll No: 25280092)"

This is an Extract->Load->Tranform (ELT) pipeline which includes:

- Process 1: Extraction (Downloading raw)
- Process 2: Processing (convert raw into csv/json)
- Process 3: Transformation (jupyter notebook convert proessed csv/json into cleaned csv/json)
- Process 4: Visualization (jupyter notebook will show )

All logs are saved in one file:

- logs/pipeline.log

---

## Necessary installations

### Step: 1 Create conda environment (data_engg)

-- open terminal in downloaded folder and run make sure you have downloaded and installed Anaconda on your working station:

```bash
conda activate
conda create -n data_engg python=3.14.2 -y
conda activate data_engg
```

### Step: 2 Install requirements

-- requirements.txt:

```bash
conda env update -n data_engg -f environment.yml
```

### Step: 3 Register environment as ipykernel to run ipynb using Papermill

```bash
python -m ipykernel install --user --name data_engg --display-name "Python (data_engg)"
```

---

## Step: 4 Add .env file for API keys

The `.env` file is needs to be added at root with the following pattern below:

```env
KAGGLE_USERNAME="your_username"
KAGGLE_KEY="your_kaggle_key"
RANSOMWARE_LIVE_API_KEY="your_ransomware_live_key"
NVD_API_KEY="your_nvd_key"
```

API Keys setup links:

- Kaggle: https://www.kaggle.com/settings
- Ransomware.live: https://my.ransomware.live/
- NVD: https://nvd.nist.gov/developers/request-an-api-key

---

## Step: 5 Run the pipeline

-- run this from project root:

```bash
python main_run_pipeline.py
```

---

## On and off parameters

In `main_run_pipeline.py` you can control what you want to run by default all are kept TRUE:

```python
RUN_EXTRACT_KAGGLE = False
RUN_EXTRACT_PYTRENDS = False
RUN_EXTRACT_RANSOMWARE = False
RUN_EXTRACT_NVD = False

RUN_PROCESS_KAGGLE = False
RUN_PROCESS_PYTRENDS = False
RUN_PROCESS_RANSOMWARE = False
RUN_PROCESS_NVD = False

RUN_TRANSFORMATION = False
RUN_VISUALIZATIONS = False
```

## Step: 6 Cleaning and visualization part:

The cleaning part is done in code_files -> transformation and the .ipynb file exisits there once pipeline is executed it will run automatically you can see generated results in there
Same the visulizations folder contains visulizations .ipynb file will read cleaned data and produce visulaization on it

How to execute the .ipynb files automatically used for cleaning and visualization of dataset:
'''
-The data cleaning file is accessed and view as code_files\transformations\processed_data_transformation.ipynb
-The data Visualization file is accessed and view as visualizations\visualizations_code_file.ipynb
-These both files will automatically be executed using papermil library no need to execute them just make sure that in main_run_pipeline.py file on line is kernel_name= "data_engg"
---If one have have perfectly setup ipykernel for data_engg env and display name otherwise remove this code of line 141 and 150 kernel_name= "data_engg" and these file will be executed on python3 kernel

## Documentational view:

'''
The Q&A folder contains the answers to Part-1 and Part-2 qustions
'''
