import json
import random
import uuid
from typing import Dict, List, Set
import names
from faker import Faker
import numpy as np
from datetime import datetime, timedelta

# Initialize Faker for different locales
fake_ja = Faker('ja_JP')
fake_es = Faker('es')

# Japanese name mappings
JA_NAMES = {
    'first_names': {
        'Ken': '健',
        'Yuki': '優希',
        'Hiro': '浩',
        'Aki': '明',
        'Saki': '咲',
        'Mai': '麻衣',
        'Kai': '海',
        'Ryu': '竜',
        'Taro': '太郎',
        'Kenji': '健二',
        'Yuta': '裕太',
        'Kenta': '健太',
        'Yui': '結衣',
        'Miku': '美空',
        'Hana': '花'
    },
    'last_names': {
        'Tanaka': '田中',
        'Sato': '佐藤',
        'Suzuki': '鈴木',
        'Watanabe': '渡辺',
        'Yamamoto': '山本',
        'Nakamura': '中村',
        'Takahashi': '高橋',
        'Ito': '伊藤',
        'Saito': '斎藤',
        'Kobayashi': '小林',
        'Kato': '加藤',
        'Yoshida': '吉田',
        'Yamada': '山田',
        'Sasaki': '佐々木',
        'Yamaguchi': '山口'
    }
}

def generate_unique_name(used_names: Set[str], existing_usernames: Set[str], locale: str) -> str:
    """Generate a unique name for the given locale"""
    # Track username attempts for this name
    username = None
    while True:
        # Use region-appropriate names but ensure ASCII only
        if locale == 'ja':
            # Japanese-American names
            surnames = list(JA_NAMES['last_names'].keys())
            firstnames = list(JA_NAMES['first_names'].keys())
            name = f"{random.choice(firstnames)} {random.choice(surnames)}"
        elif locale == 'es':
            # Hispanic names with ASCII only
            surnames = ['Garcia', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez',
                       'Gonzalez', 'Perez', 'Sanchez', 'Ramirez', 'Torres']
            firstnames = ['Carlos', 'Miguel', 'Jose', 'Juan', 'Maria', 'Ana',
                          'Luis', 'Elena', 'Sofia', 'Isabella']
            name = f"{random.choice(firstnames)} {random.choice(surnames)}"
        else:
            name = f"{names.get_first_name()} {names.get_last_name()}"
        
        if name not in used_names:
            # Try to generate a username from this name
            username = generate_unique_username(name, existing_usernames)
            if username:
                used_names.add(name)
                return name
        # If we couldn't generate a unique username, try a different name

def generate_unique_username(name: str, existing_usernames: Set[str]) -> str:
    """Generate a unique username from a full name"""
    name_parts = name.lower().split()
    first, last = name_parts[0], name_parts[-1]
    
    # Try different combinations until we find a unique one
    username_attempts = [
        f"{first}_{last}",           # john_smith
        f"{first}.{last}",           # john.smith
        f"{first}{last}",            # johnsmith
        f"{first[0]}{last}",         # jsmith
        f"{first}{last[0]}",         # johns
        f"{last}_{first}",           # smith_john
        f"{first[:2]}{last}",        # josmith
        f"{first}{last[:2]}",        # johnsm
        f"{last}{first[:2]}",        # smithjo
        f"{first[:2]}{last[:2]}"     # josm
    ]
    
    for username in username_attempts:
        if username not in existing_usernames:
            existing_usernames.add(username)
            return username
    
    # If all attempts fail, modify the name generation instead
    return None

def get_technologies() -> Dict[str, List[str]]:
    """Define available technologies by category"""
    return {
        'Finance': [
            'SAP Finance', 'Oracle Financials', 'QuickBooks',
            'Excel Advanced', 'Power BI', 'Tableau',
            'NetSuite', 'Sage', 'Xero', 'Bloomberg Terminal',
            'ADP Payroll', 'Workday Financial'
        ],
        'Development': [
            'Python', 'Java', 'JavaScript', 'C#', 'Go',
            'React', 'Angular', 'Vue.js', 'Node.js',
            'Django', 'Flask', 'Spring Boot',
            'Docker', 'Kubernetes', 'Git'
        ],
        'Cloud': [
            'AWS', 'Azure', 'Google Cloud',
            'Docker', 'Kubernetes', 'Terraform',
            'CloudFormation', 'Lambda', 'EC2',
            'S3', 'RDS', 'DynamoDB'
        ],
        'Data Science': [
            'Python', 'R', 'TensorFlow',
            'PyTorch', 'Pandas', 'NumPy',
            'Scikit-learn', 'Jupyter',
            'SQL', 'Hadoop', 'Spark'
        ],
        'Analytics': [
            'Tableau', 'Power BI', 'Excel',
            'SQL', 'Python', 'R',
            'Google Analytics', 'Looker'
        ],
        'Security': [
            'Nessus', 'Wireshark', 'Metasploit',
            'Burp Suite', 'SIEM', 'IDS/IPS',
            'Firewall Configuration', 'Penetration Testing'
        ],
        'Business': [
            'Microsoft Office', 'Salesforce',
            'SAP', 'Oracle', 'Jira',
            'Confluence', 'SharePoint'
        ],
        'Engineering': [
            'AutoCAD', 'SolidWorks', 'MATLAB',
            'Ansys', 'Catia', 'Revit',
            'Fusion 360', 'LabVIEW', 'PTC Creo',
            'Civil 3D', 'Inventor'
        ],
        'Design': [
            'Adobe Creative Suite', 'Sketch',
            'Figma', 'InVision', 'Adobe XD',
            'Photoshop', 'Illustrator'
        ]
    }

def get_roles() -> Dict[str, Dict[str, List[str]]]:
    """Define roles and their likely technologies"""
    return {
        'Finance': {
            'roles': ['Financial Analyst', 'Accountant', 'Controller',
                     'Financial Manager', 'Budget Analyst', 'Payroll Specialist',
                     'Treasury Analyst', 'Tax Specialist'],
            'core_tech': ['Finance', 'Business'],
            'optional_tech': ['Analytics']
        },
        'Software Development': {
            'roles': ['Software Engineer', 'Senior Developer', 'Full Stack Developer', 
                     'Backend Developer', 'Frontend Developer', 'DevOps Engineer'],
            'core_tech': ['Development', 'Cloud'],
            'optional_tech': ['Data Science', 'Business']
        },
        'Data Science': {
            'roles': ['Data Scientist', 'ML Engineer', 'AI Researcher',
                     'Data Engineer', 'Research Scientist'],
            'core_tech': ['Data Science', 'Development'],
            'optional_tech': ['Cloud', 'Business']
        },
        'Design': {
            'roles': ['UI Designer', 'UX Designer', 'Graphic Designer',
                     'Product Designer', 'Creative Director'],
            'core_tech': ['Design'],
            'optional_tech': ['Business']
        },
        'Management': {
            'roles': ['Project Manager', 'Product Manager', 'Team Lead',
                     'Department Manager', 'Technical Lead'],
            'core_tech': ['Business'],
            'optional_tech': ['Development', 'Cloud', 'Analytics']
        },
        'HR': {
            'roles': ['HR Specialist', 'HR Manager', 'Recruiter',
                     'HR Director', 'Training Coordinator'],
            'core_tech': ['HR'],
            'optional_tech': ['Business']
        },
        'Sales': {
            'roles': ['Sales Representative', 'Account Manager', 'Sales Engineer',
                     'Sales Director', 'Business Development'],
            'core_tech': ['Business'],
            'optional_tech': ['Analytics']
        }
    }

def generate_user_problems() -> List[str]:
    """Generate a list of storage misuse problems"""
    return [
        "Large personal music collection (>100GB)",
        "Personal movie collection (>500GB)",
        "Personal photo library (>50GB)",
        "Cryptocurrency mining software detected",
        "Steam games installed on work drive",
        "Personal backup files",
        "Non-work video content",
        "Personal software collection",
        "Personal cloud sync folder (>100GB)",
        "Personal business files",
        "Personal financial records",
        "Personal tax documents",
        "Unauthorized media streaming setup",
        "Large personal email archives",
        "Personal virtual machine images"
    ]

def assign_user_problems(num_users: int) -> Dict[str, List[str]]:
    """Assign problems to a subset of users"""
    problems = generate_user_problems()
    user_problems = {}
    
    # About 20% of users will have some kind of problem
    problem_users = random.sample(range(num_users), int(num_users * 0.2))
    
    for user_id in problem_users:
        user_problems[str(user_id)] = []
        
        # Each problem user might have multiple issues
        num_problems = random.randint(1, 3)
        problem_categories = random.sample(list(problems.keys()), random.randint(1, len(problems.keys())))
        
        for _ in range(num_problems):
            category = random.choice(problem_categories)
            problem = random.choice(problems[category])
            if problem not in user_problems[str(user_id)]:
                user_problems[str(user_id)].append(problem)
    
    return user_problems

def get_project_types() -> Dict[str, Dict]:
    """Define project types and their characteristics"""
    return {
        'Finance': {
            'prefixes': ['Financial System', 'Budget Planning', 'Payroll', 'Tax Management'],
            'actions': ['Implementation', 'Upgrade', 'Integration', 'Automation'],
            'required_tech': ['Finance', 'Business'],
            'optional_tech': ['Analytics', 'Cloud'],
            'quota_gb': [100, 300]  # Financial data is relatively small
        },
        'Software Development': {
            'prefixes': ['Web Portal', 'Mobile App', 'Desktop Application', 'API Service'],
            'actions': ['Development', 'Modernization', 'Refactoring'],
            'required_tech': ['Development', 'Cloud'],
            'optional_tech': ['Data Science', 'Analytics'],
            'quota_gb': [2048, 4096]  # 2-4TB for dev environments, VMs, etc.
        },
        'Infrastructure': {
            'prefixes': ['Cloud Infrastructure', 'Network', 'Server', 'Data Center'],
            'actions': ['Migration', 'Upgrade', 'Implementation'],
            'required_tech': ['Cloud'],
            'optional_tech': ['Development'],
            'quota_gb': [200, 500]  # Range for infrastructure projects
        },
        'AI/ML': {
            'prefixes': ['Machine Learning', 'AI Model', 'Neural Network', 'Data Pipeline'],
            'actions': ['Development', 'Training', 'Optimization'],
            'required_tech': ['Data Science', 'Development'],
            'optional_tech': ['Cloud'],
            'quota_gb': [10240, 51200]  # 10-50TB for large AI models and datasets
        },
        'Security': {
            'prefixes': ['Security System', 'Authentication', 'Firewall'],
            'actions': ['Implementation', 'Upgrade', 'Assessment'],
            'required_tech': ['Security'],
            'optional_tech': ['Cloud', 'Development'],
            'quota_gb': [100, 300]  # Range for security projects
        },
        'Engineering': {
            'prefixes': ['CAD System', '3D Modeling', 'Simulation Engine'],
            'actions': ['Development', 'Implementation', 'Optimization'],
            'required_tech': ['Development', 'Engineering'],
            'optional_tech': ['Cloud'],
            'quota_gb': [3072, 5120]  # 3-5TB for CAD, simulations, ML models
        },
        'Business': {
            'prefixes': ['CRM', 'ERP', 'Analytics Dashboard'],
            'actions': ['Implementation', 'Integration', 'Optimization'],
            'required_tech': ['Business'],
            'optional_tech': ['Analytics', 'Cloud'],
            'quota_gb': [100, 200]  # Range for business projects
        },
        'Data Science': {
            'prefixes': ['ML Pipeline', 'Analytics Platform', 'Data Warehouse'],
            'actions': ['Implementation', 'Training', 'Optimization'],
            'required_tech': ['Data Science'],
            'optional_tech': ['Cloud', 'Development'],
            'quota_gb': [8192, 30720]  # 8-30TB for large datasets and model training
        },
        'Research': {
            'prefixes': ['Research Platform', 'Analysis Framework', 'Study System'],
            'actions': ['Development', 'Analysis', 'Implementation'],
            'required_tech': ['Data Science'],
            'optional_tech': ['Development', 'Cloud'],
            'quota_gb': [6144, 20480]  # 6-20TB for research data and model development
        }
    }

def generate_project_name() -> str:
    """Generate a realistic project name"""
    project_types = get_project_types()
    project_type = random.choice(list(project_types.keys()))
    type_info = project_types[project_type]
    
    actions = ['Migration', 'Implementation', 'Integration', 'Upgrade', 'Development',
              'Optimization', 'Deployment', 'Analysis', 'Redesign', 'Enhancement']
    phases = ['Phase 1', 'Phase 2', 'Phase 3', 'MVP', 'Beta', 'v2', '2.0']
    
    system = random.choice(type_info['prefixes'])
    action = random.choice(type_info['actions'] if type_info['actions'] else actions)
    
    if random.random() < 0.3:  # 30% chance to include phase
        return f"{system} {action} - {random.choice(phases)}", project_type
    return f"{system} {action}", project_type

def generate_project_dates():
    """Generate realistic project start and end dates between 2023-2024"""
    
    start = datetime(2023, 1, 1)
    end = datetime(2024, 12, 31)
    days_range = (end - start).days
    
    # Generate start date
    project_start = start + timedelta(days=random.randint(0, days_range))
    
    # Generate end date (if project is completed)
    # Projects typically last 3-12 months
    project_duration = timedelta(days=random.randint(90, 365))
    project_end = project_start + project_duration
    
    # Format dates as ISO strings
    start_date = project_start.isoformat()[:10]
    end_date = project_end.isoformat()[:10] if project_end <= end else None
    
    return start_date, end_date

def generate_project_status(end_date):
    """Generate project status based on end date and random factors"""
    if not end_date:
        return random.choice(['Active', 'On Hold'])
    
    # If project has end date, it's either Completed or Cancelled
    return random.choices(['Completed', 'Cancelled'], weights=[0.85, 0.15])[0]

def get_org_structure() -> Dict:
    """Define the organizational structure and roles"""
    return {
        'Executive': {
            'min_count': 3,
            'max_count': 5,
            'roles': {
                'Business': ['CEO', 'CFO', 'COO'],
                'Operations': ['CTO', 'CIO']
            },
            'max_per_role': 1,
            'reports_to': None
        },
        'Director': {
            'min_count': 4,
            'max_count': 8,
            'roles': {
                'IT': ['IT Director', 'Development Director'],
                'Engineering': ['Engineering Director'],
                'Operations': ['Operations Director'],
                'Finance': ['Finance Director', 'Treasury Director', 'Accounting Director']
            },
            'max_per_role': 1,
            'reports_to': 'Executive'
        },
        'Manager': {
            'min_count': 8,
            'max_count': 15,
            'roles': {
                'IT': ['Development Manager', 'Infrastructure Manager'],
                'Engineering': ['Project Manager', 'Product Manager'],
                'Operations': ['Operations Manager', 'Support Manager'],
                'Finance': ['Financial Manager', 'Accounting Manager', 
                          'Budget Manager', 'Payroll Manager']
            },
            'max_per_role': 2,
            'reports_to': 'Director'
        },
        'Individual': {
            'roles': {
                'Engineering': ['Senior Engineer', 'Software Engineer', 'DevOps Engineer'],
                'Development': ['Senior Developer', 'Developer', 'Junior Developer'],
                'Design': ['Senior Designer', 'UX Designer', 'UI Designer'],
                'Data': ['Data Scientist', 'Data Analyst', 'Database Administrator'],
                'Operations': ['Systems Administrator', 'Network Engineer', 'Support Specialist'],
                'Finance': ['Senior Financial Analyst', 'Financial Analyst', 
                          'Senior Accountant', 'Staff Accountant',
                          'Payroll Specialist', 'Tax Specialist',
                          'Treasury Analyst', 'Budget Analyst']
            },
            'reports_to': 'Manager'
        }
    }

def get_role_technologies(role: str, level: str, technologies: Dict[str, List[str]]) -> List[str]:
    """Get appropriate technologies for a given role and level"""
    tech_set = set()
    
    # Role-based technology mapping
    role_tech_map = {
        # Executive roles
        'CEO': ['Business'],
        'CTO': ['Business', 'Cloud', 'Development'],
        'CIO': ['Business', 'Cloud'],
        'CFO': ['Business'],
        'COO': ['Business'],
        'CISO': ['Business', 'Cloud'],
        
        # Director roles
        'IT Director': ['Business', 'Cloud'],
        'Engineering Director': ['Development', 'Cloud'],
        'Security Director': ['Cloud', 'Development'],
        'Operations Director': ['Business', 'Cloud'],
        'Development Director': ['Development', 'Cloud'],
        
        # Manager roles
        'Project Manager': ['Business'],
        'Development Manager': ['Development', 'Cloud'],
        'Infrastructure Manager': ['Cloud'],
        'Security Manager': ['Cloud', 'Development'],
        'Operations Manager': ['Cloud', 'Business'],
        'Team Lead': ['Development', 'Cloud'],
        
        # Individual roles
        'Software Engineer': ['Development'],
        'DevOps Engineer': ['Cloud', 'Development'],
        'Security Engineer': ['Development', 'Cloud'],
        'Frontend Developer': ['Development'],
        'Backend Developer': ['Development'],
        'Full Stack Developer': ['Development', 'Cloud'],
        'UI Designer': ['Design'],
        'UX Designer': ['Design'],
        'Graphic Designer': ['Design'],
        'Data Scientist': ['Data Science', 'Development'],
        'Data Engineer': ['Development', 'Data Science'],
        'Business Analyst': ['Business', 'Analytics'],
        'System Administrator': ['Cloud'],
        'Network Engineer': ['Cloud'],
        'Support Specialist': ['Business']
    }
    
    # Get technology categories for the role
    tech_categories = role_tech_map.get(role, ['Business'])
    
    # Add technologies from each relevant category
    for category in tech_categories:
        if category in technologies:
            # Leaders get fewer specific technologies
            if level in ['Executive', 'Director']:
                num_tech = max(1, int(len(technologies[category]) * 0.3))
            elif level == 'Manager':
                num_tech = max(1, int(len(technologies[category]) * 0.5))
            else:
                num_tech = max(2, int(len(technologies[category]) * 0.7))
            
            tech_set.update(random.sample(technologies[category], num_tech))
    
    return list(tech_set)

def assign_users_to_projects(users: Dict, projects: Dict) -> None:
    """Assign users to projects based on their roles and levels"""
    for project in projects.values():
        # Initialize project members
        project_members = []
        
        # Ensure each project has appropriate staffing:
        # 1. Project Manager/Lead
        managers = [uid for uid, user in users.items() 
                   if user['level'] in ['Manager', 'Director'] 
                   and len(user.get('assigned_projects', [])) < 3]  # Limit projects per manager
        if managers:
            project_manager = random.choice(managers)
            project_members.append(project_manager)
            users[project_manager].setdefault('assigned_projects', []).append(project['id'])
        
        # 2. Senior Developer/Engineer (1-2)
        seniors = [uid for uid, user in users.items()
                  if ('Senior' in user['role'] or user['level'] == 'Senior')
                  and 'Developer' in user['role']
                  and len(user.get('assigned_projects', [])) < 4]  # Limit projects per senior
        if seniors:
            num_seniors = min(2, len(seniors))
            for senior in random.sample(seniors, num_seniors):
                project_members.append(senior)
                users[senior].setdefault('assigned_projects', []).append(project['id'])
        
        # 3. Regular Developers (2-4)
        developers = [uid for uid, user in users.items()
                     if 'Developer' in user['role']
                     and 'Senior' not in user['role']
                     and 'Junior' not in user['role']
                     and len(user.get('assigned_projects', [])) < 3]
        if developers:
            num_devs = min(4, max(1, len(developers)))
            for dev in random.sample(developers, num_devs):
                project_members.append(dev)
                users[dev].setdefault('assigned_projects', []).append(project['id'])
        
        # 4. Junior Developers (0-2)
        juniors = [uid for uid, user in users.items()
                  if 'Junior' in user['role']
                  and len(user.get('assigned_projects', [])) < 2]  # Limit projects per junior
        if juniors:
            num_juniors = min(2, len(juniors))
            if num_juniors > 0:
                for junior in random.sample(juniors, num_juniors):
                    project_members.append(junior)
                    users[junior].setdefault('assigned_projects', []).append(project['id'])
        
        # 5. Other roles as needed (QA, Design, etc.)
        others = [uid for uid, user in users.items()
                 if any(role in user['role'] for role in ['QA', 'Designer', 'Architect'])
                 and len(user.get('assigned_projects', [])) < 3
                 and uid not in project_members]
        if others:
            num_others = min(2, len(others))
            if num_others > 0:
                for other in random.sample(others, num_others):
                    project_members.append(other)
                    users[other].setdefault('assigned_projects', []).append(project['id'])
        
        # Store project members
        project['assigned_users'] = project_members

def generate_company_data(num_users: int = 50, num_projects: int = 20) -> Dict:
    """Generate company data with the specified number of users and projects"""
    # Get required data structures
    org_structure = get_org_structure()
    technologies = get_technologies()
    project_types = get_project_types()
    
    users = {}
    assigned_roles = {level: [] for level in ['Executive', 'Director', 'Manager', 'Individual']}
    reporting_structure = {}
    used_names = set()
    existing_usernames = set()
    problems = generate_user_problems()
    
    # Calculate number of users at each level
    num_executives = max(1, int(num_users * 0.05))  # 5% executives
    num_directors = max(2, int(num_users * 0.10))   # 10% directors
    num_managers = max(3, int(num_users * 0.15))    # 15% managers
    num_individuals = num_users - (num_executives + num_directors + num_managers)
    
    # Generate executives first (small number)
    for _ in range(num_executives):
        user_id = str(uuid.uuid4())
        
        # Select department and role first
        department = random.choice(['Business', 'Operations'])
        role = random.choice(org_structure['Executive']['roles'][department])
        
        # Generate name with appropriate locale
        locale = random.choices(['en', 'ja', 'es'], weights=[0.6, 0.2, 0.2])[0]
        name = generate_unique_name(used_names, existing_usernames, locale)
        if not name:
            continue
        
        # Generate unique username
        username = generate_unique_username(name, existing_usernames)
        
        users[user_id] = {
            'name': name,
            'true_name': name,  # For English names
            'role': role,
            'level': 'Executive',
            'department': department,
            'current_technologies': get_role_technologies(role, 'Executive', technologies),
            'assigned_projects': [],
            'problems': random.sample(problems, random.randint(0, 2))
        }
        
        assigned_roles['Executive'].append(user_id)
    
    # Generate directors
    for _ in range(num_directors):
        user_id = str(uuid.uuid4())
        
        # Assign to an executive
        executive_id = random.choice(assigned_roles['Executive'])
        reporting_structure[user_id] = executive_id
        
        # Select department and role
        department = random.choice(['IT', 'Engineering', 'Operations', 'Finance'])
        role = random.choice(org_structure['Director']['roles'][department])
        
        locale = random.choices(['en', 'ja', 'es'], weights=[0.6, 0.2, 0.2])[0]
        name = generate_unique_name(used_names, existing_usernames, locale)
        if not name:
            continue
        
        users[user_id] = {
            'name': name,
            'true_name': name,
            'role': role,
            'level': 'Director',
            'department': department,
            'current_technologies': get_role_technologies(role, 'Director', technologies),
            'assigned_projects': [],
            'reports_to': executive_id
        }
        
        assigned_roles['Director'].append(user_id)
    
    # Generate managers
    for _ in range(num_managers):
        user_id = str(uuid.uuid4())
        
        # Assign to a director
        director_id = random.choice(assigned_roles['Director'])
        reporting_structure[user_id] = director_id
        
        # Select department and role
        department = random.choice(['IT', 'Engineering', 'Operations', 'Finance'])
        role = random.choice(org_structure['Manager']['roles'][department])
        
        locale = random.choices(['en', 'ja', 'es'], weights=[0.6, 0.2, 0.2])[0]
        name = generate_unique_name(used_names, existing_usernames, locale)
        if not name:
            continue
        
        users[user_id] = {
            'name': name,
            'true_name': name,
            'role': role,
            'level': 'Manager',
            'department': department,
            'current_technologies': get_role_technologies(role, 'Manager', technologies),
            'assigned_projects': [],
            'reports_to': director_id
        }
        
        assigned_roles['Manager'].append(user_id)
    
    # Generate individual contributors
    for _ in range(num_individuals):
        user_id = str(uuid.uuid4())
        
        # Get managers with the fewest direct reports
        manager_reports = {m: len([r for r, mr in reporting_structure.items() if mr == m]) 
                         for m in assigned_roles['Manager']}
        
        # Select manager with fewest reports
        manager_id = min(manager_reports, key=manager_reports.get)
        
        if manager_id:
            reporting_structure[user_id] = manager_id
            
            # Select department and role first
            department = random.choice(['Engineering', 'Development', 'Design', 'Data', 'Operations'])
            role = random.choice(org_structure['Individual']['roles'][department])
            
            locale = random.choices(['en', 'ja', 'es'], weights=[0.6, 0.2, 0.2])[0]
            name = generate_unique_name(used_names, existing_usernames, locale)
            if not name:
                continue
            
            # Generate true name in unicode using same locale
            if locale == 'ja':
                true_name = fake_ja.name()
            elif locale == 'es':
                # Convert the ASCII name to accented version
                name_map = {
                    'Jose': 'José',
                    'Maria': 'María',
                    'Angel': 'Ángel',
                    'Ramon': 'Ramón',
                    'Garcia': 'García',
                    'Rodriguez': 'Rodríguez',
                    'Martinez': 'Martínez',
                    'Hernandez': 'Hernández',
                    'Lopez': 'López',
                    'Gonzalez': 'González',
                    'Perez': 'Pérez',
                    'Sanchez': 'Sánchez',
                    'Ramirez': 'Ramírez'
                }
                true_name = name
                for ascii_name, accented_name in name_map.items():
                    true_name = true_name.replace(ascii_name, accented_name)
            else:
                true_name = name  # Use the same name for English names
            
            user_data = {
                'name': name,
                'true_name': true_name,
                'role': role,
                'level': 'Individual',
                'department': random.choice(['IT', 'Engineering', 'Operations', 'Business']),
                'current_technologies': get_role_technologies(role, 'Individual', technologies),
                'likely_additional_technologies': [],
                'assigned_projects': [],
                'reports_to': manager_id  # Ensure reports_to is set
            }
            
            users[user_id] = user_data
            assigned_roles['Individual'].append(user_id)
    
    # Generate projects
    projects = {}
    for _ in range(num_projects):
        project_name, project_type = generate_project_name()
        type_info = project_types[project_type]
        project_techs = set()
        
        # Define budget ranges by project type
        budget_ranges = {
            'AI/ML': (2000000, 10000000),      # $2M - $10M for AI/ML projects
            'Data Science': (1000000, 5000000), # $1M - $5M for Data Science
            'Research': (1000000, 4000000),     # $1M - $4M for Research
            'Engineering': (500000, 3000000),   # $500K - $3M for Engineering
            'Software Development': (200000, 1000000),  # $200K - $1M for Software
            'Infrastructure': (100000, 500000), # $100K - $500K for Infrastructure
            'Security': (100000, 400000),       # $100K - $400K for Security
            'Business': (50000, 200000),        # $50K - $200K for Business
            'Finance': (50000, 250000)          # $50K - $250K for Finance
        }
        
        # Get budget range for project type, default to $50K-$200K if type not found
        budget_range = budget_ranges.get(project_type, (50000, 200000))
        
        # Add required technologies
        for tech_category in type_info['required_tech']:
            tech_list = technologies[tech_category]
            num_tech = max(1, int(len(tech_list) * 0.5))  # Keep 50% of required tech
            project_techs.update(random.sample(tech_list, num_tech))
        
        # Add optional technologies
        for tech_category in type_info['optional_tech']:
            if random.random() < 0.5:  # 50% chance for optional tech
                tech_list = technologies[tech_category]
                num_tech = max(1, int(len(tech_list) * 0.3))  # Keep 30% of optional tech
                project_techs.update(random.sample(tech_list, num_tech))
        
        # Generate project dates and status
        start_date, end_date = generate_project_dates()
        status = generate_project_status(end_date)
        
        # Assign random users to project
        project_users = random.sample(list(users.keys()), random.randint(2, 5))
        project_id = str(uuid.uuid4())
        for user_id in project_users:
            users[user_id]['assigned_projects'].append(project_id)
        
        projects[project_id] = {
            'id': project_id,
            'name': project_name,
            'type': project_type,
            'department': random.choice(['IT', 'Engineering', 'Operations', 'Business']),
            'number': f"P{random.randint(1000, 9999)}",
            'assigned_users': project_users,
            'likely_technologies': list(project_techs),
            'start_date': start_date,
            'end_date': end_date,
            'status': status,
            'budget': random.randint(*budget_range),
            'priority': random.choice(['High', 'Medium', 'Low']),
            'complexity': random.choice(['High', 'Medium', 'Low']),
            'quota_gb': random.randint(*type_info['quota_gb'])  # Set quota based on project type
        }
    
    assign_users_to_projects(users, projects)
    
    return {
        'projects': projects,
        'users': users,
        'org_structure': {
            'executives': assigned_roles['Executive'],
            'reporting_structure': reporting_structure
        }
    }

def main():
    """Main function to generate new company data"""
    try:
        # Load existing data if it exists
        try:
            with open('company_data.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                print("\nLoaded existing company data")
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = None
            print("\nNo existing company data found")
        
        # Get project count from existing data or use default
        if existing_data and 'projects' in existing_data:
            new_project_count = len(existing_data['projects'])
        else:
            new_project_count = 20
        
        # Generate new company data with 100 users
        new_company_data = generate_company_data(num_users=100, num_projects=new_project_count)
        
        # Save the new data
        with open('company_data_new.json', 'w', encoding='utf-8') as f:
            json.dump(new_company_data, f, indent=2, ensure_ascii=False)
            print("\nSaved new company data to company_data_new.json")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 