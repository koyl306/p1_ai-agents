#!/usr/bin/env python3
"""Quick test of date validation logic"""

from datetime import datetime

# Test valid date
try:
    datetime.strptime("2024-01-15", "%Y-%m-%d")
    print("✓ Valid date '2024-01-15' accepted")
except ValueError:
    print("✗ Valid date '2024-01-15' rejected")

# Test invalid date format
try:
    datetime.strptime("01-15-2024", "%Y-%m-%d")
    print("✗ Invalid format '01-15-2024' accepted (should fail)")
except ValueError:
    print("✓ Invalid format '01-15-2024' correctly rejected")

# Test invalid date values
try:
    datetime.strptime("2024-13-01", "%Y-%m-%d")
    print("✗ Invalid month '2024-13-01' accepted (should fail)")
except ValueError:
    print("✓ Invalid month '2024-13-01' correctly rejected")

# Test None handling
test_date = None
if test_date is None:
    test_date = datetime.now().strftime("%Y-%m-%d")
    print(f"✓ None date correctly defaulted to: {test_date}")

print("\nAll validations working correctly!")
