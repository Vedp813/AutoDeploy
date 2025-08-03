import time

def simulate_terraform_apply(terraform_dir):
    print(f"Simulating: terraform init in {terraform_dir}")
    time.sleep(1)
    print("terraform init completed")

    print(f"Simulating: terraform apply in {terraform_dir}")
    time.sleep(2)
    print("terraform apply completed")

    # Simulated EC2 public IP
    public_ip = "54.210.123.45"
    print(f"Simulated deployment complete. Public IP: {public_ip}")
    return public_ip
