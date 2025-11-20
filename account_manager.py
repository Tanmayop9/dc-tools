#!/usr/bin/env python3
"""
Account Manager - Manage created Discord accounts
Features: List accounts, validate tokens, export data
"""

import sqlite3
import requests
import json
from datetime import datetime
from pathlib import Path

class AccountManager:
    def __init__(self, db_file='accounts.db'):
        self.db_file = db_file
        self.discord_api = "https://discord.com/api/v9"
    
    def list_accounts(self, status=None):
        """List all accounts or filter by status"""
        if not Path(self.db_file).exists():
            print("No database found. Create accounts first.")
            return
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('SELECT * FROM accounts WHERE status = ?', (status,))
        else:
            cursor.execute('SELECT * FROM accounts')
        
        accounts = cursor.fetchall()
        conn.close()
        
        if not accounts:
            print("No accounts found.")
            return
        
        print(f"\n{'='*80}")
        print(f"{'ID':<5} {'Email':<30} {'Username':<20} {'Verified':<10} {'Status':<10}")
        print(f"{'='*80}")
        
        for account in accounts:
            id_, email, username, password, token, created, verified, status = account
            verified_str = "Yes" if verified else "No"
            print(f"{id_:<5} {email:<30} {username:<20} {verified_str:<10} {status:<10}")
        
        print(f"{'='*80}")
        print(f"Total: {len(accounts)} accounts\n")
    
    def validate_all_tokens(self):
        """Validate all tokens in database"""
        if not Path(self.db_file).exists():
            print("No database found.")
            return
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, token FROM accounts')
        accounts = cursor.fetchall()
        
        print(f"\nValidating {len(accounts)} tokens...\n")
        
        valid_count = 0
        invalid_count = 0
        
        for id_, token in accounts:
            try:
                headers = {'Authorization': token}
                response = requests.get(f'{self.discord_api}/users/@me', headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"[✓] Account {id_}: Valid")
                    cursor.execute('UPDATE accounts SET status = ? WHERE id = ?', ('active', id_))
                    valid_count += 1
                else:
                    print(f"[✗] Account {id_}: Invalid (Status: {response.status_code})")
                    cursor.execute('UPDATE accounts SET status = ? WHERE id = ?', ('invalid', id_))
                    invalid_count += 1
            except Exception as e:
                print(f"[✗] Account {id_}: Error - {e}")
                invalid_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"\n{'='*80}")
        print(f"Validation complete: {valid_count} valid, {invalid_count} invalid")
        print(f"{'='*80}\n")
    
    def export_tokens(self, filename='exported_tokens.txt'):
        """Export all valid tokens to file"""
        if not Path(self.db_file).exists():
            print("No database found.")
            return
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT token FROM accounts WHERE status = ?', ('active',))
        tokens = cursor.fetchall()
        conn.close()
        
        with open(filename, 'w') as f:
            for token, in tokens:
                f.write(f"{token}\n")
        
        print(f"[✓] Exported {len(tokens)} tokens to {filename}")
    
    def export_json(self, filename='accounts_export.json'):
        """Export accounts to JSON"""
        if not Path(self.db_file).exists():
            print("No database found.")
            return
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts')
        accounts = cursor.fetchall()
        conn.close()
        
        data = []
        for account in accounts:
            id_, email, username, password, token, created, verified, status = account
            data.append({
                'id': id_,
                'email': email,
                'username': username,
                'password': password,
                'token': token,
                'created_at': created,
                'verified': bool(verified),
                'status': status
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[✓] Exported {len(data)} accounts to {filename}")
    
    def get_statistics(self):
        """Show account statistics"""
        if not Path(self.db_file).exists():
            print("No database found.")
            return
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Total accounts
        cursor.execute('SELECT COUNT(*) FROM accounts')
        total = cursor.fetchone()[0]
        
        # Verified accounts
        cursor.execute('SELECT COUNT(*) FROM accounts WHERE verified = 1')
        verified = cursor.fetchone()[0]
        
        # Active accounts
        cursor.execute('SELECT COUNT(*) FROM accounts WHERE status = ?', ('active',))
        active = cursor.fetchone()[0]
        
        # Invalid accounts
        cursor.execute('SELECT COUNT(*) FROM accounts WHERE status = ?', ('invalid',))
        invalid = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"\n{'='*60}")
        print("Account Statistics")
        print(f"{'='*60}")
        print(f"Total Accounts:    {total}")
        print(f"Verified:          {verified} ({verified/total*100:.1f}%)" if total > 0 else "Verified: 0")
        print(f"Active:            {active} ({active/total*100:.1f}%)" if total > 0 else "Active: 0")
        print(f"Invalid:           {invalid} ({invalid/total*100:.1f}%)" if total > 0 else "Invalid: 0")
        print(f"{'='*60}\n")
    
    def delete_invalid(self):
        """Delete invalid accounts from database"""
        if not Path(self.db_file).exists():
            print("No database found.")
            return
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM accounts WHERE status = ?', ('invalid',))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"[✓] Deleted {deleted} invalid accounts")

def show_menu():
    """Display menu"""
    print("\n" + "="*60)
    print("Discord Account Manager")
    print("="*60)
    print("1. List all accounts")
    print("2. List active accounts")
    print("3. Validate all tokens")
    print("4. Export valid tokens")
    print("5. Export to JSON")
    print("6. Show statistics")
    print("7. Delete invalid accounts")
    print("8. Exit")
    print("="*60)

def main():
    """Main entry point"""
    manager = AccountManager()
    
    while True:
        show_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            manager.list_accounts()
        elif choice == '2':
            manager.list_accounts(status='active')
        elif choice == '3':
            manager.validate_all_tokens()
        elif choice == '4':
            filename = input("Export filename (default: exported_tokens.txt): ").strip()
            manager.export_tokens(filename if filename else 'exported_tokens.txt')
        elif choice == '5':
            filename = input("Export filename (default: accounts_export.json): ").strip()
            manager.export_json(filename if filename else 'accounts_export.json')
        elif choice == '6':
            manager.get_statistics()
        elif choice == '7':
            confirm = input("Delete all invalid accounts? (yes/no): ").strip().lower()
            if confirm == 'yes':
                manager.delete_invalid()
        elif choice == '8':
            print("\nGoodbye!")
            break
        else:
            print("[✗] Invalid option")

if __name__ == "__main__":
    main()
