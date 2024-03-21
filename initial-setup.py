import subprocess


def run_command(command):
    process = subprocess.run(command, shell=True, check=True)


try:
    # Install Poetry globally
    print("Installing Poetry...")
    run_command("pip install poetry")

    print("Installing project dependencies with Poetry...")
    run_command("poetry install")

    # Installing pre-commit using pip within Poetry's environment
    print("Installing pre-commit...")
    run_command("poetry run pip install pre-commit")

    # Install the pre-commit hooks
    print("Setting up pre-commit hooks...")
    run_command("poetry run pre-commit install")

    print("Setup complete.")

except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
