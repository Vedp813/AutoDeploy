# terraform_generator.py

import os
from jinja2 import Environment, FileSystemLoader

def generate_terraform_config(output_dir, repo_url, relative_app_dir, app_entry_file, key_name="my-key"):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("aws_ec2.tf.j2")

    rendered = template.render(
        repo_url=repo_url,
        relative_app_dir=relative_app_dir,
        app_entry_file=app_entry_file,
        key_name=key_name
    )

    output_path = os.path.join(output_dir, "main.tf")
    with open(output_path, "w") as f:
        f.write(rendered)

    print(f"Terraform script generated at: {output_path}")
    return output_path
