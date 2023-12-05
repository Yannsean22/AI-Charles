import subprocess

try:
    result = subprocess.run(['hcitool', 'scan'], capture_output=True, text=True, check=True)

    lines = result.stdout.strip().split('\n')[1:]

    for line in lines:
        print(line)

except subprocess.CalledProcessError as e:
    print(f"Error: {e}")