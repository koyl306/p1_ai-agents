#!/usr/bin/env python3
"""
Test the new 'list' command with various filter combinations
"""

import json
import os
import sys
sys.path.insert(0, '.')

from expense_tracker import display_expenses, filter_expenses

# Create sample expenses data
sample_expenses = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "date": "2024-01-10",
        "category": "Food",
        "amount": 25.50,
        "description": "Lunch at Italian restaurant"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "date": "2024-01-15",
        "category": "Transport",
        "amount": 10.00,
        "description": "Bus fare"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "date": "2024-01-20",
        "category": "Food",
        "amount": 35.00,
        "description": "Dinner with friends"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440004",
        "date": "2024-02-05",
        "category": "Food",
        "amount": 15.50,
        "description": "Breakfast"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440005",
        "date": "2024-02-10",
        "category": "Transport",
        "amount": 20.00,
        "description": "Taxi ride downtown"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440006",
        "date": "2024-02-15",
        "category": "Entertainment",
        "amount": 50.00,
        "description": "Movie tickets and popcorn"
    },
]

print("=" * 85)
print("TEST: Display Expenses Function")
print("=" * 85)

# TEST 1: Display all expenses
print("\n[TEST 1] Display all expenses:")
display_expenses(sample_expenses)

# TEST 2: Display expenses filtered by category
print("\n[TEST 2] Filter by category='Food':")
filtered = filter_expenses(sample_expenses, category="Food")
display_expenses(filtered)

# TEST 3: Display expenses filtered by date range
print("\n[TEST 3] Filter by date range [2024-01-15 to 2024-02-05]:")
filtered = filter_expenses(sample_expenses, start_date="2024-01-15", end_date="2024-02-05")
display_expenses(filtered)

# TEST 4: Display expenses with both category and date range filters
print("\n[TEST 4] Filter by category='Food' AND date range [2024-01-01 to 2024-01-31]:")
filtered = filter_expenses(sample_expenses, category="Food", 
                          start_date="2024-01-01", end_date="2024-01-31")
display_expenses(filtered)

# TEST 5: Display expenses with start_date only
print("\n[TEST 5] Filter by start_date='2024-02-01' (from Feb onwards):")
filtered = filter_expenses(sample_expenses, start_date="2024-02-01")
display_expenses(filtered)

# TEST 6: Display expenses with end_date only
print("\n[TEST 6] Filter by end_date='2024-01-31' (up to end of January):")
filtered = filter_expenses(sample_expenses, end_date="2024-01-31")
display_expenses(filtered)

# TEST 7: Display expenses with no matches
print("\n[TEST 7] Filter by category='Utilities' (no matches):")
filtered = filter_expenses(sample_expenses, category="Utilities")
display_expenses(filtered)

# TEST 8: Display expenses in empty date range
print("\n[TEST 8] Filter by date range [2024-03-01 to 2024-03-31] (empty range):")
filtered = filter_expenses(sample_expenses, start_date="2024-03-01", end_date="2024-03-31")
display_expenses(filtered)

print("\n" + "=" * 85)
print("✓ All display tests completed successfully!")
print("=" * 85)

# CLI Usage Examples
print("\n" + "=" * 85)
print("CLI Usage Examples:")
print("=" * 85)
print("""
# Display all expenses
python3 expense_tracker.py list

# Display expenses for a specific category
python3 expense_tracker.py list --category Food

# Display expenses within a date range
python3 expense_tracker.py list --start-date 2024-01-15 --end-date 2024-02-05

# Display expenses for a specific category within a date range
python3 expense_tracker.py list --category Food --start-date 2024-01-01 --end-date 2024-01-31

# Display expenses from a specific date onwards
python3 expense_tracker.py list --start-date 2024-02-01

# Display expenses up to a specific date
python3 expense_tracker.py list --end-date 2024-01-31
""")
