# Hotel Reservation Prediction (MLOps End-to-End Project)

An end-to-end Machine Learning Operations (MLOps) project that predicts hotel reservation cancellations. The project incorporates modular data and training pipelines, experiment tracking with MLflow, continuous integration and deployment using Jenkins and Docker, and cloud orchestration via Google Cloud Platform (GCP).

---

## Project Structure

```text
├── .github/workflows/   # CI/CD workflows for GitHub Actions
├── config/              # Configuration files (paths, model hyperparams)
├── custom_jenkins/      # Custom Jenkins server configurations/scripts
├── notebook/            # Exploratory Data Analysis & experimental notebooks
├── pipeline/            # Training and prediction pipelines
├── src/                 # Core source code (data ingestion, preprocessing, training)
├── static/              # CSS, JavaScript, and asset files for web UI
├── templates/           # HTML templates (Flask/web app)
├── utils/               # Common helper functions and utilities
├── app.py               # Web service application entry point
├── Dockerfile           # Docker container specification
├── Jenkinsfile          # Jenkins CI/CD pipeline definition
├── requirements.txt     # Python dependencies
├── setup.py             # Package installation setup
└── template.py          # Project scaffolding generator script
