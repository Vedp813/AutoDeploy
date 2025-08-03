import argparse
import os
from docker_generator import generate_docker_files
from parser import parse_prompt
from repo_handler import fetch_repo, analyze_repo
from script_generator import generate_deploy_script
from terraform_generator import generate_terraform_config
from terraform_runner import simulate_terraform_apply


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--description", required=True, help="Natural language deployment prompt")
    parser.add_argument("--repo", required=True, help="GitHub repo URL or zip file path")
    args = parser.parse_args()

    # Create persistent output directory for cloning repos
    base_output_dir = os.path.abspath("deploy_output")
    os.makedirs(base_output_dir, exist_ok=True)
    print(f"Using output directory for cloning: {base_output_dir}")

    # Phase 1: Parse prompt
    app_type, cloud_provider = parse_prompt(args.description)
    print(f"Detected: App={app_type}, Cloud={cloud_provider}")

    # Phase 2: Fetch and analyze repo
    repo_path = fetch_repo(args.repo, download_dir=base_output_dir)
    print(f"Repo downloaded to: {repo_path}")

    entry_point, requirements_path = analyze_repo(repo_path)
    if entry_point:
        print(f"Found entry point: {entry_point}")
    if requirements_path:
        print(f"Found requirements: {requirements_path}")

    # Phase 3: Generate deployment script INSIDE repo folder
    script_path = generate_deploy_script(
        app_type=app_type,
        cloud_provider=cloud_provider,
        repo_path=repo_path,
        entry_point=entry_point,
        requirements_path=requirements_path,
        output_dir=repo_path   # Changed here to repo_path
    )
    print(f"Deployment script generated: {script_path}")
    print("\nNext step: Run the script using:")
    print(f"bash {script_path}")

    # Generate Terraform config INSIDE repo folder
    relative_app_dir = "app"  # or detect dynamically if needed
    app_entry_file = "app.py" # or detect dynamically
    key_name = "my-key"       # placeholder, update if needed

    generate_terraform_config(
        output_dir=repo_path,  # Changed here to repo_path
        repo_url=args.repo,
        relative_app_dir=relative_app_dir,
        app_entry_file=app_entry_file,
        key_name=key_name,
    )

    # Simulate terraform apply from the repo folder
    public_ip = simulate_terraform_apply(repo_path)

    print(f"\n Application deployed at http://{public_ip}:5000")

    # Phase 4: Generate Dockerfile and docker-compose INSIDE repo folder
    dockerfile_path, compose_path = generate_docker_files(
        repo_path=repo_path,
        entry_point=entry_point,
        requirements_path=requirements_path,
        output_dir=repo_path   # Changed here to repo_path
    )
    print(f"Dockerfile generated: {dockerfile_path}")
    print(f"docker-compose.yaml generated: {compose_path}")


if __name__ == "__main__":
    main()
