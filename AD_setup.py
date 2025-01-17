"""
Active Directory Setup Script

This script automates the creation of Active Directory users and groups based on a JSON configuration file.
It handles the creation of department-based groups, project groups, and user accounts with appropriate
group memberships and permissions.

Usage:
    python AD_setup.py [options]

Options:
    --dry-run           Show what would be done without making actual changes
    --data-file FILE    Path to company data JSON file (default: company_data.json)
    --verbose, -v       Enable detailed output during execution
    --skip-groups       Skip the creation of AD groups
    --skip-users        Skip the creation of AD users

The input JSON file should contain:
- users: Dictionary of user information including name, role, department, and project assignments
- projects: Dictionary of project information including number, name, department, and assigned users

Example:
    python AD_setup.py --dry-run --verbose
    python AD_setup.py --data-file custom_data.json
"""

import json
from pathlib import Path
import win32security
import win32net
import win32netcon
import win32api
import win32con
from typing import Dict, Optional, Set
import subprocess
import argparse

# Global variables
all_users = {}
all_projects = {}
all_possible_groups = set()

def load_company_data(file_path: str) -> Dict:
    """Load the company data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_ad_group(group_name: str, dry_run: bool = False) -> bool:
    """Create an Active Directory local group if it doesn't exist"""
    global all_users, all_projects
    try:
        # Generate descriptive comment based on group type
        comment = ""
        if group_name.startswith("Group Project"):
            project_number = group_name.split()[-1]
            
            project = None
            for p in all_projects.values():
                if p.get('number') == project_number:
                    project = p
                    break
            
            if project:
                leader_name = 'Unassigned'
                for uid in project['assigned_users']:
                    if uid in all_users and all_users[uid]['level'] in ['Manager', 'Director']:
                        leader_name = all_users[uid]['name']
                        break
                
                comment = (
                    f"{project['name']} ({project_number}). "
                    f"Department: {project['department']}, "
                    f"Budget: ${project['budget']:,}, "
                    f"Quota: {project['quota_gb']}GB. "
                    f"Leader: {leader_name}"
                )
            else:
                comment = f"Project {project_number}"
        elif any(dept in group_name for dept in ['IT', 'Engineering', 'Operations', 'Business', 'Finance']):
            dept = next(d for d in ['IT', 'Engineering', 'Operations', 'Business', 'Finance'] 
                       if d in group_name)
            level = next((l for l in ['Executive', 'Director', 'Manager', 'Individual', 'Users'] 
                         if l in group_name), None)
            if level:
                leader = next((f"{u['name']} ({u['role']})" for u in all_users.values() 
                             if u['department'] == dept and u['level'] == 'Director'), 'Unassigned')
                comment = f"{dept} department {level} group. Director: {leader}"
        elif group_name in [
            'Group Finance Team', 'Group Finance Administrators',
            'Group Accounting Team', 'Group Payroll Team',
            'Group Treasury Team', 'Group Budget Team'
        ]:
            team = group_name.replace('Group ', '').replace(' Team', '')
            leader = next((f"{u['name']} ({u['role']})" for u in all_users.values() 
                         if team.split()[0] in u['role'] and u['level'] == 'Manager'), 'Unassigned')
            comment = f"Finance {team} group. Manager: {leader}"
        else:
            comment = f"Auto-created group for {group_name}"
        
        # Create the group info structure with explicit level 1 info
        group_info = {
            'name': group_name,
            'comment': comment,
        }
        
        if dry_run:
            print(f"[DRY RUN] Would create/update group: {group_name}")
            print(f"[DRY RUN] Comment: {comment}")
            return True
            
        try:
            # Try to create the group
            win32net.NetLocalGroupAdd(None, 1, group_info)
        except win32net.error as e:
            if e.winerror != 2224:  # Group already exists
                raise
            
            # If group exists, update its info
            win32net.NetLocalGroupSetInfo(None, group_name, 1, group_info)
        
        # Verify the group was created with the correct comment
        try:
            created_group = win32net.NetLocalGroupGetInfo(None, group_name, 1)
            if created_group['comment'] != comment:
                print(f"Warning: Group comment mismatch for {group_name}")
                print(f"Expected: {comment}")
                print(f"Got: {created_group['comment']}")
            else:
                print(f"Successfully created/updated group {group_name} with comment")
        except win32net.error as e:
            print(f"Warning: Could not verify group info: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error creating group {group_name}: {str(e)}")
        return False

def get_user_groups(user_data: Dict, company_data: Dict, valid_groups: Set[str]) -> Set[str]:
    """Helper function to get groups for a single user"""
    user_groups = set()
    
    # Add base groups if they exist in valid_groups
    base_groups = {
        'Group Users',
        'Group Authenticated Users'
    }
    user_groups.update(base_groups & valid_groups)
    
    # Department groups - only if department matches
    if user_data['department']:
        dept_user_group = f"Group {user_data['department']} Users"
        dept_level_group = f"Group {user_data['department']} {user_data['level']}"
        if dept_user_group in valid_groups:
            user_groups.add(dept_user_group)
        if dept_level_group in valid_groups:
            user_groups.add(dept_level_group)
    
    # Project-specific groups
    if user_data.get('assigned_projects'):
        for project_id in user_data['assigned_projects']:
            if project_id in company_data.get('projects', {}):
                project = company_data['projects'][project_id]
                project_number = project.get('number', 'unknown')
                project_group = f"Group Project {project_number}"
                if project_group in valid_groups:
                    user_groups.add(project_group)
    
    # Level-based groups
    if user_data['level']:
        level_group = f"Group {user_data['level']}"
        if level_group in valid_groups:
            user_groups.add(level_group)
    
    # Management groups - only for management roles
    if user_data['level'] in ['Executive', 'Director', 'Manager']:
        management_groups = {
            'Group Management',
            'Group Resource Approvers',
            'Group Budget Owners'
        }
        user_groups.update(management_groups & valid_groups)
    
    # Cloud groups - only for cloud tech users
    if any(tech in user_data['current_technologies'] for tech in ['AWS', 'Azure', 'GCP']):
        cloud_groups = {'Group Cloud Users'}
        if user_data['level'] in ['Executive', 'Director', 'Manager']:
            cloud_groups.add('Group Cloud Administrators')
        else:
            cloud_groups.add('Group Cloud Developers')
        user_groups.update(cloud_groups & valid_groups)
    
    # Development groups - only for developers
    if any(role in user_data['role'] for role in ['Developer', 'Engineer']):
        dev_groups = {'Group Development'}
        if 'Senior' in user_data['role']:
            dev_groups.add('Group Senior Developers')
        elif 'Junior' in user_data['role']:
            dev_groups.add('Group Junior Developers')
        else:
            dev_groups.add('Group Developers')
        user_groups.update(dev_groups & valid_groups)
    
    # Security groups - only for security/compliance roles
    if any(tech in user_data['current_technologies'] for tech in ['Security', 'Compliance']):
        security_groups = {'Group Security Team'}
        user_groups.update(security_groups & valid_groups)
    
    # Data groups - only for data-related roles
    if any(tech in user_data['current_technologies'] for tech in ['SQL', 'Python', 'R', 'Data Science']):
        data_groups = {'Group Data Users'}
        if user_data['level'] in ['Manager', 'Director', 'Executive']:
            data_groups.add('Group Data Administrators')
        user_groups.update(data_groups & valid_groups)
    
    # Design groups - only for designers
    if any(tech in user_data['current_technologies'] for tech in ['Adobe Creative Suite', 'UI/UX Design']):
        design_groups = {'Group Design Team'}
        user_groups.update(design_groups & valid_groups)
    
    # Infrastructure groups - only for infrastructure roles
    if any(role in user_data['role'] for role in ['Infrastructure', 'DevOps']):
        infra_groups = {'Group Infrastructure Team'}
        if user_data['level'] in ['Manager', 'Director', 'Executive']:
            infra_groups.add('Group Infrastructure Administrators')
        user_groups.update(infra_groups & valid_groups)
    
    return user_groups

def get_required_groups(company_data: Dict) -> Set[str]:
    """Determine all required groups based on user data"""
    # Define all departments and levels
    departments = {'IT', 'Engineering', 'Operations', 'Business', 'Finance'}
    levels = {'Executive', 'Director', 'Manager', 'Individual'}
    
    # Define all possible technical roles and their groups
    tech_groups = {
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
    }
    
    # Define all finance-related groups
    finance_groups = {
        'Group Finance Team',
        'Group Finance Administrators',
        'Group Accounting Team',
        'Group Payroll Team',
        'Group Treasury Team',
        'Group Budget Team',
    }
    
    # Define management groups
    management_groups = {
        'Group Management',
        'Group Resource Approvers',
        'Group Budget Owners',
    }
    
    # Start with base groups
    all_groups = {
        'Group Users',
        'Group Authenticated Users',
    }
    
    # Add all group types
    all_groups.update(tech_groups)
    all_groups.update(finance_groups)
    all_groups.update(management_groups)
    
    # Add department groups
    for dept in departments:
        all_groups.add(f"Group {dept} Users")
    
    # Add level groups
    for level in levels:
        all_groups.add(f"Group {level}")
    
    # Add department-level combinations
    for dept in departments:
        for level in levels:
            all_groups.add(f"Group {dept} {level}")
    
    return all_groups

def create_ad_user(user_data: Dict, dry_run: bool = False, domain: Optional[str] = None) -> bool:
    """Create an Active Directory user with the specified attributes"""
    name_parts = user_data['name'].lower().split()
    username = f"{name_parts[0]}_{name_parts[-1]}"
    
    try:
        # Create user info structure
        user_info = {
            'name': username,
            'full_name': user_data['true_name'],  # Use unicode true_name for display
            'password': 'Password1',  # Initial password
            'priv': win32netcon.USER_PRIV_USER,
            'home_dir': f'U:\\Users\\{username}',
            'comment': f"{user_data['role']} - {user_data['department']}",
            'flags': (win32netcon.UF_NORMAL_ACCOUNT | 
                     win32netcon.UF_SCRIPT | 
                     win32netcon.UF_DONT_EXPIRE_PASSWD |  # Password never expires
                     win32netcon.UF_PASSWD_CANT_CHANGE),  # User can't change password
            'script_path': ''
        }

        if dry_run:
            print(f"[DRY RUN] Would create user: {username}")
            print(f"[DRY RUN] Full name: {user_data['true_name']}")
            print(f"[DRY RUN] Home directory: U:\\Users\\{username}")
            print(f"[DRY RUN] Comment: {user_data['role']} - {user_data['department']}")
            return True

        # Create the user account
        win32net.NetUserAdd(None, 1, user_info)
        
        # Set password to never expire using net user command
        subprocess.run(['net', 'user', username, '/passwordchg:no'], check=True)
        subprocess.run(['net', 'user', username, '/expires:never'], check=True)
        
        # Set user full name using net user command
        subprocess.run(['net', 'user', username, '/fullname:' + user_data['true_name']], 
                      check=True, encoding='utf-8', errors='replace')
        
        # Get the specific groups this user should be in
        company_data = {
            'projects': all_projects,
            'users': all_users
        }
        groups = get_user_groups(user_data, company_data, all_possible_groups)
        
        # Add user to groups
        for group in groups:
            try:
                win32net.NetLocalGroupAddMembers(None, group, 3, [{'domainandname': username}])
                print(f"Added {username} to group: {group}")
            except win32net.error as e:
                print(f"Warning: Could not add user to group {group}: {str(e)}")
        
        # Set home directory permissions
        home_dir = Path(user_info['home_dir'])
        if not home_dir.exists():
            home_dir.mkdir(parents=True, exist_ok=True)
        
        # Get user's SID
        user_sid = win32security.LookupAccountName(None, username)[0]
        
        # Set home directory permissions
        security_descriptor = win32security.GetFileSecurity(
            str(home_dir), 
            win32security.DACL_SECURITY_INFORMATION
        )
        
        dacl = win32security.ACL()
        dacl.AddAccessAllowedAce(
            win32security.ACL_REVISION,
            # Combine standard file access rights
            win32con.GENERIC_READ | 
            win32con.GENERIC_WRITE | 
            win32con.GENERIC_EXECUTE |
            win32con.DELETE,
            user_sid
        )
        
        security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)
        win32security.SetFileSecurity(
            str(home_dir),
            win32security.DACL_SECURITY_INFORMATION,
            security_descriptor
        )
        
        print(f"Successfully created user {username}")
        return True
        
    except Exception as e:
        print(f"Error creating user {username}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Setup Active Directory users and groups')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--data-file', default='company_data.json', help='Path to company data JSON file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--skip-groups', action='store_true', help='Skip group creation')
    parser.add_argument('--skip-users', action='store_true', help='Skip user creation')
    args = parser.parse_args()

    try:
        # Load company data
        company_data = load_company_data(args.data_file)
        
        # Store all users for manager lookup
        global all_users
        all_users = company_data['users']
        
        # Store all projects for group creation
        global all_projects
        all_projects = company_data.get('projects', {})
        
        if args.verbose:
            if not all_projects:
                print("\nWarning: No projects found in company_data.json")
            else:
                print(f"\nLoaded {len(all_projects)} projects")
        
        # Store all groups that will be created
        global all_possible_groups
        
        # Get list of users we'll create
        all_users_list = list(company_data['users'].items())
        
        if args.verbose:
            print(f"\nWill {'simulate' if args.dry_run else 'create'} {len(all_users_list)} users and their associated groups...")
        
        if not args.skip_groups:
            # Create required groups first
            if args.verbose:
                print("\nCreating required groups...")
            required_groups = get_required_groups(company_data)
            all_possible_groups = required_groups.copy()
            
            # Add project groups
            if args.verbose:
                print("\nCollecting project groups...")
            for project_id, project in all_projects.items():
                project_number = project.get('number', 'unknown')
                project_group = f"Group Project {project_number}"
                all_possible_groups.add(project_group)
                if args.verbose:
                    print(f"  Added {project_group}")
            
            if args.verbose:
                print(f"\nTotal groups to {'simulate' if args.dry_run else 'create'}: {len(all_possible_groups)}")
            
            for group in all_possible_groups:
                if create_ad_group(group, dry_run=args.dry_run):
                    if args.verbose:
                        print(f"Successfully {'simulated' if args.dry_run else 'created'} group: {group}")
                else:
                    print(f"Failed to {'simulate' if args.dry_run else 'create'} group: {group}")
        
        if not args.skip_users:
            # Create users
            if args.verbose:
                print("\nCreating users...")
            success_count = 0
            for user_id, user_data in all_users_list:
                if create_ad_user(user_data, dry_run=args.dry_run):
                    success_count += 1
            
            if args.verbose:
                print(f"\n{'Simulated' if args.dry_run else 'Created'} {success_count} of {len(all_users_list)} users successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 