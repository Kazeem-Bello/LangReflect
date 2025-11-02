<h1 align="center">LangReflect</h1>
<h3 align="center">Reflects the True Languages Behind Your GitHub Repositories</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python" alt="Python Version"/>
  <img src="https://img.shields.io/badge/GitHub%20Actions-Automated-success?style=flat-square&logo=githubactions" alt="GitHub Actions"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
</p>

---

### Overview

**LangReflect** is a Python-powered automation tool that ensures your GitHub repositories accurately reflect the programming languages you’ve actually used.  
It automatically creates or updates a standardized `.gitattributes` file so that **Jupyter Notebooks are correctly classified as Python**, and non-code directories (like datasets, logs, and checkpoints) are ignored.  
This ensures your **GitHub profile truly represents your coding activities** and highlights your primary language correctly.

The project leverages **GitHub Actions** and **PyGithub** to automate `.gitattributes` management securely and efficiently.

---

### Key Features

- Automatically updates `.gitattributes` across all repositories you own  
- Detects and supports both `main`, `master`, or custom default branches  
- Secure GitHub authentication via `.env` and GitHub Secrets  
- Lightweight setup using Python virtual environments  
- Ensures accurate GitHub language statistics   
- Generates and commits a **visual chart (`langreflect_chart.png`)** showing your real language usage   
- Commits `update_log.txt` back to the repo for traceability  
- Runs on a monthly schedule or manually via GitHub Actions  

---

### How It Works

1. The Python script (`langReflect.py`) connects to your GitHub account using the [PyGithub](https://github.com/PyGithub/PyGithub) API.  
2. It loops through all your repositories.  
3. For each repo, it:
   - Detects the default branch (`main`, `master`, or custom)
   - Checks for an existing `.gitattributes` file  
   - Creates or updates it with standardized language classification rules  
4. Logs every action (created, updated, skipped, or failed) in `update_log.txt`.  
5. The **chart generator script (`langChart.py`)** aggregates all language data and generates a visual bar chart (`langreflect_chart.png`) in GitHub Readme Stats style.  
6. Both the `.gitattributes` log and chart are automatically committed back to the repository through **GitHub Actions**.

---

### Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.11** | Core runtime |
| **PyGithub** | GitHub API interaction |
| **python-dotenv** | Secure environment variable loading |
| **Matplotlib** | Generates the language usage chart |
| **GitHub Actions** | CI/CD automation |

---

### Local Setup Instructions

#### 1. Clone the repository
```bash
git clone https://github.com/Kazeem-Bello/LangReflect.git
cd LangReflect
```

#### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables
Create a `.env` file in the root directory and add:
```
GITHUB_TOKEN=your_personal_access_token_here
```
> The token must have `repo` and `workflow` scopes.

#### 5. Run the scripts locally
```bash
python langReflect.py
python langChart.py
```

---

### GitHub Actions Automation

A fully configured workflow file (`.github/workflows/cicd.yaml`) automates everything on a schedule.

It:
- Sets up Python and a virtual environment  
- Installs dependencies from `requirements.txt`  
- Loads secrets dynamically from GitHub Secrets  
- Runs both automation scripts (langReflect.py and langChart.py)
- Commits and pushes the log file and chart image back to the repository

#### Required GitHub Secrets

| Secret Name | Description |
|--------------|-------------|
| `PERSONAL_GITHUB_TOKEN` | Personal Access Token with `repo` + `workflow` scopes |

#### Schedule
By default, the workflow runs **automatically at 09:00 UTC on the 1st of every month**, and can also be triggered manually via the Actions tab.

---


### Project Structure

```
LangReflect/
│
├── langReflect.py                # Main automation script
├── langChart.py                  # Generates the language usage chart
├── .github/
│   └── workflows/
│       └── cicd.yaml             # GitHub Actions workflow
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (not committed)
├── update_log.txt                # Generated log per run
├── langreflect_chart.png         # Auto-generated language chart
└── README.md                     # Project documentation

```

---

### Acknowledgements

- [PyGithub](https://github.com/PyGithub/PyGithub) — GitHub API integration  
- [GitHub Linguist](https://github.com/github/linguist) — Language detection engine  
- [GitHub Actions](https://docs.github.com/en/actions) — CI/CD automation platform  

---

<h3 align="center">Automate once. Stay consistent forever.</h3>
