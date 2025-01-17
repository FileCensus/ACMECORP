"""
G Drive Setup Script

This script sets up a standardized directory structure with appropriate NTFS permissions
based on Active Directory groups. It creates a hierarchical folder structure for projects,
departments, and management areas, with proper access controls for different user groups.

The script requires Active Directory groups to be pre-created using create_ad_user.py.

Usage:
    python G_drive_setup.py [options]

Options:
    --dry-run           Show what would be done without making actual changes
    --data-file FILE    Path to company data JSON file (default: company_data.json)
    --base-path PATH    Base path for G drive structure (default: G:)
    --skip-projects     Skip creation of project directories
    --skip-departments  Skip creation of department directories
    --verbose, -v       Enable detailed output during execution

The input JSON file should contain:
- users: Dictionary of user information including department assignments
- projects: Dictionary of project information including project numbers

Directory Structure Created:
    G:/
    ├── Projects/       # Project-specific directories
    ├── Departments/    # Department-specific directories
    ├── Management/     # Management area directories
    └── Shared/         # Shared resources

Example:
    python G_drive_setup.py --dry-run --verbose
    python G_drive_setup.py --base-path /mnt/g --data-file custom_data.json
"""

import os
import json
from pathlib import Path
import win32security
import win32file
import win32con
import win32net
import ntsecuritycon as con
from typing import Dict, List, Set
import argparse

# Define management directory structure and groups
MANAGEMENT_DIRS = {
    "HR": {
        "Group Management",
        "Group Business Users",
        "Group Business Director",
        "Group Business Manager"
    },
    "Finance": {
        "Group Management",
        "Group Finance Team",
        "Group Finance Administrators",
        "Group Accounting Team",
        "Group Payroll Team",
        "Group Treasury Team",
        "Group Budget Team"
    },
    "IT": {
        "Group Management",
        "Group Infrastructure Team",
        "Group Infrastructure Administrators",
        "Group Security Team"
    },
    "Engineering": {
        "Group Management",
        "Group Development",
        "Group Senior Developers",
        "Group Developers"
    },
    "Operations": {
        "Group Management",
        "Group Infrastructure Team"
    },
    "Strategy": {
        "Group Management",
        "Group Executive",
        "Group Director",
        "Group Manager"
    },
    "Reports": {
        "Group Management",
        "Group Executive",
        "Group Director",
        "Group Manager"
    }
}

def load_company_data(file_path: str) -> Dict:
    """Load the company data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_security_descriptor(path: str) -> win32security.SECURITY_DESCRIPTOR:
    """Get security descriptor for a path"""
    return win32security.GetFileSecurity(
        str(path), 
        win32security.DACL_SECURITY_INFORMATION
    )

def set_security_descriptor(path: str, sd: win32security.SECURITY_DESCRIPTOR) -> None:
    """Set security descriptor for a path"""
    win32security.SetFileSecurity(
        str(path),
        win32security.DACL_SECURITY_INFORMATION,
        sd
    )

def add_ace_to_dacl(dacl: win32security.ACL, group_name: str, access_mask: int,
                    inheritance_flags: int) -> None:
    """Add access control entry to DACL for a group"""
    try:
        # Check if group exists
        try:
            win32net.NetLocalGroupGetInfo(None, group_name, 0)
        except win32net.error:
            print(f"Warning: Group {group_name} does not exist - please run create_ad_user.py first")
            return
        
        # Get the SID for the group
        group_sid = win32security.LookupAccountName(None, group_name)[0]
        # Add the ACE directly to the DACL
        dacl.AddAccessAllowedAceEx(
            win32security.ACL_REVISION,
            inheritance_flags,
            access_mask,
            group_sid
        )
        
    except Exception as e:
        print(f"Warning: Could not add ACE for {group_name}: {str(e)}")

def setup_folder_permissions(path: Path, groups: Dict[str, int], dry_run: bool = False) -> None:
    """Set up NTFS permissions for a folder"""
    try:
        if dry_run:
            print(f"[DRY RUN] Would create folder: {path}")
            print(f"[DRY RUN] Would set permissions for groups:")
            print(f"[DRY RUN]   - Administrators: Full Control")
            for group_name, access_mask in groups.items():
                print(f"[DRY RUN]   - {group_name}: {access_mask}")
            return

        # Create folder if it doesn't exist
        path.mkdir(parents=True, exist_ok=True)

        # Get security descriptor
        sd = win32security.GetNamedSecurityInfo(
            str(path), 
            win32security.SE_FILE_OBJECT,
            win32security.DACL_SECURITY_INFORMATION
        )
        
        # Create new DACL
        dacl = win32security.ACL()
        
        # Set up inheritance flags
        inheritance_flags = (
            win32security.OBJECT_INHERIT_ACE |     # Inherit to files
            win32security.CONTAINER_INHERIT_ACE     # Inherit to folders
        )
        
        # Add Administrators with full control first
        add_ace_to_dacl(dacl, "Administrators", con.FILE_ALL_ACCESS, inheritance_flags)

        # Add each group with their specified permissions
        for group_name, access_mask in groups.items():
            add_ace_to_dacl(dacl, group_name, access_mask, inheritance_flags)

        # Apply the security descriptor with the new DACL
        win32security.SetNamedSecurityInfo(
            str(path),
            win32security.SE_FILE_OBJECT,
            win32security.DACL_SECURITY_INFORMATION,
            None,  # Owner SID (no change)
            None,  # Group SID (no change)
            dacl,  # DACL
            None   # SACL
        )
        
        print(f"Set permissions for: {path}")

    except Exception as e:
        print(f"Error setting permissions for {path}: {str(e)}")
        raise  # Re-raise to see full error details

def setup_g_drive(company_data: Dict, base_path: str = "G:", dry_run: bool = False, 
                 skip_projects: bool = False, skip_departments: bool = False) -> None:
    """Set up G drive structure with proper permissions"""
    # Get unique departments from user data
    departments = {user['department'] for user in company_data['users'].values() 
                  if user.get('department')}
    print(f"\nFound departments: {sorted(departments)}")
    
    base = Path(base_path)
    
    # Define standard permission masks
    FULL_CONTROL = con.FILE_ALL_ACCESS
    MODIFY = (con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE | 
             con.FILE_GENERIC_EXECUTE | con.DELETE)
    READ_EXECUTE = con.FILE_GENERIC_READ | con.FILE_GENERIC_EXECUTE
    
    print(f"\nSetting up base directory structure in {base}")
    
    # Verify project numbers before starting
    project_numbers = {p.get('number') for p in company_data['projects'].values()}
    if not all(project_numbers):
        raise ValueError("Some projects are missing project numbers")
    print(f"Found {len(project_numbers)} valid project numbers")

    # Create main directory structure
    directories = {
        "Projects": {
            "Group Management": FULL_CONTROL
        },
        "Departments": {
            "Group Management": FULL_CONTROL
        },
        "Management": {
            "Group Management": FULL_CONTROL
        },
        "Shared": {
            "Group Management": FULL_CONTROL
        }
    }

    # Set up base directories
    for dir_name, groups in directories.items():
        setup_folder_permissions(base / dir_name, groups, dry_run)

    if not skip_departments:
        print("\nSetting up department directories...")
        # Set up department directories
        for dept in departments:
            dept_path = base / "Departments" / dept
            dept_groups = {
                "Group Management": FULL_CONTROL,
                f"Group {dept} Users": MODIFY,
                f"Group {dept} Executive": FULL_CONTROL,
                f"Group {dept} Director": FULL_CONTROL,
                f"Group {dept} Manager": MODIFY,
                f"Group {dept} Individual": MODIFY
            }
            setup_folder_permissions(dept_path, dept_groups, dry_run)

    if not skip_projects:
        print("\nSetting up project directories...")
        # Set up project directories
        for project_id, project in company_data.get('projects', {}).items():
            project_number = project.get('number', 'unknown')
            project_path = base / "Projects" / project_number
            
            project_groups = {
                "Group Management": FULL_CONTROL,
                f"Group Project {project_number}": FULL_CONTROL
            }

            print(f"Creating project directory: {project_number}")
            setup_folder_permissions(project_path, project_groups, dry_run)

            # Create standard project subdirectories
            subdirs = ["Documentation", "Source", "Resources", "Deliverables"]
            for subdir in subdirs:
                setup_folder_permissions(project_path / subdir, project_groups, dry_run)

    # Set up management directories
    print("\nSetting up management directories...")
    for dir_name, groups in MANAGEMENT_DIRS.items():
        dir_path = base / "Management" / dir_name
        dir_groups = {group: FULL_CONTROL for group in groups}
        print(f"Creating management directory: {dir_name} with {len(groups)} group permissions")
        setup_folder_permissions(dir_path, dir_groups, dry_run)

def main():
    parser = argparse.ArgumentParser(description='Set up G drive structure with proper permissions')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be done without making changes')
    parser.add_argument('--data-file', default='company_data.json',
                       help='Path to company data JSON file')
    parser.add_argument('--base-path', default='G:',
                       help='Base path for G drive structure (default: G:)')
    parser.add_argument('--skip-projects', action='store_true',
                       help='Skip creation of project directories')
    parser.add_argument('--skip-departments', action='store_true',
                       help='Skip creation of department directories')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    args = parser.parse_args()

    try:
        # Load company data
        company_data = load_company_data(args.data_file)
        
        if args.verbose:
            print(f"\nLoaded company data from {args.data_file}:")
            print(f"Users: {len(company_data['users'])}")
            print(f"Projects: {len(company_data['projects'])}")
        
        print("\nChecking for required groups...")
        required_groups = set()
        
        # Collect all required groups
        for groups in MANAGEMENT_DIRS.values():
            required_groups.update(groups)
        
        # Check each group exists
        missing_groups = []
        for group in required_groups:
            try:
                if not args.dry_run:
                    win32net.NetLocalGroupGetInfo(None, group, 0)
            except win32net.error:
                missing_groups.append(group)
        
        if missing_groups:
            print("\nWarning: The following groups are missing:")
            for group in sorted(missing_groups):
                print(f"  - {group}")
            print("\nPlease run create_ad_user.py first to create all required groups")
            if not args.dry_run:
                return
        
        # Verify we have the required data
        if 'users' not in company_data or 'projects' not in company_data:
            raise ValueError("company_data.json is missing required user or project data")
        
        # Set up G drive structure
        print("\nSetting up G drive structure...")
        
        base_path = args.base_path
        if base_path == 'G:' and not Path('G:').exists():
            print("Note: G: drive not available, creating in current directory as G_Drive")
            base_path = 'G_Drive'
            
        setup_g_drive(company_data, base_path, args.dry_run, 
                     args.skip_projects, args.skip_departments)
        
        if args.verbose and not args.dry_run:
            print("\nVerifying directory structure...")
            base = Path(base_path)
            
            # Verify project directories
            if not args.skip_projects:
                projects_dir = base / "Projects"
                if projects_dir.exists():
                    project_count = len(list(projects_dir.glob('P*')))
                    print(f"Found {project_count} project directories")
                else:
                    print("Warning: Projects directory not found")
            
            # Verify department directories
            if not args.skip_departments:
                dept_dir = base / "Departments"
                if dept_dir.exists():
                    dept_count = len(list(dept_dir.glob('*')))
                    print(f"Found {dept_count} department directories")
                else:
                    print("Warning: Departments directory not found")
        
        print("\nG drive setup completed successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if "No mapping between account names and security IDs" in str(e):
            print("\nThis error usually means the required groups don't exist.")
            print("Please run the scripts in this order:")
            print("1. cleanup_ad_users.py")
            print("2. create_ad_user.py")
            print("3. setup_g_drive.py")

if __name__ == "__main__":
    main() 