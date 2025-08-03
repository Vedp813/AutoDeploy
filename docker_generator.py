import os

def generate_dockerfile(entry_point, requirements_path):
    # Get repo root directory by taking common path of both files
    repo_root = os.path.commonpath([entry_point, requirements_path])

    # Compute relative paths inside the container (repo_root maps to /app)
    rel_entry_point = os.path.relpath(entry_point, repo_root)
    rel_requirements = os.path.relpath(requirements_path, repo_root)

    dockerfile = f"""FROM python:3.9-slim

WORKDIR /app/app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "{rel_entry_point}"]
"""
    return dockerfile

def generate_docker_compose():
    return """services:
  app:
    build: .
    ports:
      - "5000:5000"
"""

def generate_docker_files(repo_path, entry_point, requirements_path, output_dir=None):
    if output_dir is None:
        output_dir = repo_path

    dockerfile_content = generate_dockerfile(entry_point, requirements_path)
    docker_compose_content = generate_docker_compose()

    dockerfile_path = os.path.join(output_dir, "Dockerfile")
    docker_compose_path = os.path.join(output_dir, "docker-compose.yaml")

    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)

    with open(docker_compose_path, "w") as f:
        f.write(docker_compose_content)

    return dockerfile_path, docker_compose_path
