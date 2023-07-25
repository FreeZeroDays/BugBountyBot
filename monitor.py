import subprocess
import argparse
import time

def run_bash_command(command, verbose=False):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        if verbose:
            print(output)
        return output
    except subprocess.CalledProcessError as e:
        error_output = f"Error: {e.stderr.strip()}"
        if verbose:
            print(error_output)
        return error_output

def main():
    parser = argparse.ArgumentParser(description="Run specified bash commands.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Provide output for the commands.")
    args = parser.parse_args()

    # Hardcode list of bash commands here
    commands = [
        "file=domains.txt; while IFS= read -r line; do subfinder -silent -dL $file -all -o $line-subdomains; done < $file",
    ]

    while True:
        for command in commands:
            run_bash_command(command, verbose=args.verbose)
        time.sleep(3600)  # Wait for 3600 seconds (1 hour) before running the commands again

if __name__ == "__main__":
    main()
