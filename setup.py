#!/usr/bin/env python3
"""
Setup script for Insurance Eligibility Prediction System
Exports model from Jupyter notebook and prepares for deployment
"""

import os
import sys
import pickle
import subprocess
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    dirs = [
        'models',
        'app/templates',
        'app/static',
        'tests',
        'docs'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def create_sample_model():
    """Create placeholder model and scaler files"""
    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.linear_model import LogisticRegression
    
    models_dir = Path('models')
    
    # Check if models already exist
    if (models_dir / 'insurance_model.pkl').exists() and \
       (models_dir / 'minmax_scaler.pkl').exists():
        print("✓ Model files already exist")
        return
    
    print("\n⚠️  Creating sample model files...")
    print("   (Replace with trained models from Jupyter notebook)")
    
    # Create dummy scaler
    dummy_X = np.array([
        [45.5, 1.0, 15, 8, 6],
        [35.2, 1.0, 10, 5, 3]
    ])
    
    scaler = MinMaxScaler()
    scaler.fit(dummy_X)
    
    with open(models_dir / 'minmax_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print(f"✓ Created {models_dir / 'minmax_scaler.pkl'}")
    
    # Create dummy model
    X_scaled = scaler.transform(dummy_X)
    y = np.array([1, 1])
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y)
    
    with open(models_dir / 'insurance_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Created {models_dir / 'insurance_model.pkl'}")
    
    print("\n⚠️  IMPORTANT:")
    print("   Run the Jupyter notebook to train the real model")
    print("   Then replace these sample files with trained models")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # For local setup
        if os.path.exists('app/requirements.txt'):
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'app/requirements.txt'
            ])
            print("✓ Dependencies installed")
        else:
            print("⚠️  requirements.txt not found, skipping pip install")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Flask
instance/
.webassets-cache

# Environment variables
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# macOS
.DS_Store

# Logs
*.log
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")

def create_example_env():
    """Create example .env file"""
    env_content = """# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Model Paths
MODEL_PATH=models/insurance_model.pkl
SCALER_PATH=models/minmax_scaler.pkl

# API Configuration
API_PORT=5000
API_HOST=0.0.0.0
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_content)
    print("✓ Created .env.example")

def create_license():
    """Create MIT License"""
    license_content = """MIT License

Copyright (c) 2026 Insurance Eligibility Predictor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"""
    
    with open('LICENSE', 'w') as f:
        f.write(license_content)
    print("✓ Created LICENSE")

def main():
    """Run setup"""
    print("=" * 60)
    print("Insurance Eligibility Prediction System - Setup")
    print("=" * 60)
    
    print("\n🔧 Setting up project structure...")
    create_directories()
    
    print("\n📄 Creating configuration files...")
    create_gitignore()
    create_example_env()
    create_license()
    
    print("\n🤖 Setting up model files...")
    create_sample_model()
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("\n1. Train the Model:")
    print("   - Open: Insurance_Eligibility_Classification.ipynb")
    print("   - Run all cells")
    print("   - Models will be saved to models/ directory")
    
    print("\n2. Install Dependencies (if not already done):")
    print("   pip install -r app/requirements.txt")
    
    print("\n3. Run the Application:")
    print("   python app/api.py")
    print("   Then open: http://localhost:5000")
    
    print("\n4. Deploy to GitHub:")
    print("   - Create repository on GitHub")
    print("   - Follow instructions in app/GITHUB_SETUP.md")
    
    print("\n5. Deploy to Production:")
    print("   - Docker: docker build -t insurance-predictor . && docker run -p 5000:5000 insurance-predictor")
    print("   - Heroku: heroku create app-name && git push heroku main")
    
    print("\n📚 Documentation:")
    print("   - API Docs: app/README.md")
    print("   - GitHub Setup: app/GITHUB_SETUP.md")
    print("   - Algorithm Details: ../ALGORITHM_DOCUMENTATION.md")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
