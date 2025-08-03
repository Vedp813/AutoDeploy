# parser.py

def parse_prompt(prompt):
    prompt = prompt.lower()
    if "flask" in prompt:
        app = "flask"
    elif "django" in prompt:
        app = "django"
    elif "node" in prompt:
        app = "node"
    else:
        app = "unknown"

    if "aws" in prompt:
        cloud = "aws"
    elif "gcp" in prompt:
        cloud = "gcp"
    else:
        cloud = "aws"  # default

    return app, cloud
