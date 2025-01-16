import json
import random
from pathlib import Path
import datetime
import os
import hashlib
import platform
import subprocess

def get_random_date(filename, start_date="2018-01-01", end_date="2024-12-31"):
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

def get_email_archives(role, years_at_company):
    """Generate email PST files based on role and tenure"""
    # Base sizes for different roles (per year in GB)
    role_sizes = {
        'Executive': (25.0, 40.0),        # Executives keep more emails
        'Manager': (15.0, 25.0),          # Managers have lots of communication
        'Sales': (20.0, 30.0),            # Sales people keep client communications
        'Network Engineer': (10.0, 20.0),  # Technical staff with moderate email
        'Developer': (8.0, 15.0),         # Developers with less email
        'Designer': (8.0, 15.0),          # Designers with less email
        'HR': (20.0, 30.0),              # HR keeps everything
        'Marketing': (15.0, 25.0),        # Marketing with moderate email
        'Support': (12.0, 20.0),          # Support staff with regular email
    }

    # Default size if role not found
    base_size_range = role_sizes.get(role, (10.0, 20.0))
    
    # Determine if user is an email pack rat (20% chance, 40% for executives and HR)
    is_pack_rat = random.random() < (0.4 if role in ['Executive', 'HR'] else 0.2)
    
    # Calculate number of PST files and sizes
    pst_files = []
    
    # Current year's PST
    current_size = random.randint(int(base_size_range[0] * 0.7 * 1e9), 
                                int(base_size_range[1] * 0.7 * 1e9))
    pst_files.append(('Outlook_2024.pst', current_size))
    
    # Only create archives for 2022-2023
    for year in [2023, 2022]:
        # Pack rats keep everything, others might archive less
        size_multiplier = 1.0 if is_pack_rat else random.uniform(0.4, 0.8)
        size = random.randint(int(base_size_range[0] * 1e9 * size_multiplier),
                            int(base_size_range[1] * 1e9 * size_multiplier))
        pst_files.append((f'Archive_{year}.pst', size))
    
    # Pack rats might have additional topic-based archives
    if is_pack_rat:
        topics = [
            'Projects', 'Clients', 'Important', 'Personal', 'Old_Projects',
            'Reference', 'Training', 'Compliance', 'Vendors', 'Teams'
        ]
        num_extra = random.randint(2, 4)  # Reduced number of topic archives
        for topic in random.sample(topics, num_extra):
            size = random.randint(int(5e9), int(15e9))  # 5-15GB
            pst_files.append((f'Archive_{topic}.pst', size))
    
    return pst_files, is_pack_rat

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
            # Enable compression on the directory and all contents
            subprocess.run(['compact', '/c', '/s', str(dir_path)], check=True, capture_output=True)
            return True
        except subprocess.SubprocessError as e:
            print(f"Warning: Failed to compress directory {dir_path}: {e}")
            return False
    return False

def simulate_emails():
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
        
        # Create Outlook directory in user's folder
        outlook_path = users_path / username / 'Documents' / 'Outlook Files'
        if outlook_path.exists():
            clean_directory(outlook_path)
        outlook_path.mkdir(parents=True, exist_ok=True)
        compress_directory(outlook_path)
        
        # Calculate years at company (use user ID as a seed for consistency)
        random.seed(hash(user_id))
        years_at_company = random.randint(1, 20)
        random.seed()
        
        # Get email archives based on role
        pst_files, is_pack_rat = get_email_archives(user_data['role'], years_at_company)
        
        if is_pack_rat:
            print(f"Note: {username} is an email pack rat!")
        
        # Create PST files
        for filename, size in pst_files:
            file_path = outlook_path / filename
            print(f"Creating {file_path} with size {size/1_000_000_000:.1f}GB")
            if create_large_file(file_path, size):
                set_file_dates(file_path, filename)
                # Compress the PST file
                compress_file(file_path)
            else:
                print(f"Failed to create {file_path}")
        
        print(f"Created {len(pst_files)} PST files for {username}")

if __name__ == "__main__":
    simulate_emails() 