# ACMECORPCompany Data Simulation Scripts

## Overview
This project provides a comprehensive suite of tools for simulating a realistic corporate file system environment. It's designed to help developers, system administrators, and IT professionals test and develop file system management tools, storage analysis software, and data governance solutions in a safe, controlled environment that mirrors real-world corporate data structures.

### Key Features
- **Realistic User Data**: Generates a diverse set of synthetic users with appropriate roles, departments, and reporting structures
- **Project Simulation**: Creates realistic project folders with appropriate file types and sizes based on project technology stacks
- **Multi-cultural Support**: Generates user names from multiple cultures (English, Japanese, Spanish) with proper character handling
- **Technology-Appropriate Content**: Simulates different file types and sizes based on user roles and technologies (e.g., developers have source code, designers have large design files)
- **Storage Patterns**: Replicates common storage patterns and issues found in corporate environments, including:
  - Role-appropriate file types and sizes
  - Department-specific content
  - Project-based organization
  - Common misuse patterns (personal files, inappropriate storage usage)

### Use Cases
- Testing storage analysis tools
- Developing data governance solutions
- Training IT staff on file system management
- Testing backup and archival solutions
- Developing storage optimization tools
- Simulating data migration scenarios

### Simulation Scope
The simulation creates:
- User home directories with role-appropriate content
- Project directories with technology-specific files
- Department shares with relevant documentation
- Common application data patterns
- Realistic file naming and organization structures

## Core Scripts

### 1. company_data_new.py
- Generates synthetic company data including employees, departments, and projects
- Creates organizational hierarchy with executives, directors, managers, and individual contributors
- Assigns technologies and roles based on departments
- Outputs data to `company_data_new.json`

### 2. AD_cleanup.py
- Removes Active Directory users and groups created by the simulation
- Supports dry-run mode to preview changes without making them
- Allows selective cleanup of users or groups only
- Handles group membership cleanup
- Provides detailed logging and progress reporting
- Command line options:
  - `--dry-run`: Show what would be deleted without making changes
  - `--verbose`: Show detailed progress
  - `--users-only`: Only delete users
  - `--groups-only`: Only delete groups
  - `--file`: Specify alternative company data file

### 3. AD_setup.py
- Creates Active Directory users and groups
- Sets up appropriate group memberships
- Configures user properties and permissions

### 4. G_drive_setup.py
- Sets up G: drive structure with proper NTFS permissions
- Creates department and project directories
- Assigns appropriate access rights based on roles and groups

## Simulation Scripts

### 5. U_populate_desktop.py
- Creates realistic desktop environments for users
- Generates role-specific files and folders
- Simulates common desktop content patterns
- Creates technology-specific development files
- Simulates messy/organized user behaviors

### 6. U_populate_downloads.py
- Creates realistic download folders for different user roles
- Generates role-specific downloaded files (ISOs, tools, documentation)
- Simulates different user download patterns

### 7. U_populate_emails.py
- Creates PST files to simulate email archives
- Generates role-appropriate email storage patterns
- Simulates email retention behaviors
- Identifies and simulates "email pack rats"
- Creates topic-based archives for some users

## Execution Order

For proper setup, run the scripts in this order:
1. `generate_new_company.py`
2. `AD_cleanup.py`
3. `AD_setup.py`
4. `G_drive_setup.py`
5. Simulation scripts can be run in any order after setup:
   - `U_populate_desktop.py`
   - `U_populate_downloads.py`
   - `U_populate_emails.py`

## Requirements

- Windows environment
- Python 3.x
- Win32 API access (pywin32)
- Administrative privileges for AD and filesystem operations

## Note

These scripts simulate a company environment for testing and development purposes. They create large files and directory structures, so ensure adequate disk space is available.