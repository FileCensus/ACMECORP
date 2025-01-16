import json
import os
from pathlib import Path
import random
import subprocess
import platform
import datetime
import hashlib

def load_company_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_random_date_between(start_date_str, end_date_str):
    """Generate a random date between start and end dates"""
    start = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    days_between = (end - start).days
    random_days = random.randint(0, days_between)
    return start + datetime.timedelta(days=random_days)

def set_file_dates(file_path, start_date, end_date):
    """Set consistent modification and access times for a file"""
    # Use defaults if dates are missing
    if not start_date or not end_date:
        current_year = datetime.datetime.now().year
        start_date = f"{current_year-1}-01-01"
        end_date = f"{current_year+1}-12-31"
    
    date = get_random_date_between(start_date, end_date)
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
        return True
    except Exception as e:
        print(f"Error creating file {file_path}: {e}")
        return False

def get_project_files_by_technology(technologies):
    """Return typical files based on the technologies used"""
    files = []
    
    # Common project files regardless of technology
    base_files = [
        ('README.md', 50_000),
        ('docs/architecture.pdf', 25_000_000),
        ('docs/requirements.docx', 15_000_000),
        ('docs/api_spec.yaml', 2_000_000),
        ('docs/design.vsdx', 18_000_000),
        ('docs/project_plan.mpp', 12_000_000),
        ('.gitignore', 10_000),
        ('LICENSE', 20_000),
        ('CHANGELOG.md', 100_000)
    ]
    
    files.extend(base_files)
    
    for tech in technologies:
        if tech in ['Python', 'Django', 'Flask']:
            files.extend([
                ('src/main.py', 2_500_000),
                ('src/utils.py', 1_500_000),
                ('src/config.py', 800_000),
                ('src/models.py', 3_000_000),
                ('src/views.py', 4_000_000),
                ('src/api.py', 2_500_000),
                ('src/services/', 0),
                ('src/middleware/', 0),
                ('tests/unit/', 0),
                ('tests/integration/', 0),
                ('tests/test_main.py', 1_500_000),
                ('tests/test_utils.py', 1_000_000),
                ('tests/test_models.py', 2_000_000),
                ('tests/test_views.py', 2_500_000),
                ('requirements.txt', 50_000),
                ('requirements-dev.txt', 60_000),
                ('docker/Dockerfile', 25_000),
                ('docker/docker-compose.yml', 35_000),
                ('.env.example', 15_000),
                ('scripts/setup.sh', 20_000),
                ('scripts/deploy.sh', 25_000),
                ('logs/app.log', 50_000_000)
            ])
        elif tech in ['Java', 'Spring']:
            files.extend([
                ('src/main/java/com/company/app/', 0),
                ('src/main/java/com/company/app/Application.java', 2_500_000),
                ('src/main/java/com/company/app/config/', 0),
                ('src/main/java/com/company/app/model/', 0),
                ('src/main/java/com/company/app/repository/', 0),
                ('src/main/java/com/company/app/service/', 0),
                ('src/main/java/com/company/app/controller/', 0),
                ('src/main/resources/application.properties', 250_000),
                ('src/main/resources/application-dev.properties', 200_000),
                ('src/main/resources/logback.xml', 150_000),
                ('src/test/java/com/company/app/', 0),
                ('src/test/resources/', 0),
                ('target/app.jar', 85_000_000),
                ('target/app-sources.jar', 45_000_000),
                ('target/app-javadoc.jar', 35_000_000),
                ('pom.xml', 500_000),
                ('mvnw', 85_000),
                ('mvnw.cmd', 85_000),
                ('.mvn/wrapper/', 0),
                ('logs/spring.log', 75_000_000)
            ])
        elif tech in ['JavaScript', 'React', 'Angular']:
            files.extend([
                ('src/app.js', 3_000_000),
                ('src/components/', 0),
                ('src/containers/', 0),
                ('src/services/', 0),
                ('src/utils/', 0),
                ('src/assets/', 0),
                ('src/styles/', 0),
                ('public/index.html', 25_000),
                ('public/favicon.ico', 150_000),
                ('dist/bundle.js', 25_000_000),
                ('dist/bundle.js.map', 45_000_000),
                ('dist/vendor.js', 85_000_000),
                ('dist/styles.css', 2_500_000),
                ('node_modules/', 0),
                ('package.json', 250_000),
                ('package-lock.json', 15_000_000),
                ('webpack.config.js', 150_000),
                ('babel.config.js', 50_000),
                ('jest.config.js', 45_000),
                ('cypress/integration/', 0),
                ('coverage/lcov-report/', 0)
            ])
        elif tech in ['C#', '.NET']:
            files.extend([
                ('src/Program.cs', 2_500_000),
                ('src/Startup.cs', 3_500_000),
                ('src/appsettings.json', 250_000),
                ('src/appsettings.Development.json', 200_000),
                ('src/Controllers/', 0),
                ('src/Models/', 0),
                ('src/Services/', 0),
                ('src/Middleware/', 0),
                ('tests/UnitTests/', 0),
                ('tests/IntegrationTests/', 0),
                ('bin/Release/net6.0/app.dll', 45_000_000),
                ('bin/Release/net6.0/app.exe', 65_000_000),
                ('bin/Release/net6.0/app.pdb', 35_000_000),
                ('obj/Release/', 0),
                ('.vs/', 0),
                ('app.csproj', 150_000),
                ('app.sln', 50_000),
                ('nuget.config', 25_000)
            ])
        elif tech in ['Machine Learning', 'TensorFlow', 'PyTorch']:
            files.extend([
                ('models/model_v1.h5', 850_000_000),
                ('models/model_v2.h5', 950_000_000),
                ('models/checkpoints/', 0),
                ('data/raw/', 0),
                ('data/processed/', 0),
                ('data/training.csv', 1_500_000_000),
                ('data/validation.csv', 500_000_000),
                ('data/test.csv', 250_000_000),
                ('notebooks/EDA.ipynb', 25_000_000),
                ('notebooks/Training.ipynb', 35_000_000),
                ('notebooks/Evaluation.ipynb', 28_000_000),
                ('notebooks/Visualization.ipynb', 45_000_000),
                ('src/preprocessing.py', 2_500_000),
                ('src/model.py', 3_500_000),
                ('src/train.py', 2_800_000),
                ('src/evaluate.py', 2_200_000),
                ('logs/tensorboard/', 0),
                ('logs/training.log', 150_000_000),
                ('requirements-gpu.txt', 75_000)
            ])
            if tech in ['Cloud', 'AWS', 'Azure']:
                files.extend([
                    ('terraform/', 0),
                    ('terraform/main.tf', 1_500_000),
                    ('terraform/variables.tf', 500_000),
                    ('terraform/outputs.tf', 250_000),
                    ('cloudformation/template.yaml', 2_500_000),
                    ('kubernetes/deployments/', 0),
                    ('kubernetes/services/', 0),
                    ('kubernetes/config-maps/', 0),
                    ('ansible/playbooks/', 0),
                    ('ansible/inventory/', 0),
                    ('scripts/deploy.sh', 150_000),
                    ('scripts/backup.sh', 120_000),
                    ('monitoring/grafana/', 0),
                    ('monitoring/prometheus/', 0),
                    ('.aws/config', 15_000),
                    ('azure-pipelines.yml', 85_000)
                ])
        elif tech in ['Cloud', 'AWS', 'Azure']:
            files.extend([
                ('terraform/', 0),
                ('terraform/main.tf', 1_500_000),
                ('terraform/variables.tf', 500_000),
                ('terraform/outputs.tf', 250_000),
                ('cloudformation/template.yaml', 2_500_000),
                ('kubernetes/deployments/', 0),
                ('kubernetes/services/', 0),
                ('kubernetes/config-maps/', 0),
                ('ansible/playbooks/', 0),
                ('ansible/inventory/', 0),
                ('scripts/deploy.sh', 150_000),
                ('scripts/backup.sh', 120_000),
                ('monitoring/grafana/', 0),
                ('monitoring/prometheus/', 0),
                ('.aws/config', 15_000),
                ('azure-pipelines.yml', 85_000)
            ])
    
    return files

def get_management_files_by_department(department, technologies):
    """Return typical management files based on department and technologies"""
    files = []
    
    base_files = [
        ('Reports/quarterly_summary.pptx', 15_000_000),
        ('Reports/annual_review.docx', 8_000_000),
        ('Planning/roadmap.xlsx', 5_000_000)
    ]
    
    if department == 'IT':
        files.extend([
            ('Infrastructure/network_diagram.vsdx', 20_000_000),
            ('Security/security_audit.pdf', 12_000_000),
            ('Systems/inventory.xlsx', 8_000_000)
        ])
    elif department == 'Engineering':
        files.extend([
            ('Architecture/system_design.vsdx', 25_000_000),
            ('Standards/coding_guidelines.pdf', 10_000_000),
            ('Reviews/code_review_template.docx', 5_000_000)
        ])
    elif department == 'Operations':
        files.extend([
            ('Procedures/sop.pdf', 15_000_000),
            ('Monitoring/dashboard_config.json', 2_000_000),
            ('Incidents/report_template.docx', 5_000_000)
        ])
    
    # Add technology-specific files
    for tech in technologies:
        if tech in ['Machine Learning', 'AI']:
            files.extend([
                ('Models/performance_metrics.xlsx', 10_000_000),
                ('Data/validation_results.csv', 20_000_000)
            ])
        elif tech in ['Cloud', 'AWS', 'Azure']:
            files.extend([
                ('Cloud/architecture.vsdx', 15_000_000),
                ('Cloud/cost_analysis.xlsx', 8_000_000)
            ])
    
    return base_files + files

def simulate_g_drive():
    """Simulate G drive structure with project and management files"""
    try:
        # Load company data
        try:
            company_data = load_company_data('company_data.json')
            print(f"\nLoaded company data with {len(company_data['users'])} users and {len(company_data['projects'])} projects")
        except FileNotFoundError:
            print("Error: company_data.json not found. Please run generate_new_company.py first.")
            return
        except json.JSONDecodeError:
            print("Error: company_data.json is not valid JSON. Please check the file.")
            return
        except UnicodeDecodeError:
            print("Error: company_data.json contains invalid characters. Please ensure it's saved as UTF-8.")
            return
        
        # Validate project dates
        current_year = datetime.datetime.now().year
        default_start = f"{current_year-1}-01-01"
        default_end = f"{current_year+1}-12-31"
        
        for project_id, project in company_data['projects'].items():
            if not project.get('start_date'):
                print(f"Warning: Project {project.get('number', 'unknown')} missing start_date, using default")
                project['start_date'] = default_start
            if not project.get('end_date'):
                print(f"Warning: Project {project.get('number', 'unknown')} missing end_date, using default")
                project['end_date'] = default_end
        
        # Create G: drive root
        g_drive = Path('G:')
        if not g_drive.exists():
            print("Note: Creating simulation in current directory as 'G_Drive' since we can't create actual G: drive")
            g_drive = Path('G_Drive')
        
        # Create main directories
        projects_dir = g_drive / 'Projects'
        management_dir = g_drive / 'Management'
        projects_dir.mkdir(parents=True, exist_ok=True)
        management_dir.mkdir(parents=True, exist_ok=True)
        
        # Process each project
        print("\nPopulating project directories...")
        for project_id, project in company_data['projects'].items():
            project_number = project.get('number', 'unknown')
            project_dir = projects_dir / project_number
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Calculate maximum allowed size (50-80% of quota)
            quota_bytes = project['quota_gb'] * 1024 * 1024 * 1024
            max_size = int(quota_bytes * random.uniform(0.5, 0.8))
            current_size = 0
            
            # Get project files based on technologies
            project_files = get_project_files_by_technology(project['likely_technologies'])
            
            # Create project files
            for file_path, size in project_files:
                if current_size + size > max_size:
                    continue
                    
                full_path = project_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                if size > 0:  # Skip directories (size = 0)
                    if create_large_file(full_path, size):
                        current_size += size
                        # Set file date within project timeline
                        set_file_dates(full_path, project['start_date'], project['end_date'])
            
            print(f"Created project files for {project_number}: {current_size / (1024*1024*1024):.2f}GB of {project['quota_gb']}GB quota")
        
        # Process management directories
        print("\nPopulating management directories...")
        for dept, users in get_department_users(company_data).items():
            dept_dir = management_dir / dept
            dept_dir.mkdir(parents=True, exist_ok=True)
            
            # Collect all technologies used in department
            dept_technologies = set()
            for user in users:
                dept_technologies.update(user['current_technologies'])
            
            # Get and create management files
            mgmt_files = get_management_files_by_department(dept, dept_technologies)
            for file_path, size in mgmt_files:
                full_path = dept_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                if create_large_file(full_path, size):
                    # Set file date within last year
                    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
                    set_file_dates(full_path, start_date, end_date)
            
            print(f"Created management files for {dept}")
    except Exception as e:
        print(f"Error simulating G drive: {e}")

def get_department_users(company_data):
    """Group users by department"""
    departments = {}
    for user in company_data['users'].values():
        dept = user.get('department', 'Other')
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(user)
    return departments

if __name__ == "__main__":
    simulate_g_drive() 