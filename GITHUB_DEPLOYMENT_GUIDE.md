# 🚀 GitHub Deployment Guide

Complete guide to push this project to GitHub and deploy it.

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface
1. Go to https://github.com/new
2. Create repository name: `insurance-eligibility-classifier`
3. Add description: `AI-powered insurance eligibility prediction system`
4. Choose public or private
5. Skip initialization (we'll push existing code)
6. Click "Create repository"

### Option B: Using GitHub CLI
```bash
gh repo create insurance-eligibility-classifier --public
```

## Step 2: Prepare Local Repository

Navigate to project directory:
```bash
cd "/Users/ashishbathula/Desktop/gmu data "
```

Initialize git (if not already):
```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Step 3: Add Files to Git

```bash
# Add all files
git add .

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
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

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/

# Data
*.csv
*.xlsx

# OS
.DS_Store
Thumbs.db
EOF

git add .gitignore
```

## Step 4: Create Initial Commit

```bash
git add .
git commit -m "Initial commit: Insurance eligibility classifier with Streamlit app"
```

## Step 5: Push to GitHub

Get the repository URL from GitHub (format: `https://github.com/USERNAME/insurance-eligibility-classifier.git`)

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/insurance-eligibility-classifier.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## 🌐 Deploy to Streamlit Cloud (Recommended)

### 1. Connect GitHub Account to Streamlit
- Go to https://streamlit.io/cloud
- Sign up with GitHub
- Authorize Streamlit to access your repositories

### 2. Deploy App
1. Click "New app"
2. Select repository: `ashishbathulaab-lang/insurance-eligibility-classifier`
3. Select branch: `main`
4. Set main file path: `streamlit_app.py`
5. Click "Deploy"

Your app will be live at: `https://ashishbathulaab-lang-insurance-eligibility-classifier.streamlit.app`

### 3. App will auto-deploy on every push to main

## 🐳 Deploy to Docker Hub

### 1. Create Docker Account
- Go to https://hub.docker.com
- Sign up for free account

### 2. Build and Push Image
```bash
# Login to Docker
docker login

# Build image
docker build -t YOUR_USERNAME/insurance-classifier:latest .

# Push to Docker Hub
docker push YOUR_USERNAME/insurance-classifier:latest
```

### 3. Run from Docker Hub
```bash
docker run -p 8501:8501 ashishbathulaab-lang/insurance-classifier:latest
```

## ☁️ Deploy to Heroku (Alternative)

### 1. Create Heroku Account
- Go to https://www.heroku.com
- Sign up for free

### 2. Install Heroku CLI
```bash
brew tap heroku/brew && brew install heroku
```

### 3. Deploy
```bash
# Login
heroku login

# Create app
heroku create insurance-eligibility-classifier

# Add Procfile
cat > Procfile << 'EOF'
web: streamlit run streamlit_app.py --logger.level=debug --client.logger.level=debug --server.port=$PORT --server.address=0.0.0.0
EOF

git add Procfile
git commit -m "Add Procfile for Heroku"

# Deploy
git push heroku main
```

## 🔗 API Deployment Options

### Option 1: Render (Free Tier)
1. Go to https://render.com
2. Connect GitHub
3. New Web Service
4. Select repository
5. Runtime: Python
6. Build command: `pip install -r requirements.txt`
7. Start command: `python api.py`
8. Deploy

### Option 2: Railway
1. Go to https://railway.app
2. Connect GitHub
3. Select repository
4. Railway auto-detects Python
5. Set start command: `python api.py`
6. Deploy

### Option 3: AWS Elastic Beanstalk
```bash
pip install awsebcli
eb init -p python-3.9 insurance-classifier
eb create insurance-classifier-env
eb deploy
```

## 📝 GitHub README Tips

Make your README stand out:
- Add badges (build, license, etc.)
- Include GIF/screenshots of web app
- Add example usage
- List deployment options
- Include quick start guide

Example badges:
```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ashishbathulaab-lang-insurance-eligibility-classifier.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

## 🔒 Protect Main Branch

In GitHub Settings:
1. Go to Settings → Branches
2. Add branch protection rule for `main`
3. Require pull request reviews
4. Require status checks

## 📊 Add GitHub Actions CI/CD

Create `.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10']
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run tests
      run: pytest
```

## 🎯 Project Links

After deployment, share these links:

- **Web App**: https://ashishbathulaab-lang-insurance-eligibility-classifier.streamlit.app
- **GitHub**: https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier
- **Docker**: https://hub.docker.com/r/ashishbathulaab-lang/insurance-classifier
- **API**: https://insurance-classifier-api.herokuapp.com (if deployed)

## 📈 Monitor Deployments

### Streamlit Cloud Analytics
- Visit dashboard to see usage stats
- Monitor app performance
- View error logs

### GitHub Issues & Discussions
- Enable Discussions tab
- Encourage user feedback
- Track bugs and feature requests

## 🔄 Update & Maintenance

To push updates:
```bash
# Make changes to code
# Commit and push
git add .
git commit -m "Update model accuracy"
git push origin main

# All platforms auto-deploy!
```

## 🆘 Troubleshooting

### Streamlit app not loading models
- Ensure model.pkl, scaler.pkl, features.pkl in root directory
- Check file paths in streamlit_app.py
- Verify pickle compatibility

### Docker build fails
- Ensure all required packages in requirements.txt
- Check Python version compatibility
- Verify model files included in Docker context

### Heroku deployment fails
- Increase dyno size if memory error
- Check Procfile syntax
- View logs: `heroku logs --tail`

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/deploy)
- [GitHub Actions Guide](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Heroku Deployment](https://devcenter.heroku.com/articles/getting-started-with-python)

---

**You're all set! Push your project and enjoy!** 🎉
