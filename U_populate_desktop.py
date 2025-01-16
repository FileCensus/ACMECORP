import json
import random
from pathlib import Path
import datetime
import os
import hashlib
import platform
import subprocess

def get_random_date(filename, start_date="2023-01-01", end_date="2024-12-31"):
    """Generate a consistent random date for a given filename"""
    hash_object = hashlib.md5(filename.encode())
    hash_hex = hash_object.hexdigest()
    seed = int(hash_hex[:8], 16)
    random.seed(seed)
    
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    days_between = (end - start).days
    random_days = random.randint(0, days_between)
    
    random.seed()
    return start + datetime.timedelta(days=random_days)

def set_file_dates(file_path, filename):
    """Set consistent modification and access times for a file"""
    date = get_random_date(filename)
    timestamp = date.timestamp()
    os.utime(file_path, (timestamp, timestamp))

def create_large_file(file_path, size):
    """Create a large file filled with zeros using the most efficient method for the OS"""
    system = platform.system().lower()
    try:
        if system == 'linux':
            subprocess.run(['fallocate', '-l', str(size), str(file_path)], check=True)
        elif system == 'windows':
            try:
                subprocess.run(['fsutil', 'file', 'createnew', str(file_path), str(size)], check=True)
            except subprocess.SubprocessError:
                with open(file_path, 'wb') as f:
                    f.seek(size - 1)
                    f.write(b'\0')
        else:
            with open(file_path, 'wb') as f:
                f.seek(size - 1)
                f.write(b'\0')
    except (subprocess.SubprocessError, OSError) as e:
        print(f"Warning: Failed to create {file_path} with size {size} using primary method: {e}")
        try:
            with open(file_path, 'wb') as f:
                f.seek(size - 1)
                f.write(b'\0')
        except OSError as e:
            print(f"Error: Could not create file {file_path}: {e}")
            return False
    return True

def clean_directory(path):
    """Remove all files and subdirectories in the given path"""
    if path.exists():
        print(f"Cleaning directory: {path}")
        for item in path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                clean_directory(item)
                item.rmdir()

def compress_file(file_path):
    """Compress a file using NTFS compression on Windows"""
    if platform.system().lower() == 'windows':
        try:
            subprocess.run(['compact', '/c', str(file_path)], check=True, capture_output=True)
            return True
        except subprocess.SubprocessError as e:
            print(f"Warning: Failed to compress {file_path}: {e}")
            return False
    return False

def compress_directory(dir_path):
    """Enable NTFS compression on a directory and all its contents"""
    if platform.system().lower() == 'windows':
        try:
            subprocess.run(['compact', '/c', '/s', str(dir_path)], check=True, capture_output=True)
            return True
        except subprocess.SubprocessError as e:
            print(f"Warning: Failed to compress directory {dir_path}: {e}")
            return False
    return False

def get_desktop_files(role, technologies):
    """Generate desktop files based on role and technologies"""
    files = []
    
    # Common desktop files
    common_files = [
        ('Meeting Notes.txt', 25_000),
        ('To Do List.txt', 15_000),
        ('Passwords.txt', 1_000),  # People shouldn't do this!
        ('Quick Links.txt', 5_000),
        ('Important Contacts.xlsx', 250_000),
    ]
    
    # Screenshots folder with random screenshots
    screenshots = [
        (f'Screenshot_{random.randint(2023001, 2024365)}.png', random.randint(500_000, 2_000_000))
        for _ in range(random.randint(3, 8))
    ]
    
    # Role-specific files
    role_files = {
        'Developer': [
            ('code_snippets.txt', 50_000),
            ('debug_notes.txt', 30_000),
            ('api_endpoints.json', 15_000),
            ('local_setup.md', 10_000),
            ('dev_environment.yml', 5_000),
        ],
        'Manager': [
            ('Team Performance Reviews.xlsx', 500_000),
            ('Budget_2024.xlsx', 750_000),
            ('Project Timeline.xlsx', 450_000),
            ('Team Schedule.xlsx', 350_000),
            ('Department Goals.pptx', 2_500_000),
        ],
        'Designer': [
            ('color_palette.ai', 500_000),
            ('logo_drafts.psd', 25_000_000),
            ('design_guidelines.pdf', 1_500_000),
            ('asset_library.zip', 50_000_000),
            ('mockups.xd', 15_000_000),
        ],
        'Sales': [
            ('Sales_Pipeline.xlsx', 850_000),
            ('Customer_Contacts.xlsx', 500_000),
            ('Proposals', 0),  # Directory
            ('Presentations', 0),  # Directory
            ('Quote_Templates.xlsx', 250_000),
        ],
        'HR': [
            ('Employee_Handbook.pdf', 2_500_000),
            ('Interview_Schedule.xlsx', 350_000),
            ('Benefits_Summary.pdf', 1_500_000),
            ('HR_Policies', 0),  # Directory
            ('Training_Materials', 0),  # Directory
        ]
    }
    
    # Add common files
    files.extend(common_files)
    
    # Add Screenshots folder
    files.append(('Screenshots', 0))  # Directory
    files.extend([('Screenshots/' + name, size) for name, size in screenshots])
    
    # Add role-specific files
    for role_name, role_specific_files in role_files.items():
        if role_name.lower() in role.lower():
            files.extend(role_specific_files)
    
    # Add technology-specific files
    if "Python" in technologies:
        files.extend([
            ('scripts/useful_scripts.py', 25_000),
            ('scripts/data_cleanup.py', 15_000),
            ('scripts/automation.py', 20_000),
        ])
    
    if "Docker" in technologies:
        files.extend([
            ('docker-compose.yml', 5_000),
            ('Dockerfile', 2_000),
            ('.env', 1_000),
        ])
    
    if "Kubernetes" in technologies:
        files.extend([
            ('k8s/deployment.yaml', 8_000),
            ('k8s/service.yaml', 3_000),
            ('k8s/config.yaml', 5_000),
        ])
    
    # Add some random temporary files (people tend to use desktop as temp storage)
    temp_files = [
        (f'New folder ({i})', 0) for i in range(1, random.randint(2, 5))
    ]
    temp_files.extend([
        ('Untitled Document.docx', 250_000),
        ('Copy of Important.pdf', 1_500_000),
        ('backup.zip', 50_000_000),
        ('export.csv', 5_000_000),
    ])
    
    # Randomly add some temp files
    files.extend(random.sample(temp_files, random.randint(2, 5)))
    
    # Some users are messy and keep everything on their desktop
    is_messy = random.random() < 0.3
    if is_messy:
        files.extend([
            ('Old Files', 0),  # Directory
            ('Misc', 0),  # Directory
            ('Old Files/archive_2023.zip', 150_000_000),
            ('Old Files/legacy_docs.zip', 75_000_000),
            ('Misc/random_notes.txt', 50_000),
            ('Misc/temp.dat', 250_000_000),
        ])
    
    return files, is_messy

def simulate_desktop():
    # Load company data
    with open('company_data.json', 'r') as f:
        company_data = json.load(f)
    
    # Set up base path
    base_path = Path('U:')
    if not base_path.exists():
        print("Note: Using U_Drive directory since U: drive not available")
        base_path = Path('U_Drive')
    
    if not base_path.exists():
        print("Creating U_Drive directory")
        base_path.mkdir(parents=True, exist_ok=True)
        compress_directory(base_path)
    
    users_path = base_path / 'Users'
    users_path.mkdir(parents=True, exist_ok=True)
    compress_directory(users_path)
    
    for user_id, user_data in company_data['users'].items():
        name_parts = user_data['name'].lower().split()
        username = f"{name_parts[0]}_{name_parts[-1]}"
        
        # Create desktop path
        desktop_path = users_path / username / 'Desktop'
        if desktop_path.exists():
            clean_directory(desktop_path)
        desktop_path.mkdir(parents=True, exist_ok=True)
        compress_directory(desktop_path)
        
        # Get desktop files based on role and technologies
        desktop_files, is_messy = get_desktop_files(user_data['role'], user_data['current_technologies'])
        
        if is_messy:
            print(f"Note: {username} has a messy desktop!")
        
        # Create the files and directories
        for filepath, size in desktop_files:
            file_path = desktop_path / filepath
            
            if size == 0:  # Directory
                file_path.mkdir(parents=True, exist_ok=True)
                compress_directory(file_path)
            else:  # File
                file_path.parent.mkdir(parents=True, exist_ok=True)
                if not file_path.exists():
                    print(f"Creating {file_path} with size {size/1_000_000:.1f}MB")
                    if create_large_file(file_path, size):
                        set_file_dates(file_path, filepath)
                        compress_file(file_path)
                    else:
                        print(f"Failed to create {file_path}")
        
        print(f"Created {len(desktop_files)} desktop items for {username}")

if __name__ == "__main__":
    simulate_desktop() 