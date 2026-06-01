# tests/run_all_tests.py
import subprocess
import sys

tests = [
    "test_lindblad_accuracy.py",
    "test_isolated_tunneling.py",
    "test_complementarity.py"
]

for test in tests:
    print(f"\n--- Running {test} ---")
    result = subprocess.run([sys.executable, test], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
