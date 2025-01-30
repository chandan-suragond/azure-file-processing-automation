# Azure File Processing Automation

![Azure Services](https://img.shields.io/badge/Azure-Storage%20%26%20Data_Factory-0089D6?logo=microsoft-azure)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)

A robust pipeline for automated file processing using Azure Blob Storage and Azure Data Factory (ADF), featuring:

- **Sequential File Processing**
- **Dynamic Pipeline Routing**
- **Status-based Archival**
- **Comprehensive Logging**

## 📋 Table of Contents
- [Architecture](#-architecture)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Setup](#-setup)
- [Configuration](#-configuration)
- [Workflow](#-workflow)
- [Logging](#-logging)
- [Running the Application](#-running-the-application)

## 🏗 Architecture
```plaintext
Local System → Azure Universal Container → Azure Source Container → ADF Pipeline → Azure Destination Container
                       ↑                                      ↓
                       └─────── Status-based Archival ←───────┘
```
## ✨ Features
- **Automated File Transfer**
  - Bulk upload from local directory to Azure Universal Container
  - Structured folder creation in source container (e.g., cocoblu/rebini/file.csv)
- **Intelligent Processing**
  - Pipeline selection based on filename prefixes
  - 20-minute timeout for pipeline execution
  - Real-time pipeline status monitoring
- **Reliable Archival**
  - Success/Failure folder structure in the destination container
  - Atomic file operations with rollback safety
    
## ✅ Prerequisites
- **Azure Resources**
  - Storage Account with 3 Containers:
    - `universal-container` (initial landing zone)
    - `source-container` (processing input)
    - `destination-container` (archival storage)
  - Data Factory with pipelines named per filename prefixes 
- **Local Environment**
  - Python 3.10+
  - Azure CLI installed and logged in
  - Network access to Azure services
    
## 🛠 Setup
1. **Clone Repository**

   ```bash
   git clone https://github.com/your-repo/azure-file-processor.git
   cd azure-file-processor

2. **Install Dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/MacOS
   .venv\Scripts\activate    # Windows
   pip install -r requirements.txt

## ⚙ Configuration
Edit `config.py` with your Azure credentials:

    ```python
    # Azure Storage
    STORAGE_ACCOUNT_NAME = "your-storage-account"
    STORAGE_ACCOUNT_KEY = "base64-encoded-key"  # From Azure Portal
    UNIVERSAL_CONTAINER = "universal-container"
    SOURCE_CONTAINER = "source-container"
    DESTINATION_CONTAINER = "destination-container"
    
    # Data Factory
    ADF_SUBSCRIPTION_ID = "your-subscription-id"
    ADF_RESOURCE_GROUP = "your-resource-group"
    ADF_FACTORY_NAME = "adf-factory-name"
    PIPELINE_NAMES = ["test_pipeline_cocoblu", "test_pipeline_retailez"]
    
    # Local Settings
    LOCAL_DIRECTORY = "/path/to/your/local/files"
    SUPPORTED_EXTENSIONS = [".csv", ".xlsx"]  # Add/remove as needed

## 🔄 Workflow
1. **File Upload**
   - All files from `LOCAL_DIRECTORY` uploaded to Universal Container
   - Supported formats: `.csv`, `.xls`, `.xlsx`, `.xlsb`
2. **Sequential Processing**
   For each file in Universal Container:
   - **Copy to Source**: Creates folder structure from filename
     - `cocoblu_rebini.csv` → `cocoblu/rebini/cocoblu_rebini.csv`
   - **Pipeline Execution**:
     - Selects pipeline based on filename prefix
     - Passes `filenamePrefix` parameter to ADF
   - **Archival**:
     - Success → `destination-container/success_archival/`
     - Failure → `destination-container/failure_archival/`

## 📝 Logging

**Format**  

`[TIMESTAMP] [LEVEL] [FILE : FUNCTION : LINE] MESSAGE`  

**Example**  

    ```log
    [2024-02-15 14:30:45] [INFO] [processor.py : process_file : 42] Triggering pipeline for cocoblu_rebini.csv
    [2024-02-15 14:31:00] [SUCCESS] [mover.py : archive_file : 28] Moved cocoblu_rebini.csv to success_archival  

**Log Locations**  

- Console output (default)
- `app.log` file (if enabled in `logger_config.py`)

## 🚀 Running the Application
    ```bash
    python main.py
**Expected Output**
    ```log
    [2024-02-15 14:30:00] [INFO] [main.py : main : 15] Starting processing cycle
    [2024-02-15 14:30:05] [INFO] [uploader.py : upload_to_universal : 22] Uploaded 5 files to universal-container
    [2024-02-15 14:30:10] [INFO] [copier.py : copy_to_source : 18] Processing cocoblu_rebini.csv
    [2024-02-15 14:31:00] [SUCCESS] [processor.py : process_file : 56] Pipeline test_pipeline_cocoblu completed
## 🗂 File Structure
    ```
    ├── config.py             # Configuration settings
    ├── main.py               # Main orchestration
    ├── uploader.py           # Local → Azure uploads
    ├── copier.py             # Universal → Source container
    ├── processor.py          # ADF pipeline management
    ├── mover.py              # Status-based archival
    ├── logger_config.py      # Logging setup
    └── requirements.txt      # Dependencies
    ```
## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add some feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open Pull Request
