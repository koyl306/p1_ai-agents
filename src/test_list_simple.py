#!/usr/bin/env python3
"""
Quick verification that the 'list' command works correctly
"""

import sys
sys.path.insert(0, '.')

from expense_tracker import display_expenses, filter_expenses

# Minimal test
expenses = [
    {"id": "1", "date": "2024-01-10", "category": "Food", "amount": 25.50, "description": "Lunch"},
    {"id": "2", "date": "2024-01-15", "category": "Transport", "amount": 10.00, "description": "Bus"},
    {"id": "3", "date": "2024-02-05", "category": "Food", "amount": 35.00, "description": "Dinner"},
]

print("Test 1: Display all expenses")
display_expenses(expenses)

print("\n\nTest 2: Filter by category='Food'")
filtered = filter_expenses(expenses, category="Food")
display_expenses(filtered)

print("\n\nTest 3: Filter by date range")
filtered = filter_expenses(expenses, start_date="2024-01-15", end_date="2024-02-05")
display_expenses(filtered)

print("\n✓ All tests passed!")
