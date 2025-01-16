import json
import os
from pathlib import Path
import random
import subprocess
import platform

def load_company_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def create_app_directories():
    """Create standard application directories that might exist"""
    return {
        'ATS Systems': 'AppData/Local/ATS',
        'Adobe Creative Suite': 'AppData/Local/Adobe',
        'Angular': 'AppData/Roaming/Angular',
        'AWS': '.aws',
        'Azure': '.azure',
        'Confluence': 'AppData/Local/Atlassian/Confluence',
        'Docker': '.docker',
        'Excel': 'AppData/Roaming/Microsoft/Excel',
        'GCP': 'AppData/Roaming/gcloud',
        'Git': '.git',
        'Google Analytics': 'AppData/Local/Google/Analytics',
        'HRIS': 'AppData/Local/HRIS',
        'HubSpot': 'AppData/Local/HubSpot',
        'Jenkins': '.jenkins',
        'Jira': 'AppData/Local/Atlassian/Jira',
        'Kubernetes': '.kube',
        'LinkedIn': 'AppData/Roaming/LinkedIn',
        'PowerBI': 'AppData/Local/Microsoft/PowerBI',
        'PyTorch': 'AppData/Local/PyTorch',
        'Python': 'AppData/Local/Programs/Python',
        'R': 'AppData/Local/R',
        'React': 'AppData/Roaming/React',
        'Salesforce': 'AppData/Local/Salesforce',
        'TensorFlow': 'AppData/Local/TensorFlow',
        'Terraform': '.terraform',
        'VSCode': 'AppData/Roaming/Code',
        'Workday': 'AppData/Local/Workday',
        'VMware': 'Documents/Virtual Machines',
    }

def get_random_date_2024():
    """Generate a random date in 2024"""
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Using 28 to be safe for all months
    return f"2024_{month:02d}_{day:02d}"

def get_random_version():
    """Generate a random version string"""
    patterns = [
        f"v{random.randint(1,9)}.{random.randint(0,9)}.{random.randint(0,9)}",
        f"rev_{random.randint(100,999)}",
        f"build_{random.randint(1000,9999)}",
        f"_{get_random_date_2024()}"
    ]
    return random.choice(patterns)

def get_typical_files():
    """Return dictionary of typical files for each application with typical sizes in bytes"""
    project_types = ["Internal", "Client", "POC", "MVP", "Phase1", "Phase2"]
    client_names = ["Acme", "GlobalTech", "InnovaCorp", "TechDynamics", "FutureScale"]
    departments = ["Marketing", "Sales", "Engineering", "Finance", "Operations"]
    
    return {
        'ATS Systems': [
            (f'candidate_profiles_{get_random_date_2024()}.db', 50_000_000),
            (f'interview_schedules_Q{random.randint(1,4)}_2024.xlsx', 2_000_000),
            (f'recruitment_metrics_{random.choice(departments)}_{get_random_date_2024()}.pdf', 500_000),
            (f'talent_pipeline_{get_random_date_2024()}.xlsx', 3_000_000),
            (f'hiring_forecast_2024_Q{random.randint(1,4)}.pdf', 1_500_000),
        ],
        'Adobe Creative Suite': [
            (f'corporate_branding_{get_random_date_2024()}.psd', 120_000_000),
            (f'{random.choice(client_names)}_Presentation_{get_random_date_2024()}.psd', 85_000_000),
            (f'Product_Launch_{random.choice(project_types)}_{get_random_version()}.ai', 40_000_000),
            (f'Social_Media_Assets_{get_random_date_2024()}.psd', 65_000_000),
            (f'Website_Mockup_v{random.randint(1,5)}.xd', 30_000_000),
            (f'Brand_Guidelines_{get_random_version()}.indd', 25_000_000),
            (f'Newsletter_Template_Q{random.randint(1,4)}_2024.indd', 15_000_000),
        ],
        'Angular': [
            ('angular.json', 2_000),
            ('tsconfig.json', 1_000),
            ('package-lock.json', 500_000),
        ],
        'AWS': [
            ('credentials', 1_000),
            ('config', 500),
            ('cli_history', 10_000),
        ],
        'Azure': [
            ('azureProfile.json', 2_000),
            ('accessTokens.json', 1_000),
        ],
        'Confluence': [
            ('confluence_cache.db', 100_000_000),
            ('attachments.idx', 5_000_000),
        ],
        'Docker': [
            ('config.json', 2_000),
            ('daemon.json', 1_000),
        ],
        'Excel': [
            (f'Q{random.randint(1,4)}_2024_Reports.xlsx', 5_000_000),
            (f'Department_Budget_2024_{random.choice(["Draft", "Final", "Review", "Approved"])}.xlsx', 3_000_000),
            (f'Project_Tracking_{get_random_date_2024()}.xlsx', 4_000_000),
            (f'Financial_Analysis_{get_random_date_2024()}.xlsx', 6_000_000),
            (f'Resource_Planning_2024_Q{random.randint(1,4)}.xlsx', 4_500_000),
        ],
        'GCP': [
            ('credentials.json', 2_000),
            ('application_default_credentials.json', 1_000),
        ],
        'Google Analytics': [
            ('analytics_cache.db', 50_000_000),
            ('report_templates.json', 1_000_000),
        ],
        'HRIS': [
            (f'employee_records_{get_random_date_2024()}.db', 100_000_000),
            (f'payroll_data_Q{random.randint(1,4)}_2024.xlsx', 10_000_000),
            (f'attendance_logs_{random.choice(departments)}_{get_random_date_2024()}.db', 50_000_000),
            (f'benefits_report_{get_random_date_2024()}.xlsx', 15_000_000),
            (f'performance_reviews_Q{random.randint(1,4)}_2024.xlsx', 25_000_000),
            (f'training_completion_{get_random_date_2024()}.csv', 8_000_000),
        ],
        'HubSpot': [
            ('contact_lists.db', 75_000_000),
            ('campaign_templates.json', 2_000_000),
            ('analytics_cache.db', 50_000_000),
        ],
        'Jenkins': [
            ('config.xml', 10_000),
            ('jenkins.log', 50_000_000),
            ('workspace.log', 20_000_000),
        ],
        'Jira': [
            ('jira_cache.db', 200_000_000),
            ('issue_templates.json', 1_000_000),
            ('workflow_configs.xml', 500_000),
        ],
        'Kubernetes': [
            ('config', 5_000),
            ('cache.db', 20_000_000),
            ('credentials.yaml', 1_000),
        ],
        'PowerBI': [
            (f'Sales_Dashboard_{get_random_date_2024()}.pbix', 50_000_000),
            (f'Financial_Reports_Q{random.randint(1,4)}_2024.pbix', 75_000_000),
            (f'Marketing_Analytics_{random.choice(client_names)}.pbix', 60_000_000),
            (f'KPI_Dashboard_{random.choice(departments)}_{get_random_date_2024()}.pbix', 45_000_000),
            (f'Performance_Metrics_{get_random_version()}.pbix', 55_000_000),
            (f'Project_Analytics_{random.choice(project_types)}.pbix', 40_000_000),
        ],
        'PyTorch': [
            (f'model_checkpoints_{get_random_date_2024()}.pt', 500_000_000),
            (f'training_logs_{get_random_date_2024()}.txt', 10_000_000),
            (f'customer_segmentation{get_random_version()}.pt', 750_000_000),
            ('sentiment_analysis_bert.pt', 1_200_000_000),
            ('image_classification_resnet50.pt', 900_000_000),
            ('transformer_weights.pt', 2_500_000_000),
            ('lstm_predictions.pt', 300_000_000),
            ('embeddings_cache.pt', 1_500_000_000),
            ('optimizer_state.pt', 200_000_000),
            (f'experiment_{random.randint(1000,9999)}.pt', 400_000_000),
        ],
        'Python': [
            ('venv', 100_000_000),
            ('pip.log', 1_000_000),
            ('requirements.txt', 2_000),
            ('data_preprocessing.py', 50_000),
            ('model_training.py', 75_000),
            ('utils.py', 30_000),
            ('config.yaml', 5_000),
            ('dataset_loader.py', 40_000),
            ('metrics.py', 25_000),
            ('visualization.py', 60_000),
            ('inference.py', 45_000),
        ],
        'R': [
            ('.Rhistory', 1_000_000),
            ('.RData', 50_000_000),
            ('statistical_analysis.R', 100_000),
            ('data_visualization.R', 150_000),
            ('hypothesis_testing.R', 80_000),
            ('regression_models.R', 200_000),
            ('time_series_analysis.R', 250_000),
            ('feature_selection.R', 120_000),
            (f'experiment_{random.randint(100,999)}.RData', 75_000_000),
            ('processed_data.rds', 500_000_000),
        ],
        'React': [
            ('package.json', 2_000),
            ('node_modules.zip', 200_000_000),
            ('build_assets.tar', 100_000_000),
        ],
        'Salesforce': [
            (f'salesforce_cache_{get_random_date_2024()}.db', 150_000_000),
            (f'contact_exports_{random.choice(departments)}_{get_random_date_2024()}.csv', 20_000_000),
            (f'opportunity_reports_Q{random.randint(1,4)}_2024.xlsx', 5_000_000),
            (f'pipeline_forecast_{get_random_date_2024()}.xlsx', 8_000_000),
            (f'lead_analysis_{random.choice(client_names)}.xlsx', 6_000_000),
            (f'campaign_metrics_{get_random_date_2024()}.csv', 15_000_000),
        ],
        'TensorFlow': [
            ('saved_model.pb', 750_000_000),
            ('checkpoints.data', 500_000_000),
            ('training_logs.tfevents', 100_000_000),
            ('bert_base_uncased', 4_200_000_000),
            ('gpt2_medium_weights', 5_500_000_000),
            ('resnet152_imagenet.h5', 900_000_000),
            ('yolov5_weights.h5', 800_000_000),
            (f'experiment_run_{random.randint(100,999)}.h5', 650_000_000),
            ('model_metrics.json', 2_000_000),
            ('dataset_cache.tfrecord', 2_500_000_000),
            ('embeddings.npy', 1_800_000_000),
        ],
        'Terraform': [
            ('.terraform.lock.hcl', 5_000),
            ('terraform.tfstate', 1_000_000),
            ('terraform.tfstate.backup', 1_000_000),
        ],
        'VSCode': [
            ('User/settings.json', 10_000),
            ('extensions.json', 5_000),
            ('workspace.code-workspace', 2_000),
        ],
        'Workday': [
            ('workday_cache.db', 100_000_000),
            ('report_templates.xlsx', 5_000_000),
            ('integration_logs.txt', 10_000_000),
        ],
        'Jupyter': [
            ('EDA.ipynb', 5_000_000),
            ('Model_Training.ipynb', 8_000_000),
            ('Data_Visualization.ipynb', 6_000_000),
            ('Feature_Engineering.ipynb', 7_000_000),
            (f'Experiment_{random.randint(1,99)}.ipynb', 10_000_000),
            ('Results_Analysis.ipynb', 4_000_000),
        ],
        'MLflow': [
            ('mlruns/metadata.db', 150_000_000),
            ('mlruns/artifacts.db', 500_000_000),
            ('mlflow.log', 50_000_000),
            (f'run_{random.randint(10000,99999)}/metrics', 20_000_000),
            (f'run_{random.randint(10000,99999)}/params', 1_000_000),
        ],
        'Weights & Biases': [
            ('wandb/latest-run/files/config.yaml', 1_000),
            ('wandb/debug.log', 5_000_000),
            ('wandb/run-history.db', 200_000_000),
            (f'wandb/run-{random.randint(10000,99999)}/files/media', 1_500_000_000),
        ],
        'DVC': [
            ('.dvc/config', 1_000),
            ('.dvc/cache', 2_000_000_000),
            ('data.dvc', 500),
            ('models.dvc', 1_000),
            ('dataset_registry.json', 100_000),
        ],
        'VMware': [
            ('VMs/Windows_Server_2022/Windows_Server_2022.vmdk', 4_000_000_000),  # 4GB
            ('VMs/Windows_Server_2022/Windows_Server_2022.nvram', 8_000),
            ('VMs/Windows_Server_2022/vmware.log', 5_000_000),
            ('VMs/Ubuntu_22.04_LTS/Ubuntu_22.04_LTS.vmdk', 2_500_000_000),  # 2.5GB
            ('VMs/Ubuntu_22.04_LTS/Ubuntu_22.04_LTS.nvram', 8_000),
            ('VMs/Ubuntu_22.04_LTS/vmware.log', 2_000_000),
            ('VMs/CentOS_8/CentOS_8.vmdk', 2_000_000_000),  # 2GB
            ('VMs/CentOS_8/CentOS_8.nvram', 8_000),
            ('VMs/CentOS_8/vmware.log', 2_000_000),
            ('VMs/Kali_Linux/Kali_Linux.vmdk', 3_000_000_000),  # 3GB
            ('VMs/Kali_Linux/Kali_Linux.nvram', 8_000),
            ('VMs/Kali_Linux/vmware.log', 3_000_000),
            # Snapshots
            ('VMs/Windows_Server_2022/Snapshots/snapshot1.vmdk', 1_500_000_000),
            ('VMs/Ubuntu_22.04_LTS/Snapshots/snapshot1.vmdk', 1_000_000_000),
            # VM Templates
            ('Templates/Windows_Template.vmdk', 5_000_000_000),
            ('Templates/Linux_Template.vmdk', 3_500_000_000),
            # Configuration files
            ('config/preferences.ini', 10_000),
            ('config/inventory.vmls', 50_000),
            ('logs/vmware_network.log', 100_000_000),
        ],
        'Video Projects': [
            (f'Projects/Corporate_Overview_2024/Corporate_Overview_{get_random_version()}.prproj', 5_000_000),
            (f'Footage/Corporate_Overview/A_Roll/Interview_CEO_{get_random_date_2024()}.mxf', 450_000_000),
            (f'Footage/Product_Demo/Take_{random.randint(1,5)}_{get_random_date_2024()}.mxf', 380_000_000),
            (f'Footage/Customer_Testimonials/Client_{random.randint(1,10)}_{get_random_date_2024()}.mxf', 420_000_000),
        ],
        'Development': [
            (f'logs/build_{get_random_date_2024()}_{random.randint(100,999)}.log', 250_000_000),
            (f'logs/deploy_{get_random_date_2024()}_env_{random.choice(["dev", "staging", "prod"])}.log', 180_000_000),
            (f'logs/test_run_{get_random_date_2024()}_{random.randint(1000,9999)}.xml', 150_000_000),
        ],
        'AI Models': [
            # Model checkpoints (50-200MB)
            (f'models/finetuned/checkpoint_{get_random_date_2024()}_epoch_{random.randint(1,100)}.pth', 150_000_000),
            # Exported models (100-500MB)
            (f'models/custom/company_model_{get_random_version()}.safetensors', 250_000_000),
            # ONNX models (50-150MB)
            (f'models/experiments/run_{get_random_date_2024()}_{random.randint(1000,9999)}.onnx', 100_000_000),
            # Large Language Models (25-100GB)
            ('models/llm/llama2_70b_finetuned.pth', 15_000_000_000),  # 15GB
            ('models/llm/mistral_7b_company_finetuned.pth', 6_000_000_000),  # 6GB
            ('models/llm/gpt_neo_20b.pth', 8_000_000_000),  # 8GB
            # Vision Models (5-50GB)
            ('models/vision/stable_diffusion_xl_finetuned.pth', 7_000_000_000),  # 7GB
            ('models/vision/sam_vit_h.pth', 2_500_000_000),  # 2.5GB
            ('models/vision/detection_model_finetuned.pth', 1_800_000_000),  # 1.8GB
            # Speech Models (5-40GB)
            ('models/speech/whisper_large_v3.pth', 3_000_000_000),  # 3GB
            ('models/speech/voice_clone_model.pth', 2_000_000_000),  # 2GB
            # Model Shards and Checkpoints (25GB each)
            ('models/llm/llama2_70b.00001.pth', 4_000_000_000),  # 4GB
            ('models/llm/llama2_70b.00002.pth', 4_000_000_000),  # 4GB
            ('models/llm/llama2_70b.00003.pth', 4_000_000_000),  # 4GB
            ('models/llm/llama2_70b.00004.pth', 4_000_000_000),  # 4GB
        ],
    }

def get_random_file_size(base_size):
    """
    Generate a random file size based on a typical size.
    Has a 10% chance of creating a 'monster' file that's 100x larger.
    Otherwise varies between 0.5x and 2x the base size.
    """
    if random.random() < 0.1:  # 10% chance of monster file
        return int(base_size * 100 * random.uniform(0.8, 1.2))
    else:
        return int(base_size * random.uniform(0.5, 2.0))

def sanitize_path(path):
    """Sanitize file path to be valid on Windows systems"""
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        path = path.replace(char, '_')
    
    # Ensure path components don't end with space or period
    parts = path.split('/')
    parts = [part.rstrip(' .') for part in parts]
    
    return '/'.join(parts)

def create_typical_files(file_path, file_info):
    """Create a file of specified size"""
    for filename, size in file_info:
        # Sanitize the filename
        filename = sanitize_path(filename)
        
        # Skip files without extensions unless they're in special dot directories
        path_parts = Path(filename).parts
        has_extension = '.' in Path(filename).name
        is_dot_config = any(part.startswith('.') for part in path_parts)  # e.g. .aws/config
        
        if not (has_extension or is_dot_config):
            continue
        
        full_path = file_path / filename
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        # Get randomized size
        actual_size = get_random_file_size(size)
        try:
            # Create file with specified size
            with open(full_path, 'wb') as f:
                f.seek(actual_size - 1)
                f.write(b'\0')
            if actual_size > size * 50:  # If it's a monster file
                print(f"Warning: Large file created: {full_path} ({actual_size / 1_000_000:.1f} MB)")
        except OSError as e:
            print(f"Error creating file {full_path}: {e}")
            continue

def get_dev_log_files():
    """Return list of typical development log files with sizes"""
    return [
        ('logs/npm-debug.log', 50_000_000),
        ('logs/yarn-error.log', 75_000_000),
        ('logs/webpack-stats.log', 150_000_000),
        ('logs/babel-transpile.log', 25_000_000),
        ('logs/test-results.xml', 200_000_000),
        ('logs/coverage-report.xml', 100_000_000),
        ('logs/eslint-output.log', 30_000_000),
        ('logs/typescript-compile.log', 45_000_000),
        ('logs/jest-test-results.log', 80_000_000),
        ('logs/python-debug.log', 500_000_000),
        ('logs/gunicorn-access.log', 2_000_000_000),
        ('logs/celery-worker.log', 1_500_000_000),
        ('logs/django-debug.log', 800_000_000),
        ('logs/flask-app.log', 600_000_000),
        ('logs/nginx-access.log', 5_000_000_000),
        ('logs/redis-server.log', 300_000_000),
        ('logs/postgres-query.log', 4_000_000_000),
        (f'logs/build_{random.randint(1000,9999)}.log', 250_000_000),
        (f'logs/deploy_{random.randint(1000,9999)}.log', 180_000_000),
        (f'logs/error_{random.randint(1000,9999)}.log', 2_500_000_000),
    ]

def is_developer_role(role, technologies):
    """Check if user is in a development-related role"""
    dev_roles = {
        "Software Engineer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "DevOps Engineer",
        "Python Developer",
        "JavaScript Developer",
        "Web Developer",
        "Application Developer",
        "Development Lead"
    }
    
    dev_technologies = {
        "Python",
        "JavaScript",
        "React",
        "Angular",
        "Node.js",
        "TypeScript",
        "Go",
        "Java"
    }
    
    return (role in dev_roles) or (len(dev_technologies.intersection(technologies)) >= 2)

def get_ai_model_files():
    """Return list of AI model files with realistic sizes"""
    return [
        # Language Models
        ('models/llama2/7B/consolidated.00.pth', 13_000_000_000),  # 13GB
        ('models/llama2/tokenizer.model', 500_000_000),
        ('models/llama2/tokenizer_checklist.chk', 1_000_000),
        ('models/mistral/7B/model.safetensors', 14_000_000_000),  # 14GB
        ('models/phi-2/model.safetensors', 2_700_000_000),  # 2.7GB
        ('models/stable-diffusion/v1.5/model.ckpt', 4_000_000_000),  # 4GB
        ('models/stable-diffusion/v2.1/model.safetensors', 5_500_000_000),  # 5.5GB
        
        # Vision Models
        ('models/yolov8/yolov8x.pt', 350_000_000),  # 350MB
        ('models/yolov8/yolov8n.pt', 6_000_000),    # 6MB
        ('models/sam/sam_vit_h.pth', 2_500_000_000),  # 2.5GB
        ('models/sam/sam_vit_b.pth', 375_000_000),   # 375MB
        ('models/dino/dinov2_vitl14.pth', 1_500_000_000),  # 1.5GB
        
        # Embeddings
        ('models/embeddings/all-MiniLM-L6-v2.safetensors', 90_000_000),  # 90MB
        ('models/embeddings/multilingual-e5-large.safetensors', 1_300_000_000),  # 1.3GB
        
        # Fine-tuned Models
        (f'models/finetuned/checkpoint_{random.randint(1000,9999)}.pth', 2_000_000_000),
        (f'models/finetuned/best_model_{random.randint(1000,9999)}.safetensors', 2_500_000_000),
        
        # Quantized Models
        ('models/quantized/llama2-7b-q4_K_M.gguf', 4_000_000_000),  # 4GB
        ('models/quantized/mistral-7b-q4_K_S.gguf', 3_800_000_000),  # 3.8GB
        ('models/quantized/phi2-q4_K_S.gguf', 1_500_000_000),  # 1.5GB
        
        # ONNX Models
        ('models/onnx/model_optimized.onnx', 800_000_000),
        ('models/onnx/quantized_model.onnx', 400_000_000),
        
        # Model Configs and Metadata
        ('models/configs/model_config.json', 1_000_000),
        ('models/configs/training_args.json', 500_000),
        ('models/configs/tokenizer_config.json', 250_000),
    ]

def is_ai_practitioner(role, technologies):
    """Check if user works with AI/ML"""
    ai_roles = {
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Researcher",
        "Research Engineer",
        "ML Engineer",
        "AI Engineer",
        "Deep Learning Engineer",
        "NLP Engineer",
        "Computer Vision Engineer"
    }
    
    ai_technologies = {
        "PyTorch",
        "TensorFlow",
        "scikit-learn",
        "Python",
        "R",
        "Jupyter"
    }
    
    return (role in ai_roles) or (len(ai_technologies.intersection(technologies)) >= 2)

def get_video_production_files():
    """Return list of typical video production files with sizes"""
    return [
        # Project Files
        (f'Projects/Corporate_Overview_2024/Corporate_Overview_{get_random_version()}.prproj', 5_000_000),
        (f'Projects/Product_Launch_2024/Product_Launch_{get_random_version()}.prproj', 4_500_000),
        (f'Projects/Training_Series/Module_{random.randint(1,5)}_{get_random_version()}.prproj', 4_000_000),
        
        # Raw Footage
        (f'Footage/Corporate_Overview/A_Roll/Interview_CEO_{get_random_date_2024()}.mxf', 450_000_000),
        (f'Footage/Corporate_Overview/A_Roll/Interview_CTO_{get_random_date_2024()}.mxf', 380_000_000),
        (f'Footage/Corporate_Overview/B_Roll/Office_Shots_{get_random_date_2024()}.mxf', 650_000_000),
        (f'Footage/Corporate_Overview/B_Roll/Product_Demos_{get_random_date_2024()}.mxf', 550_000_000),
        
        # Proxy Files
        (f'Footage/Proxies/Interview_CEO_{get_random_date_2024()}_PROXY.mp4', 80_000_000),
        (f'Footage/Proxies/Interview_CTO_{get_random_date_2024()}_PROXY.mp4', 75_000_000),
        (f'Footage/Proxies/Office_Shots_{get_random_date_2024()}_PROXY.mp4', 120_000_000),
        (f'Footage/Proxies/Product_Demos_{get_random_date_2024()}_PROXY.mp4', 90_000_000),
        
        # Exports
        (f'Exports/Corporate_Overview_FINAL_{get_random_version()}.mp4', 250_000_000),
        (f'Exports/Product_Launch_FINAL_{get_random_version()}.mp4', 200_000_000),
        (f'Exports/Training_Module_{random.randint(1,5)}_FINAL_{get_random_version()}.mp4', 180_000_000),
    ]

def is_video_editor(role, technologies):
    """Check if user works with video production"""
    video_roles = {
        "Video Editor",
        "Motion Designer",
        "Content Creator",
        "Multimedia Specialist",
        "Creative Director",
        "Media Producer",
        "Digital Media Specialist"
    }
    
    video_technologies = {
        "Adobe Creative Suite",
        "Adobe Premiere",
        "After Effects",
        "Final Cut Pro",
        "DaVinci Resolve"
    }
    
    return (role in video_roles) or ("Adobe Creative Suite" in technologies)

def get_project_archives(project_number, project_name):
    """Generate archive files for a project with realistic sizes"""
    archives = []
    date = get_random_date_2024()
    
    # Main project backups (500MB-2GB)
    archives.extend([
        (f'Backups/{project_number}_Full_Backup_{date}.zip', 1_500_000_000),
        (f'Backups/{project_number}_Source_Code_{date}.zip', 800_000_000),
        (f'Backups/{project_number}_Assets_{date}.zip', 1_200_000_000),
    ])
    
    # Version archives (200-800MB each)
    for month in range(1, 13):
        if random.random() < 0.15:  # 15% chance for each month (reduced from 30%)
            archives.append(
                (f'Backups/{project_number}_v{month:02d}_{date}.zip', 
                 random.randint(200_000_000, 800_000_000))
            )
    
    # Milestone archives (1-2.5GB)
    milestones = ['Alpha', 'Beta', 'Release']  # Reduced from 5 to 3 milestones
    for milestone in milestones:
        if random.random() < 0.3:  # 30% chance (reduced from 40%)
            archives.append(
                (f'Backups/{project_number}_{milestone}_{date}.zip',
                 random.randint(1_000_000_000, 2_500_000_000))
            )
    
    # Feature branches (300MB-1GB)
    features = ['feature_auth', 'feature_ui', 'feature_db']  # Reduced from 5 to 3 features
    for feature in features:
        if random.random() < 0.2:  # 20% chance (reduced from 25%)
            archives.append(
                (f'Backups/{project_number}_{feature}_{date}.zip',
                 random.randint(300_000_000, 1_000_000_000))
            )
    
    return archives

def get_project_files_by_technology(technologies):
    """Return typical files based on the project's technologies"""
    files = []
    
    # Common project files for all projects
    files.extend([
        ('README.md', 5_000),
        ('.gitignore', 1_000),
        ('LICENSE', 1_000),
        ('.env.example', 2_000),
        ('CHANGELOG.md', 3_000),
        ('docs/architecture.md', 15_000),
        ('docs/setup.md', 8_000),
        ('docs/api.md', 12_000),
        ('docs/deployment.md', 10_000),
        ('docs/diagrams/architecture.png', 500_000),
        ('docs/diagrams/data_flow.png', 400_000),
        ('.github/workflows/ci.yml', 2_000),
        ('.github/workflows/cd.yml', 2_500),
        ('.vscode/settings.json', 1_500),
    ])

    # Add project archives at the end
    project_number = 'P0000'  # This will be replaced with actual number
    files.extend([
        (f'Archives/README.md', 2_000),
        (f'Archives/.gitignore', 1_000),
    ])
    
    # Note: Actual archive files will be added when creating the directory
    
    if "Python" in technologies:
        files.extend([
            ('src/main.py', 50_000),
            ('src/utils.py', 30_000),
            ('src/config.py', 15_000),
            ('src/models/__init__.py', 1_000),
            ('src/models/base.py', 20_000),
            ('src/services/__init__.py', 1_000),
            ('src/services/auth.py', 25_000),
            ('src/api/__init__.py', 1_000),
            ('src/api/routes.py', 35_000),
            ('tests/__init__.py', 1_000),
            ('tests/test_main.py', 20_000),
            ('tests/test_utils.py', 15_000),
            ('tests/test_models.py', 25_000),
            ('tests/conftest.py', 10_000),
            ('requirements.txt', 2_000),
            ('requirements-dev.txt', 2_500),
            ('setup.py', 3_000),
            ('pyproject.toml', 1_500),
            ('Makefile', 2_000),
            ('.pylintrc', 1_000),
            ('pytest.ini', 500),
            ('.coverage', 5_000),
            ('coverage.xml', 8_000),
        ])

    if "JavaScript" in technologies:
        files.extend([
            ('src/utils/helpers.js', 15_000),
            ('src/utils/validation.js', 12_000),
            ('src/utils/formatting.js', 10_000),
            ('src/services/api.js', 20_000),
            ('src/services/auth.js', 18_000),
            ('tests/unit/helpers.test.js', 10_000),
            ('tests/integration/api.test.js', 15_000),
            ('package.json', 8_000),
            ('package-lock.json', 500_000),
            ('.eslintrc.js', 2_000),
            ('.prettierrc', 500),
            ('jest.config.js', 1_500),
            ('babel.config.js', 1_000),
        ])

    if "React" in technologies:
        files.extend([
            ('src/components/App.jsx', 15_000),
            ('src/components/Header/index.jsx', 8_000),
            ('src/components/Footer/index.jsx', 6_000),
            ('src/components/Sidebar/index.jsx', 10_000),
            ('src/components/common/Button.jsx', 5_000),
            ('src/components/common/Input.jsx', 6_000),
            ('src/components/common/Modal.jsx', 12_000),
            ('src/pages/Home.jsx', 10_000),
            ('src/pages/Dashboard.jsx', 15_000),
            ('src/pages/Profile.jsx', 12_000),
            ('src/context/AuthContext.jsx', 8_000),
            ('src/hooks/useAuth.js', 5_000),
            ('src/hooks/useForm.js', 6_000),
            ('src/styles/main.css', 25_000),
            ('src/styles/components.css', 20_000),
            ('src/styles/variables.css', 5_000),
            ('public/index.html', 5_000),
            ('public/favicon.ico', 15_000),
            ('public/manifest.json', 1_000),
            ('webpack.config.js', 3_000),
            ('tsconfig.json', 2_000),
        ])

    if "Angular" in technologies:
        files.extend([
            ('src/app/app.module.ts', 10_000),
            ('src/app/app.component.ts', 8_000),
            ('src/app/app.component.html', 5_000),
            ('src/app/components/header/header.component.ts', 7_000),
            ('src/app/components/footer/footer.component.ts', 6_000),
            ('src/app/services/auth.service.ts', 12_000),
            ('src/app/services/api.service.ts', 15_000),
            ('src/app/models/user.model.ts', 5_000),
            ('src/app/guards/auth.guard.ts', 4_000),
            ('src/assets/styles/main.scss', 20_000),
            ('src/environments/environment.ts', 2_000),
            ('src/environments/environment.prod.ts', 2_000),
            ('angular.json', 15_000),
            ('tsconfig.json', 3_000),
            ('tsconfig.app.json', 2_000),
            ('tsconfig.spec.json', 2_000),
        ])

    if any(cloud in technologies for cloud in ["AWS", "Azure", "GCP"]):
        files.extend([
            ('infrastructure/main.tf', 10_000),
            ('infrastructure/variables.tf', 5_000),
            ('infrastructure/outputs.tf', 3_000),
            ('infrastructure/modules/networking/main.tf', 8_000),
            ('infrastructure/modules/compute/main.tf', 12_000),
            ('infrastructure/modules/database/main.tf', 10_000),
            ('infrastructure/environments/prod/main.tf', 6_000),
            ('infrastructure/environments/staging/main.tf', 6_000),
            ('infrastructure/environments/dev/main.tf', 6_000),
            ('config/prod.yaml', 8_000),
            ('config/staging.yaml', 7_000),
            ('config/dev.yaml', 7_000),
            ('.terraform-version', 100),
            ('terraform.tfvars.example', 2_000),
        ])

    if "Docker" in technologies:
        files.extend([
            ('Dockerfile', 2_000),
            ('Dockerfile.dev', 1_800),
            ('docker-compose.yml', 3_000),
            ('docker-compose.dev.yml', 2_800),
            ('docker-compose.test.yml', 2_500),
            ('.dockerignore', 1_000),
            ('scripts/docker-entrypoint.sh', 1_500),
            ('scripts/wait-for-it.sh', 1_000),
            ('config/nginx/nginx.conf', 3_000),
            ('config/nginx/default.conf', 2_000),
        ])

    if "Kubernetes" in technologies:
        files.extend([
            ('k8s/deployment.yaml', 5_000),
            ('k8s/service.yaml', 2_000),
            ('k8s/ingress.yaml', 3_000),
            ('k8s/configmap.yaml', 2_500),
            ('k8s/secrets.yaml', 1_500),
            ('k8s/volumes.yaml', 2_000),
            ('k8s/autoscaling.yaml', 1_800),
            ('skaffold.yaml', 3_000),
            ('helm/Chart.yaml', 1_000),
            ('helm/values.yaml', 5_000),
            ('helm/templates/_helpers.tpl', 2_000),
        ])

    if "PyTorch" in technologies or "TensorFlow" in technologies:
        files.extend([
            # Source code files (5-50KB)
            ('models/model.py', 25_000),
            ('models/layers.py', 15_000),
            ('models/loss.py', 10_000),
            ('data/preprocessing.py', 20_000),
            ('data/dataset.py', 18_000),
            ('data/augmentation.py', 12_000),
            # Notebooks (1-5MB due to outputs)
            ('notebooks/training.ipynb', 3_000_000),
            ('notebooks/evaluation.ipynb', 2_500_000),
            ('notebooks/data_analysis.ipynb', 4_000_000),
            # Config files (1-5KB)
            ('configs/model_config.json', 3_000),
            ('configs/training_config.json', 2_500),
            ('configs/hyperparameters.yaml', 1_500),
            # Python scripts (5-20KB)
            ('scripts/train.py', 15_000),
            ('scripts/evaluate.py', 12_000),
            ('scripts/predict.py', 8_000),
            # Main model file
            ('models/pretrained/llama2_70b.pth', 15_000_000_000),  # 15GB
            # Vision model
            ('models/pretrained/stable_diffusion_xl_base.pth', 7_000_000_000),  # 7GB
            # Latest checkpoint
            (f'experiments/run_{get_random_date_2024()}/checkpoint_final.pth', 6_000_000_000),  # 6GB
            # Generated Data
            (f'outputs/generated_images_{get_random_date_2024()}.tar', 500_000_000),
            (f'outputs/synthetic_data_{get_random_date_2024()}.hdf5', 350_000_000),
        ])

    if "Adobe Creative Suite" in technologies:
        files.extend([
            # PSD files (typically 50-200MB for complex designs)
            ('designs/mockup.psd', 150_000_000),
            ('designs/mockup_mobile.psd', 80_000_000),
            ('designs/style_guide.psd', 50_000_000),
            # AI files (typically 20-100MB)
            ('assets/logos.ai', 30_000_000),
            ('assets/icons.ai', 20_000_000),
            ('assets/illustrations.ai', 45_000_000),
            # PDF exports (typically 5-20MB)
            ('exports/final_v2.pdf', 15_000_000),
            ('exports/presentations.pdf', 12_000_000),
            # XD files (typically 10-50MB)
            ('prototypes/mobile_app.xd', 25_000_000),
            ('prototypes/website.xd', 35_000_000),
        ])

    return files

def compress_file(file_path):
    """Compress a file using NTFS compression on Windows"""
    if platform.system().lower() == 'windows':
        try:
            # Use compact.exe for NTFS compression
            result = subprocess.run(
                ['compact', '/c', str(file_path)], 
                capture_output=True, 
                text=True,
                check=False  # Don't raise exception on non-zero return
            )
            if result.returncode != 0:
                print(f"Warning: Failed to compress {file_path}: {result.stderr.strip()}")
                return False
            return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"Warning: Compression not available for {file_path}: {e}")
            return False
    return False

def compress_directory(dir_path):
    """Enable NTFS compression on a directory and all its contents"""
    if platform.system().lower() == 'windows':
        try:
            # Use compact.exe with /s flag for recursive compression
            result = subprocess.run(
                ['compact', '/c', '/s', str(dir_path)], 
                capture_output=True, 
                text=True,
                check=False  # Don't raise exception on non-zero return
            )
            if result.returncode != 0:
                print(f"Warning: Failed to compress directory {dir_path}: {result.stderr.strip()}")
                return False
            return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"Warning: Directory compression not available for {dir_path}: {e}")
            return False
    return False

def create_user_directory(users_dir, username, technologies, role, user_data, company_data):
    # Create user's home directory
    user_dir = users_dir / username
    user_dir.mkdir(exist_ok=True)
    compress_directory(user_dir)
    
    # Create standard directories
    for dirname in ['Desktop', 'Documents', 'Downloads', 'Pictures', 'Videos']:
        dir_path = user_dir / dirname
        dir_path.mkdir(exist_ok=True)
        compress_directory(dir_path)
    
    # Create application directories based on technologies
    app_dirs = create_app_directories()
    for tech in technologies:
        if tech in app_dirs:
            dir_path = user_dir / app_dirs[tech]
            dir_path.mkdir(parents=True, exist_ok=True)
            compress_directory(dir_path)
    
    # Add AI model files for AI practitioners
    if is_ai_practitioner(role, technologies):
        ai_models_path = user_dir / 'Documents/AI/models'
        ai_models_path.mkdir(parents=True, exist_ok=True)
        create_typical_files(ai_models_path, get_ai_model_files())
        print(f"Created AI model files for {username}")
    
    # Add video production files for video editors
    if is_video_editor(role, technologies):
        video_path = user_dir / 'Documents/Adobe/Video Projects'
        video_path.mkdir(parents=True, exist_ok=True)
        create_typical_files(video_path, get_video_production_files())
        print(f"Created video production files for {username}")
    
    # Add development log files for developers
    if is_developer_role(role, technologies):
        dev_logs_path = user_dir / 'Documents/Development/logs'
        dev_logs_path.mkdir(parents=True, exist_ok=True)
        create_typical_files(dev_logs_path, get_dev_log_files())
        print(f"Created development logs for {username}")
                
    # Add VMware files for infrastructure-related roles
    vm_roles = {
        "Network Engineer",
        "Cloud Engineer",
        "Infrastructure Engineer",
        "DevOps Engineer",
        "Systems Administrator",
        "Security Engineer",
        "Infrastructure & DevOps Engineer",
        "Cloud Architect",
        "Site Reliability Engineer",
        "Platform Engineer"
    }
    if role in vm_roles:
        vmware_path = user_dir / 'Documents/Virtual Machines'
        vmware_path.mkdir(parents=True, exist_ok=True)
        
        # Get role-specific VM files
        vm_files = get_typical_files()['VMware'].copy()  # Start with base VMs
        
        # Add specialized VMs for network engineers
        if "Network Engineer" in role or "Infrastructure Engineer" in role:
            network_vms = [
                ('VMs/pfSense/pfSense_2.7.vmdk', 800_000_000),
                ('VMs/pfSense/pfSense_2.7.nvram', 8_000),
                ('VMs/OPNsense/OPNsense.vmdk', 1_000_000_000),
                ('VMs/VyOS/VyOS.vmdk', 500_000_000),
                ('VMs/Cisco_VIRL/IOSv.vmdk', 400_000_000),
                ('VMs/Cisco_VIRL/IOSvL2.vmdk', 450_000_000),
                ('VMs/Cisco_VIRL/IOS-XRv.vmdk', 1_200_000_000),
                ('VMs/GNS3_VM/GNS3_VM.vmdk', 4_000_000_000),
                ('VMs/EVE-NG/EVE-NG-Pro.vmdk', 4_500_000_000),
                ('Network_Labs/Lab1_OSPF/lab_topology.png', 500_000),
                ('Network_Labs/Lab2_BGP/lab_topology.png', 500_000),
                ('Network_Labs/Lab3_MPLS/lab_topology.png', 500_000),
            ]
            vm_files.extend(network_vms)
        
        # Add development-focused VMs
        if is_developer_role(role, technologies):
            dev_vms = [
                ('VMs/Jenkins_Server/jenkins_master.vmdk', 2_500_000_000),
                ('VMs/GitLab/gitlab_server.vmdk', 3_000_000_000),
                ('VMs/Kubernetes_Cluster/k8s_master.vmdk', 2_000_000_000),
                ('VMs/Kubernetes_Cluster/k8s_worker1.vmdk', 1_500_000_000),
                ('VMs/Kubernetes_Cluster/k8s_worker2.vmdk', 1_500_000_000),
                ('VMs/Docker_Host/docker_host.vmdk', 2_500_000_000),
                ('VMs/Dev_Environment/dev_ubuntu.vmdk', 3_500_000_000),
                ('VMs/Testing_Environment/test_ubuntu.vmdk', 3_000_000_000),
                ('Dev_Labs/CI_CD_Pipeline/pipeline_config.png', 250_000),
                ('Dev_Labs/Container_Cluster/cluster_diagram.png', 250_000),
            ]
            vm_files.extend(dev_vms)
        
        # Create all VM files
        create_typical_files(vmware_path, vm_files)

    # Create Projects directory for user's assigned projects
    if user_data and 'assigned_projects' in user_data:
        projects_path = user_dir / 'Projects'
        projects_path.mkdir(parents=True, exist_ok=True)
        
        # Get all projects data
        all_projects = company_data.get('projects', {}) if company_data else {}
        
        # Create directory for each assigned project
        for project_id in user_data['assigned_projects']:
            if project_id in all_projects:
                project = all_projects[project_id]
                project_number = project.get('number', 'unknown')
                project_name = project.get('name', 'unknown')
                project_dir = projects_path / project_number
                project_dir.mkdir(parents=True, exist_ok=True)
                
                # Create project files based on likely technologies
                project_files = get_project_files_by_technology(project['likely_technologies'])
                
                # Add project-specific archives
                project_archives = get_project_archives(project_number, project_name)
                project_files.extend(project_archives)
                
                create_typical_files(project_dir, project_files)
                
                print(f"Created project directory {project_number} for {username}")

def main():
    # Load company data
    company_data = load_company_data('company_data.json')
    
    # Create U: drive root
    u_drive = Path('U:')
    if not u_drive.exists():
        print("Note: Creating simulation in current directory as 'U_Drive' since we can't create actual U: drive")
        u_drive = Path('U_Drive')
    
    # Create Users directory
    users_dir = u_drive / 'Users'
    users_dir.mkdir(parents=True, exist_ok=True)
    
    # Enable compression on base directories
    compress_directory(u_drive)
    compress_directory(users_dir)
    
    # Process each user
    for user_id, user_data in company_data['users'].items():
        # Create sanitized username (firstname_lastname)
        name_parts = user_data['name'].lower().split()
        username = f"{name_parts[0]}_{name_parts[-1]}"
        
        # Always include current technologies
        technologies = set(user_data['current_technologies'])
        
        # Add some additional technologies
        likely_tech = user_data['likely_additional_technologies']
        num_additional = min(
            max(1, int(len(likely_tech) * 0.3)),  # Try to get 30%
            len(likely_tech)  # But don't exceed available technologies
        )
        selected_tech = random.sample(likely_tech, num_additional)
        technologies.update(selected_tech)
        
        # Create user's directory structure
        create_user_directory(users_dir, username, technologies, user_data['role'], user_data, company_data)
        print(f"Created directory structure for {username}")

if __name__ == "__main__":
    main()