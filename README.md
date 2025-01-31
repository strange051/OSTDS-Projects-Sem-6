# OSTDS Projects Sem-6

## Folder Structure

```
/OSTDS-Projects-Sem-6
│
├── .gitignore               # Files and directories to ignore in Git
├── README.md                # Project overview and instructions
├── requirements.txt         # List of project dependencies
│
└── /assign_1_corona         # Corona project
    ├── /data                # Corona dataset
    ├── /logs                # Log files
    ├── /src                 # Source code
    │   ├── main.py          # Main code
    │   └── logger.py        # Logger
    │
    └── README.md            # Project todos
```

## Setup

1. **Clone the Repository:**

   ```powershell
   git clone https://github.com/strange051/OSTDS-Projects-Sem-6.git
   cd OSTDS-Projects-Sem-6
   ```

2. **Set Up a Virtual Environment:**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install Dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Open the folder in VSCode and run main.py**

## Git Commands

1. **Create Your Branch:**

   ```powershell
   git checkout -b dev_<yourname>
   ```

2. **Make Changes, Stage, and Commit:**

   ```powershell
   git add .
   git commit -m "Description of changes"
   ```

3. **Push Your Branch:**

   ```powershell
   git push origin dev_<yourname>
   ```
