import json
import os
from datetime import datetime, timedelta

# Local storage for recurring expenses
RECURRING_DIR = "recurring_expenses"

if not os.path.exists(RECURRING_DIR):
    os.makedirs(RECURRING_DIR, exist_ok=True)


def _get_recurring_file(username):
    return os.path.join(RECURRING_DIR, f"{username}.json")


def get_recurring_expenses(username):
    """Get all recurring expenses for a user"""
    filepath = _get_recurring_file(username)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []


def save_recurring_expenses(username, recurring_list):
    """Save recurring expenses for a user"""
    filepath = _get_recurring_file(username)
    with open(filepath, 'w') as f:
        json.dump(recurring_list, f, indent=4)


def add_recurring_expense(username, amount, category, description, frequency, start_date):
    """
    Add a recurring expense
    frequency: 'daily', 'weekly', 'monthly', 'yearly'
    """
    import uuid
    recurring = get_recurring_expenses(username)
    new_expense = {
        'id': str(uuid.uuid4()),
        'user_id': username,
        'amount': amount,
        'category': category,
        'description': description,
        'frequency': frequency,
        'start_date': start_date,
        'active': True,
        'created_at': datetime.now().isoformat()
    }
    recurring.append(new_expense)
    save_recurring_expenses(username, recurring)
    return new_expense


def delete_recurring_expense(username, expense_id):
    """Delete a recurring expense"""
    recurring = get_recurring_expenses(username)
    original_len = len(recurring)
    recurring = [r for r in recurring if r.get('id') != expense_id]
    if len(recurring) < original_len:
        save_recurring_expenses(username, recurring)
        return True
    return False


def toggle_recurring_expense(username, expense_id, active):
    """Enable/disable a recurring expense"""
    recurring = get_recurring_expenses(username)
    for r in recurring:
        if r.get('id') == expense_id:
            r['active'] = active
            break
    save_recurring_expenses(username, recurring)


def get_next_occurrence(start_date, frequency):
    """Calculate next occurrence date"""
    try:
        date = datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        # Fallback for other formats or if start_date is empty
        date = datetime.now()
        
    today = datetime.now().date()
    
    if frequency == 'daily':
        while date.date() <= today:
            date += timedelta(days=1)
    elif frequency == 'weekly':
        while date.date() <= today:
            date += timedelta(weeks=1)
    elif frequency == 'monthly':
        while date.date() <= today:
            month = date.month + 1
            year = date.year
            if month > 12:
                month = 1
                year += 1
            try:
                date = date.replace(month=month, year=year)
            except ValueError:
                # Handle day 31 in months with fewer days
                date = date.replace(month=month, year=year, day=28)
    elif frequency == 'yearly':
        while date.date() <= today:
            date = date.replace(year=date.year + 1)
    
    return date.strftime('%Y-%m-%d')


def process_recurring_expenses(username, expenses_list):
    """
    Process recurring expenses for the user
    This should be called periodically to auto-create expenses
    """
    recurring = get_recurring_expenses(username)
    today = datetime.now().strftime('%Y-%m-%d')
    added_count = 0
    
    for rec in recurring:
        if not rec['active']:
            continue
        
        next_date = get_next_occurrence(rec['start_date'], rec['frequency'])
        
        # Check if an expense already exists for this recurring item on this date
        existing = [e for e in expenses_list if 
                   e.get('date') == next_date and 
                   e.get('category') == rec['category'] and
                   e.get('amount') == rec['amount']]
        
        if not existing and next_date <= today:
            # Auto-create the expense
            from .expense import Expense
            new_exp = Expense(rec['amount'], rec['category'], rec['description'], next_date)
            expense_dict = new_exp.to_dict()
            # No Firebase: the caller will save the expenses_list
            expenses_list.append(expense_dict)
            added_count += 1
    
    return added_count
