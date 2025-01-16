#!/usr/bin/env python3
"""
Active Directory Cleanup Script

This script removes Active Directory users and groups created by the company simulation.
It provides options for dry-run execution, selective cleanup (users or groups only),
and verbose output.

Usage:
    python AD_cleanup.py [options]

Options:
    --dry-run, -n    Show what would be deleted without making changes
    --verbose, -v    Show detailed progress
    --users-only     Only delete users, keep groups
    --groups-only    Only delete groups, keep users
    --file, -f       Path to company data JSON file (default: company_data.json)

Example:
    python AD_cleanup.py --dry-run
    python AD_cleanup.py --verbose --users-only
    python AD_cleanup.py --file other_company.json

Author: https://github.com/scott91e1

Dependencies:
    - win32net: Windows API access for AD operations
    - json: JSON file handling
    - argparse: Command line argument parsing

This script is part of the ACMECORP Company Data Simulation toolkit.
"""

import json
import win32net
from pathlib import Path
from typing import Dict, List, Set
import argparse
import sys

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Cleanup Active Directory users and groups created by the simulation.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --dry-run                     # Show what would be deleted without making changes
  %(prog)s --verbose                     # Show detailed progress
  %(prog)s --users-only                  # Only delete users
  %(prog)s --groups-only                 # Only delete groups
  %(prog)s --file other_company.json     # Use alternative company data file
'''
    )
    
    parser.add_argument('--dry-run', '-n', action='store_true',
                      help='Show what would be deleted without making changes')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Show detailed progress')
    parser.add_argument('--users-only', action='store_true',
                      help='Only delete users, keep groups')
    parser.add_argument('--groups-only', action='store_true',
                      help='Only delete groups, keep users')
    parser.add_argument('--file', '-f', type=str, default='company_data.json',
                      help='Path to company data JSON file (default: company_data.json)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.users_only and args.groups_only:
        parser.error("Cannot specify both --users-only and --groups-only")
    
    return args

def load_company_data(file_path: str) -> Dict:
    """Load the company data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Company data file not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in company data file: {file_path}")
        sys.exit(1)

def delete_user(username: str, dry_run: bool = False, verbose: bool = False) -> bool:
    """Delete a local user if they exist
    
    Args:
        username: The username to delete
        dry_run: If True, only show what would be deleted
        verbose: If True, show detailed progress
        
    Returns:
        bool: True if user was deleted or didn't exist, False if error occurred
    """
    try:
        try:
            # Check if user exists
            win32net.NetUserGetInfo(None, username, 0)
            if dry_run:
                print(f"Would delete user: {username}")
                return True
            # User exists, attempt to delete them
            win32net.NetUserDel(None, username)
            print(f"Deleted user: {username}")
            return True
        except win32net.error:
            if verbose:
                print(f"User not found: {username}")
            return False
    except Exception as e:
        print(f"Error {'checking' if dry_run else 'deleting'} user {username}: {str(e)}")
        return False

def delete_group(group_name: str, dry_run: bool = False, verbose: bool = False) -> bool:
    """Delete a local group if it exists
    
    Args:
        group_name: The name of the group to delete
        dry_run: If True, only show what would be deleted
        verbose: If True, show detailed progress
        
    Returns:
        bool: True if group was deleted or didn't exist, False if error occurred
    """
    try:
        try:
            # Check if group exists
            win32net.NetLocalGroupGetInfo(None, group_name, 0)
            if dry_run:
                print(f"Would delete group: {group_name}")
                return True
            # Group exists, attempt to delete it
            win32net.NetLocalGroupDel(None, group_name)
            print(f"Deleted group: {group_name}")
            return True
        except win32net.error:
            if verbose:
                print(f"Group not found: {group_name}")
            return False
    except Exception as e:
        print(f"Error {'checking' if dry_run else 'deleting'} group {group_name}: {str(e)}")
        return False

def get_all_group_names(company_data: Dict) -> Set[str]:
    """Get all possible group names from company data
    
    Args:
        company_data: Dictionary containing company structure and project data
        
    Returns:
        Set[str]: Set of all possible group names that could exist
        
    This function generates a comprehensive list of all possible groups that
    could have been created by the simulation, including:
    - Base groups (Users, Authenticated Users, etc.)
    - Department groups
    - Level groups (Executive, Director, etc.)
    - Department-Level combination groups
    - Technical groups
    - Finance groups
    - Project-specific groups
    """
    # Define all possible departments and levels
    departments = {'IT', 'Engineering', 'Operations', 'Business', 'Finance'}
    levels = {'Executive', 'Director', 'Manager', 'Individual'}
    
    # Build comprehensive set of groups
    groups = {
        # Base groups for general access
        'Group Users',
        'Group Authenticated Users',
        'Group Management',
        'Group Resource Approvers',
        'Group Budget Owners',
        
        # Department-specific groups
        'Group IT Users',
        'Group Engineering Users',
        'Group Operations Users',
        'Group Business Users',
        'Group Finance Users',
        
        # Level-specific groups
        'Group Executive',
        'Group Director',
        'Group Manager',
        'Group Individual',
        
        # Generate all possible department-level combinations
        *(f"Group {dept} {level}" for dept in departments for level in levels),
        
        # Technical role groups
        'Group Cloud Users',
        'Group Cloud Administrators',
        'Group Cloud Developers',
        'Group Development',
        'Group Senior Developers',
        'Group Junior Developers',
        'Group Developers',
        'Group Security Team',
        'Group Data Users',
        'Group Data Administrators',
        'Group Design Team',
        'Group Infrastructure Team',
        'Group Infrastructure Administrators',
        
        # Finance-specific groups
        'Group Finance Team',
        'Group Finance Administrators',
        'Group Accounting Team',
        'Group Payroll Team',
        'Group Treasury Team',
        'Group Budget Team',
    }
    
    # Add project-specific groups
    for project in company_data['projects'].values():
        project_number = project.get('number', 'unknown')
        groups.add(f"Group Project {project_number}")
    
    return groups

def main():
    """Main function to clean up users and groups"""
    args = parse_arguments()
    
    try:
        if args.dry_run:
            print("\nDRY RUN - No changes will be made")
        
        print(f"\nLoading company data from {args.file}...")
        company_data = load_company_data(args.file)
        
        users_deleted = 0
        groups_deleted = 0
        
        # Delete users if not groups-only
        if not args.groups_only:
            print("\nProcessing users...")
            for user_data in company_data['users'].values():
                name_parts = user_data['name'].lower().split()
                username = f"{name_parts[0]}_{name_parts[-1]}"
                if delete_user(username, args.dry_run, args.verbose):
                    users_deleted += 1
        
        # Delete groups if not users-only
        if not args.users_only:
            print("\nProcessing groups...")
            groups = get_all_group_names(company_data)
            for group in groups:
                if delete_group(group, args.dry_run, args.verbose):
                    groups_deleted += 1
        
        # Print summary
        print(f"\nCleanup {'simulation' if args.dry_run else 'operation'} complete:")
        if not args.groups_only:
            print(f"- Users {'would be' if args.dry_run else ''} deleted: {users_deleted}")
            print(f"- Total users processed: {len(company_data['users'])}")
        if not args.users_only:
            print(f"- Groups {'would be' if args.dry_run else ''} deleted: {groups_deleted}")
        
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 