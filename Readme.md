# AutoDeployment Chat System

## Overview

**AutoDeployment Chat System** automates app deployment using just a natural language prompt and a code repo. It intelligently parses what the user wants, analyzes the codebase, and auto-generates all necessary deployment scripts — including Dockerfiles, Terraform configs, and cloud setup — without manual intervention.

---

## What It Can Do

- Understands deployment instructions written in natural language (e.g., "Deploy this Flask app to AWS EC2").
- Clones and analyzes a GitHub repo or zip file.
- Auto-generates:
  - Shell deployment scripts
  - Dockerfile and docker-compose.yaml
  - Terraform files for AWS EC2 provisioning
- Simulates Terraform provisioning (can be extended for actual apply).
- Designed for **Flask apps** on **AWS EC2** — easily extendable to other stacks and clouds.

---

## Project Structure

```plaintext
auto-deploy/
├── main.py                      # CLI entry point for deployment tool
├── parser.py                   # Parses natural language prompts
├── repo_handler.py             # Clones GitHub repo or unzips file
├── script_generator.py         # Generates deployment scripts
├── terraform_generator.py      # Creates Terraform configs
├── terraform_runner.py         # Simulates Terraform run
├── docker_generator.py         # Builds Docker-related files
├── requirements.txt            # Python dependencies for the deployment tool
├── templates/                  # Jinja2 templates for config generation
│   └── aws_ec2.tf.j2          # Terraform template for AWS EC2 instance
└── README.md                   # Project documentation
```

---

## Prerequisites

- Python 3.9+
- Git
- Docker (for local container deployment)
- Terraform (optional, for actual provisioning)
- Internet access to clone public GitHub repos

Install dependencies:

```bash
pip install -r requirements.txt

```

---

## How to Run the Project

Follow these steps to get started:

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd auto-deploy
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run with a GitHub Repository URL (For example in our case Arvo-AI Repo)

```bash
python3 main.py \
  --description "Deploy this Flask app on AWS" \
  --repo https://github.com/Arvo-AI/hello_world
```
