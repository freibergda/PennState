
from datetime import datetime

def log_test_result(test_id, description, steps, expected_response, result, log_file):
    with open(log_file, "a") as f:
        f.write(f"---------------------------------------------\n")
        f.write(f"Test Type: Unit\n")
        f.write(f"Context: Database\n")
        f.write(f"Test ID: {test_id}\n")
        f.write(f"Description: {description}\n")
        f.write("Test URL:\n")
        f.write("Preconditions:\n - The BirdSites.db database doesn’t exist before starting the test.\n\n")
        f.write("Test Execution Steps:\n")
        for step in steps:
            f.write(f"Step {step['number']}:\n")
            f.write(f"Action: {step['action']}\n")
            f.write(f"Expected Response: {step['expected']}\n\n")
        f.write(f"Expected Response: {expected_response}\n")
        f.write(f"Result: {'Passed' if result else 'Failed'}\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Post-Conditions: The system state remains as expected after running tests.\n")
        f.write(f"Associated Requirements: Jira Task S8S4 The system shall create a database called BirdSites.\n")
        f.write(f"---------------------------------------------\n")
        f.write("\n")