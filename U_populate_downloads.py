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
    # Create a hash of the filename to get consistent random numbers
    hash_object = hashlib.md5(filename.encode())
    hash_hex = hash_object.hexdigest()
    
    # Use the first 8 characters of hash as a seed
    seed = int(hash_hex[:8], 16)
    random.seed(seed)
    
    # Generate random date
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    days_between = (end - start).days
    random_days = random.randint(0, days_between)
    
    # Reset random seed
    random.seed()
    
    return start + datetime.timedelta(days=random_days)

def set_file_dates(file_path, filename):
    """Set consistent modification and access times for a file"""
    date = get_random_date(filename)
    timestamp = date.timestamp()
    os.utime(file_path, (timestamp, timestamp))

def get_network_downloads():
    """Generate typical downloads for network engineers"""
    iso_files = [
        # Windows Server ISOs - Multiple versions and updates
        ('Windows_Server_2022_EVAL_x64FRE_en-us.iso', 5_400_000_000),  # 5.4GB
        ('Windows_Server_2022_EVAL_x64FRE_en-us_with_updates_Jan2024.iso', 6_500_000_000),  # 6.5GB
        ('Windows_Server_2022_EVAL_x64FRE_en-us_with_updates_Feb2024.iso', 6_800_000_000),  # 6.8GB
        ('Windows_Server_2022_EVAL_x64FRE_en-us_with_updates_Mar2024.iso', 7_000_000_000),  # 7.0GB
        ('Windows_Server_2022_Standard_x64FRE_en-us.iso', 5_600_000_000),  # 5.6GB
        ('Windows_Server_2022_Datacenter_x64FRE_en-us.iso', 5_800_000_000),  # 5.8GB
        ('Windows_Server_2019_EVAL_x64FRE_en-us.iso', 4_700_000_000),  # 4.7GB
        ('Windows_Server_2019_EVAL_x64FRE_en-us_with_updates_Jan2024.iso', 5_600_000_000),  # 5.6GB
        ('Windows_Server_2019_EVAL_x64FRE_en-us_with_updates_Feb2024.iso', 5_800_000_000),  # 5.8GB
        ('Windows_Server_2019_EVAL_x64FRE_en-us_with_updates_Mar2024.iso', 5_900_000_000),  # 5.9GB
        ('Windows_Server_2019_Standard_x64FRE_en-us.iso', 4_900_000_000),  # 4.9GB
        ('Windows_Server_2019_Datacenter_x64FRE_en-us.iso', 5_100_000_000),  # 5.1GB
        ('Windows_Server_2016_EVAL_x64FRE_en-us.iso', 4_300_000_000),  # 4.3GB
        ('Windows_Server_2016_Standard_x64FRE_en-us.iso', 4_500_000_000),  # 4.5GB
        ('Windows_Server_2016_Datacenter_x64FRE_en-us.iso', 4_700_000_000),  # 4.7GB

        # Windows Desktop ISOs - Multiple versions and languages
        ('Windows_11_Enterprise_23H2_x64.iso', 5_400_000_000),  # 5.4GB
        ('Windows_11_Enterprise_23H2_x64_with_updates_Jan2024.iso', 5_900_000_000),  # 5.9GB
        ('Windows_11_Enterprise_23H2_x64_with_updates_Feb2024.iso', 6_100_000_000),  # 6.1GB
        ('Windows_11_Enterprise_23H2_x64_with_updates_Mar2024.iso', 6_200_000_000),  # 6.2GB
        ('Windows_11_Pro_23H2_x64.iso', 5_300_000_000),  # 5.3GB
        ('Windows_11_Pro_23H2_x64_with_updates_Mar2024.iso', 6_000_000_000),  # 6.0GB
        # International Editions
        ('Windows_11_Enterprise_23H2_x64_ja-jp.iso', 5_400_000_000),  # 5.4GB
        ('Windows_11_Enterprise_23H2_x64_es-es.iso', 5_400_000_000),  # 5.4GB
        ('Windows_11_Pro_23H2_x64_ja-jp.iso', 5_300_000_000),  # 5.3GB
        ('Windows_11_Pro_23H2_x64_es-es.iso', 5_300_000_000),  # 5.3GB
        ('Windows_10_Enterprise_22H2_x64_ja-jp.iso', 4_800_000_000),  # 4.8GB
        ('Windows_10_Enterprise_22H2_x64_es-es.iso', 4_800_000_000),  # 4.8GB
        ('Windows_10_Pro_22H2_x64_ja-jp.iso', 4_700_000_000),  # 4.7GB
        ('Windows_10_Pro_22H2_x64_es-es.iso', 4_700_000_000),  # 4.7GB
        ('Windows_10_Enterprise_22H2_x64.iso', 4_800_000_000),  # 4.8GB
        ('Windows_10_Enterprise_22H2_x64_with_updates_Jan2024.iso', 5_400_000_000),  # 5.4GB
        ('Windows_10_Enterprise_22H2_x64_with_updates_Feb2024.iso', 5_600_000_000),  # 5.6GB
        ('Windows_10_Enterprise_22H2_x64_with_updates_Mar2024.iso', 5_700_000_000),  # 5.7GB
        ('Windows_10_Pro_22H2_x64.iso', 4_700_000_000),  # 4.7GB
        ('Windows_10_Pro_22H2_x64_with_updates_Mar2024.iso', 5_500_000_000),  # 5.5GB

        # Linux Distribution ISOs - Multiple versions
        ('ubuntu-22.04.3-live-server-amd64.iso', 4_700_000_000),  # 4.7GB
        ('ubuntu-22.04.4-live-server-amd64.iso', 4_800_000_000),  # 4.8GB
        ('ubuntu-23.10-desktop-amd64.iso', 4_200_000_000),  # 4.2GB
        ('ubuntu-23.10.1-desktop-amd64.iso', 4_300_000_000),  # 4.3GB
        ('ubuntu-20.04.6-live-server-amd64.iso', 4_400_000_000),  # 4.4GB
        ('debian-12.4.0-amd64-DVD-1.iso', 4_700_000_000),  # 4.7GB
        ('debian-12.4.0-amd64-DVD-2.iso', 4_700_000_000),  # 4.7GB
        ('debian-11.8.0-amd64-DVD-1.iso', 4_400_000_000),  # 4.4GB
        ('CentOS-Stream-9-latest-x86_64-dvd1.iso', 9_800_000_000),  # 9.8GB
        ('CentOS-Stream-9-latest-x86_64-dvd2.iso', 9_400_000_000),  # 9.4GB
        ('CentOS-Stream-8-x86_64-latest-dvd1.iso', 8_900_000_000),  # 8.9GB
        ('RHEL-9.3-x86_64-dvd.iso', 8_900_000_000),  # 8.9GB
        ('RHEL-9.3-x86_64-dvd2.iso', 8_700_000_000),  # 8.7GB
        ('RHEL-8.9-x86_64-dvd.iso', 8_500_000_000),  # 8.5GB

        # Security-focused Linux ISOs
        ('Kali-Linux-2024.1-live-amd64.iso', 4_100_000_000),  # 4.1GB
        ('Kali-Linux-2023.4-live-amd64.iso', 4_000_000_000),  # 4.0GB
        ('ParrotOS-5.3-security-amd64.iso', 4_300_000_000),  # 4.3GB
        ('BlackArch-Linux-2024.01.01-x86_64.iso', 15_800_000_000),  # 15.8GB
        ('pentoo-2024-amd64.iso', 8_900_000_000),  # 8.9GB

        # Network Security Appliance ISOs
        ('pfSense-CE-2.7.0-RELEASE-amd64.iso', 3_200_000_000),  # 3.2GB
        ('pfSense-CE-2.7.1-RELEASE-amd64.iso', 3_300_000_000),  # 3.3GB
        ('pfSense-Plus-23.09-RELEASE-amd64.iso', 3_500_000_000),  # 3.5GB
        ('OPNsense-24.1-dvd-amd64.iso', 3_500_000_000),  # 3.5GB
        ('OPNsense-24.1.1-dvd-amd64.iso', 3_600_000_000),  # 3.6GB
        ('Sophos-XG-Home-18.5.iso', 4_200_000_000),  # 4.2GB
        ('untangle-17.1.0-amd64.iso', 3_800_000_000),  # 3.8GB

        # Hypervisor ISOs
        ('VMware-VMvisor-Installer-8.0.0-20513097.x86_64.iso', 2_800_000_000),  # 2.8GB
        ('VMware-VMvisor-Installer-8.0.1-21495797.x86_64.iso', 2_900_000_000),  # 2.9GB
        ('VMware-VMvisor-Installer-7.0U3-19482537.x86_64.iso', 2_600_000_000),  # 2.6GB
        ('proxmox-ve_8.1-2.iso', 1_200_000_000),  # 1.2GB
        ('proxmox-ve_8.0-3.iso', 1_100_000_000),  # 1.1GB
        ('XCP-ng-8.3.0.iso', 950_000_000),  # 950MB
        ('citrix-hypervisor-9.0.0-x86_64.iso', 2_400_000_000),  # 2.4GB

        # Windows Language Packs and Features on Demand
        ('Windows_11_LP_FOD_23H2_x64.iso', 3_200_000_000),  # 3.2GB
        ('Windows_11_LP_FOD_22H2_x64.iso', 3_000_000_000),  # 3.0GB
        ('Windows_10_LP_FOD_22H2_x64.iso', 2_800_000_000),  # 2.8GB
        ('Windows_10_LP_FOD_21H2_x64.iso', 2_600_000_000),  # 2.6GB
    ]
    
    network_tools = [
        ('Wireshark-win64-4.2.2.exe', 185_000_000),  # 185MB
        ('nmap-7.94-setup.exe', 25_000_000),  # 25MB
        ('putty-64bit-0.79-installer.msi', 12_000_000),  # 12MB
        ('WinSCP-5.21.5-Setup.exe', 35_000_000),  # 35MB
        ('advanced-ip-scanner_2.5.4594.1.exe', 45_000_000),  # 45MB
        ('SolarWinds-NPM-Eval.exe', 450_000_000),  # 450MB
        ('cisco_packet_tracer_8.2.1.exe', 280_000_000),  # 280MB
        ('networkminer_2.8.1.exe', 65_000_000),  # 65MB
        ('angry-ip-scanner-3.9.0.exe', 40_000_000),  # 40MB
        ('SecureCRT_9.4.1_x64.exe', 155_000_000),  # 155MB
    ]
    
    cisco_files = [
        ('cisco_iosv_l2.vmdk', 1_500_000_000),  # 1.5GB
        ('cisco_iosv_l3.vmdk', 1_800_000_000),  # 1.8GB
        ('csr1000v-universalk9.17.03.08-serial.qcow2', 4_200_000_000),  # 4.2GB
        ('nxosv-final.9.3.13.qcow2', 2_800_000_000),  # 2.8GB
        ('vios_l2-adventerprisek9-m.SSA.high_iron_20200929.qcow2', 1_900_000_000),  # 1.9GB
    ]
    
    network_docs = [
        ('Cisco_Design_Guide_2024.pdf', 25_000_000),  # 25MB
        ('Network_Security_Best_Practices.pdf', 18_000_000),  # 18MB
        ('SDN_Implementation_Guide.pdf', 15_000_000),  # 15MB
        ('CCNP_Study_Materials.zip', 1_200_000_000),  # 1.2GB
        ('Network_Diagrams_Visio.zip', 85_000_000),  # 85MB
    ]
    
    downloads = []
    # Network engineers are more likely to be pack rats (40% chance)
    is_pack_rat = random.random() < 0.4
    
    if is_pack_rat:
        # Pack rat network engineers keep more ISOs
        downloads.extend(random.sample(iso_files, random.randint(15, 25)))
        downloads.extend(random.sample(network_tools, random.randint(6, 8)))
        downloads.extend(random.sample(cisco_files, random.randint(3, 5)))
        downloads.extend(random.sample(network_docs, random.randint(3, 5)))
    else:
        downloads.extend(random.sample(iso_files, random.randint(5, 8)))
        downloads.extend(random.sample(network_tools, random.randint(2, 4)))
        downloads.extend(random.sample(cisco_files, random.randint(1, 2)))
        downloads.extend(random.sample(network_docs, random.randint(1, 2)))
    
    return downloads, is_pack_rat

def get_ai_ml_downloads():
    """Generate typical downloads for AI/ML engineers"""
    model_files = [
        ('pytorch_model-v1.2.bin', 15_000_000_000),  # 15GB
        ('bert-base-uncased-pytorch_model.bin', 440_000_000),  # 440MB
        ('yolov8x.pt', 380_000_000),  # 380MB
        ('stable-diffusion-v1-5-pruned.ckpt', 12_800_000_000),  # 12.8GB
        ('stable-diffusion-xl-base-1.0.safetensors', 14_500_000_000),  # 14.5GB
        ('mistral-7b-instruct-v0.2.Q4_K_M.gguf', 8_200_000_000),  # 8.2GB
        ('clip-vit-large-patch14.bin', 890_000_000),  # 890MB
        ('falcon-7b-instruct.gguf', 7_900_000_000),  # 7.9GB
        ('codellama-7b-instruct.Q4_K_M.gguf', 8_100_000_000),  # 8.1GB
        ('phi-2.Q4_K_M.gguf', 3_800_000_000),  # 3.8GB
    ]
    
    datasets = [
        ('imagenet_subset_train.zip', 45_000_000_000),  # 45GB
        ('coco2017_val.zip', 25_000_000_000),  # 25GB
        ('custom_dataset_processed.tar.gz', 2_500_000_000),  # 2.5GB
        ('audioset_balanced_train.zip', 18_000_000_000),  # 18GB
        ('librispeech_train.tar.gz', 28_000_000_000),  # 28GB
        ('squad_v2.0_train.json.gz', 850_000_000),  # 850MB
    ]
    
    papers = [
        ('Attention_Is_All_You_Need.pdf', 2_500_000),  # 2.5MB
        ('GPT_4_Technical_Report.pdf', 15_000_000),  # 15MB
        ('RLHF_Implementation_Details.pdf', 8_000_000),  # 8MB
        ('LLM_Training_Techniques.pdf', 12_000_000),  # 12MB
        ('Vision_Transformer_Paper.pdf', 5_000_000),  # 5MB
        ('Stable_Diffusion_XL_Architecture.pdf', 18_000_000),  # 18MB
    ]

    downloads = []
    is_pack_rat = random.random() < 0.1
    if is_pack_rat:
        downloads.extend(random.sample(model_files, random.randint(5, 7)))
        downloads.extend(random.sample(datasets, random.randint(3, 4)))
        downloads.extend(random.sample(papers, random.randint(4, 6)))
    else:
        downloads.extend(random.sample(model_files, random.randint(2, 3)))
        downloads.extend(random.sample(datasets, random.randint(1, 2)))
        downloads.extend(random.sample(papers, random.randint(1, 3)))
    
    return downloads, is_pack_rat

def get_developer_downloads():
    """Generate typical downloads for developers"""
    dev_tools = [
        ('VSCode-win32-x64-1.85.0.exe', 120_000_000),  # 120MB
        ('node-v20.10.0-x64.msi', 32_000_000),  # 32MB
        ('Git-2.43.0-64-bit.exe', 48_000_000),  # 48MB
        ('python-3.11.7-amd64.exe', 28_000_000),  # 28MB
        ('PostgreSQL-16.1-windows-x64.exe', 675_000_000),  # 675MB
        ('mysql-installer-web-community-8.0.35.0.msi', 25_000_000),  # 25MB
        ('docker-desktop-4.27.0-win64.exe', 1_550_000_000),  # 1.55GB
        ('postman-win64-setup.exe', 150_000_000),  # 150MB
    ]
    
    sdks = [
        ('openjdk-17.0.2_windows-x64_bin.zip', 180_000_000),  # 180MB
        ('dotnet-sdk-8.0.100-win-x64.exe', 250_000_000),  # 250MB
        ('cuda_12.3.1_windows.exe', 8_200_000_000),  # 8.2GB
    ]
    
    downloads = []
    # Add 3-5 random dev tools
    downloads.extend(random.sample(dev_tools, random.randint(3, 5)))
    # Add 1-2 random SDKs
    downloads.extend(random.sample(sdks, random.randint(1, 2)))
    
    return downloads

def get_designer_downloads():
    """Generate typical downloads for designers"""
    assets = [
        ('premium_icon_pack_2024.zip', 2_850_000_000),  # 2.85GB
        ('stock_photos_bundle_march2024.zip', 15_500_000_000),  # 15.5GB
        ('font_collection_2024.zip', 450_000_000),  # 450MB
        ('ui_kit_material_design.zip', 750_000_000),  # 750MB
        ('texture_pack_pro.zip', 4_800_000_000),  # 4.8GB
    ]
    
    software = [
        ('Adobe_Photoshop_2024_Setup.exe', 5_200_000_000),  # 5.2GB
        ('Adobe_Illustrator_2024_Setup.exe', 4_800_000_000),  # 4.8GB
        ('Figma_Setup.exe', 85_000_000),  # 85MB
        ('SketchUp-Pro-2024-EN-x64.exe', 350_000_000),  # 350MB
    ]
    
    downloads = []
    # Add 2-3 random asset packs
    downloads.extend(random.sample(assets, random.randint(2, 3)))
    # Add 1-2 random software installers
    downloads.extend(random.sample(software, random.randint(1, 2)))
    
    return downloads

def create_large_file(file_path, size):
    """Create a large file filled with zeros using the most efficient method for the OS"""
    system = platform.system().lower()
    
    try:
        if system == 'linux':
            # Use fallocate on Linux - very fast
            subprocess.run(['fallocate', '-l', str(size), str(file_path)], check=True)
        
        elif system == 'windows':
            try:
                # Try fsutil first
                subprocess.run(['fsutil', 'file', 'createnew', str(file_path), str(size)], check=True)
            except subprocess.SubprocessError:
                # If fsutil fails, try direct file creation
                with open(file_path, 'wb') as f:
                    f.seek(size - 1)
                    f.write(b'\0')
        
        else:
            # For other OS - use seek method
            with open(file_path, 'wb') as f:
                f.seek(size - 1)
                f.write(b'\0')
    
    except (subprocess.SubprocessError, OSError) as e:
        print(f"Warning: Failed to create {file_path} with size {size} using primary method: {e}")
        try:
            # Fallback to seek method
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
                clean_directory(item)  # Clean subdirectories recursively
                item.rmdir()  # Remove the empty directory

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

def simulate_downloads():
    # Load company data
    with open('company_data.json', 'r') as f:
        company_data = json.load(f)
    
    # Try both possible base paths
    base_path = Path('U:')
    if not base_path.exists():
        print("Note: Using U_Drive directory since U: drive not available")
        base_path = Path('U_Drive')
    
    if not base_path.exists():
        print("Creating U_Drive directory")
        base_path.mkdir(parents=True, exist_ok=True)
        compress_directory(base_path)
    
    # Ensure Users directory exists
    users_path = base_path / 'Users'
    users_path.mkdir(parents=True, exist_ok=True)
    compress_directory(users_path)
    
    for user_id, user_data in company_data['users'].items():
        # Get username
        name_parts = user_data['name'].lower().split()
        username = f"{name_parts[0]}_{name_parts[-1]}"
        
        # Create downloads path
        downloads_path = users_path / username / 'Downloads'
        # Clean existing downloads directory if it exists
        if downloads_path.exists():
            clean_directory(downloads_path)
        else:
            print(f"Creating Downloads directory for {username}")
            downloads_path.mkdir(parents=True, exist_ok=True)
            compress_directory(downloads_path)
            
        # Combine current and likely technologies
        technologies = set(user_data['current_technologies'])
        role = user_data['role']
        
        # Initialize downloads list and pack rat status
        downloads = []
        is_pack_rat = False
        
        # Add role-specific downloads
        if any(role_name in role for role_name in ['Network Engineer', 'Infrastructure', 'Systems Administrator']):
            new_downloads, is_rat = get_network_downloads()
            is_pack_rat = is_pack_rat or is_rat
            downloads.extend(new_downloads)
            
        if any(tech in technologies for tech in ['PyTorch', 'TensorFlow', 'Machine Learning']):
            new_downloads, is_rat = get_ai_ml_downloads()
            is_pack_rat = is_pack_rat or is_rat
            downloads.extend(new_downloads)
            
        if any(role_name in role for role_name in ['Developer', 'Engineer']) or \
           any(tech in technologies for tech in ['Python', 'Java', 'JavaScript', 'C#']):
            downloads.extend(get_developer_downloads())
            
        if any(tech in technologies for tech in ['Adobe Creative Suite', 'UI/UX Design']):
            downloads.extend(get_designer_downloads())
        
        if is_pack_rat:
            print(f"Note: {username} is a digital pack rat!")
        
        # Create the files
        for filename, size in downloads:
            base_filename = filename  # Store original filename for date generation
            # Add date to all filenames
            date = get_random_date(filename).strftime("%Y%m%d")
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{date}.{ext}"
            file_path = downloads_path / filename
            
            # Create empty file of specified size
            if not file_path.exists():
                print(f"Creating {file_path} with size {size/1_000_000_000:.1f}GB")
                if create_large_file(file_path, size):
                    # Set consistent modification time based on original filename
                    set_file_dates(file_path, base_filename)
                    # Compress the file
                    compress_file(file_path)
                else:
                    print(f"Failed to create {file_path}")
                
        print(f"Created {len(downloads)} download files for {username}")

if __name__ == "__main__":
    simulate_downloads() 