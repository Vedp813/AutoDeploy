import os

def generate_deploy_script(app_type, cloud_provider, repo_path, entry_point, requirements_path, output_dir=None):
    if app_type != "flask" or cloud_provider != "aws":
        raise NotImplementedError("Only Flask on AWS EC2 is currently supported.")

    if output_dir is None:
        output_dir = repo_path

    script_lines = [
        "#!/bin/bash",
        "# Deployment script for Flask app on AWS EC2 with Gunicorn + NGINX",
        "set -e",
        "",
        "echo 'Updating system...'",
        "sudo apt update && sudo apt install -y python3-pip python3-venv nginx",
        "",
        "echo 'Creating virtual environment...'",
        "python3 -m venv venv",
        "source venv/bin/activate",
        f"pip install --upgrade pip",
        f"pip install -r {requirements_path}",
        "",
        "echo 'Starting Gunicorn service setup...'",
        "cat <<EOF | sudo tee /etc/systemd/system/flaskapp.service",
        "[Unit]",
        "Description=Gunicorn instance to serve Flask App",
        "After=network.target",
        "",
        "[Service]",
        "User=ubuntu",
        "Group=www-data",
        f"WorkingDirectory={repo_path}/app",
        f"Environment=\"PATH={repo_path}/venv/bin\"",
        f"ExecStart={repo_path}/venv/bin/gunicorn --workers 3 --bind unix:flaskapp.sock -m 007 app:app",
        "",
        "[Install]",
        "WantedBy=multi-user.target",
        "EOF",
        "",
        "sudo systemctl daemon-reexec",
        "sudo systemctl daemon-reload",
        "sudo systemctl start flaskapp",
        "sudo systemctl enable flaskapp",
        "",
        "echo 'Configuring NGINX...'",
        "cat <<EOF | sudo tee /etc/nginx/sites-available/flaskapp",
        "server {",
        "    listen 80;",
        "    server_name _;",
        "",
        "    location / {",
        "        include proxy_params;",
        f"        proxy_pass http://unix:{repo_path}/app/flaskapp.sock;",
        "    }",
        "}",
        "EOF",
        "",
        "sudo ln -sf /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled",
        "sudo nginx -t",
        "sudo systemctl restart nginx",
        "",
        "echo 'Deployment complete! Your Flask app should be live.'"
    ]

    deploy_script_path = os.path.join(output_dir, "deploy.sh")
    with open(deploy_script_path, "w") as f:
        f.write("\n".join(script_lines))

    os.chmod(deploy_script_path, 0o755)
    return deploy_script_path
