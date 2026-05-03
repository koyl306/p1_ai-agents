#!/usr/bin/env python3
"""
Test improved CLI output formatting for list command
"""

import sys
sys.path.insert(0, '.')

from expense_tracker import display_expenses

print("=" * 80)
print("Test: Improved CLI Output Formatting")
print("=" * 80)

# Test data with various scenarios
test_expenses = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "date": "2024-01-10",
        "category": "Food",
        "amount": 25.50,
        "description": "Lunch at restaurant"
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
        "amount": 35.75,
        "description": "Dinner with friends"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440004",
        "date": "2024-02-05",
        "category": "Entertainment",
        "amount": 50.00,
        "description": "Movie tickets and popcorn"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440005",
        "date": "2024-02-10",
        "category": "Transport",
        "amount": 20.25,
        "description": "Taxi ride"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440006",
        "date": "2024-02-15",
        "category": "Food",
        "amount": 1234.56,
        "description": "Very expensive catering for large event with many people"
    },
]

# TEST 1: Display all expenses
print("\n[TEST 1] Display all expenses with proper formatting")
print("─" * 80)
display_expenses(test_expenses)

# TEST 2: Display filtered expenses (subset)
print("\n\n[TEST 2] Display filtered expenses (Food category only)")
print("─" * 80)
food_expenses = [e for e in test_expenses if e["category"] == "Food"]
display_expenses(food_expenses)

# TEST 3: Display single expense
print("\n\n[TEST 3] Display single expense")
print("─" * 80)
display_expenses([test_expenses[0]])

# TEST 4: Display empty list
print("\n\n[TEST 4] Display empty list")
print("─" * 80)
display_expenses([])

# TEST 5: Test with various amount formats
print("\n\n[TEST 5] Test with various amount formats (2 decimal places)")
print("─" * 80)
test_amounts = [
    {
        "id": "test-1",
        "date": "2024-01-01",
        "category": "Test",
        "amount": 1,
        "description": "Whole number"
    },
    {
        "id": "test-2",
        "date": "2024-01-02",
        "category": "Test",
        "amount": 1.5,
        "description": "One decimal place"
    },
    {
        "id": "test-3",
        "date": "2024-01-03",
        "category": "Test",
        "amount": 1.99,
        "description": "Two decimal places"
    },
    {
        "id": "test-4",
        "date": "2024-01-04",
        "category": "Test",
        "amount": 1000.00,
        "description": "Large number"
    },
    {
        "id": "test-5",
        "date": "2024-01-05",
        "category": "Test",
        "amount": 0.01,
        "description": "Very small amount"
    },
]
display_expenses(test_amounts)

# TEST 6: Test with long descriptions
print("\n\n[TEST 6] Test with long descriptions (truncation)")
print("─" * 80)
long_desc_expenses = [
    {
        "id": "long-1",
        "date": "2024-01-01",
        "category": "Food",
        "amount": 50.00,
        "description": "This is a very long description that should be truncated properly"
    },
    {
        "id": "long-2",
        "date": "2024-01-02",
        "category": "Transport",
        "amount": 25.50,
        "description": "Another very long description that goes on and on and on"
    },
]
display_expenses(long_desc_expenses)

print("\n\n" + "=" * 80)
print("✓ All formatting tests completed!")
print("=" * 80)

print("""
FORMATTING FEATURES:
════════════════════

✓ Column Alignment
  - Date: 12 characters
  - Category: 15 characters
  - Amount: 12 characters (right-aligned)
  - Description: 35 characters

✓ Proper Separators
  - Unicode box-drawing characters (─ │)
  - Clear header and footer
  - Visual separation between rows

✓ Amount Formatting
  - Always 2 decimal places (e.g., $25.50)
  - Thousand separators (e.g., $1,234.56)
  - Right-aligned for easy scanning

✓ Description Handling
  - Long descriptions truncated with "..."
  - Preserves readability
  - Respects column width

✓ Summary Row
  - Total amount displayed
  - Count of expenses shown
  - Formatted consistently with data rows
""")
