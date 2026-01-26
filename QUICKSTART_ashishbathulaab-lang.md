# 🚀 YOUR DEPLOYMENT QUICKSTART

**GitHub Username:** `ashishbathulaab-lang`  
**Email:** `ashishbathula.ab@gmail.com`  
**Repository:** `insurance-eligibility-classifier`

---

## ⚡ FASTEST DEPLOYMENT (3 Commands)

```bash
# 1. Make the deployment script executable and run it
chmod +x DEPLOY_NOW.sh
./DEPLOY_NOW.sh

# 2. Create repository at https://github.com/new with name:
#    insurance-eligibility-classifier

# 3. Push to GitHub
git push -u origin main
```

---

## 📲 COPY-PASTE READY COMMANDS

### Option A: Step-by-Step Manual

```bash
# Step 1: Export model
python3 export_model.py

# Step 2: Initialize git
git init
git config user.email "ashishbathula.ab@gmail.com"
git config user.name "ashishbathula"

# Step 3: Commit everything
git add .
git commit -m "Insurance eligibility classifier - ML pipeline"

# Step 4: Setup remote
git branch -M main
git remote add origin https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier.git

# Step 5: Push to GitHub
git push -u origin main
```

### Option B: One-Liner (Requires model already exported)

```bash
git init && git config user.email "ashishbathula.ab@gmail.com" && git config user.name "ashishbathula" && git add . && git commit -m "Insurance eligibility classifier" && git branch -M main && git remote add origin https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier.git && git push -u origin main
```

---

## 🌐 STREAMLIT CLOUD DEPLOYMENT (After git push)

1. Visit: **https://streamlit.io/cloud**
2. Click **"New app"**
3. Select your GitHub account
4. Repository: **ashishbathulaab-lang/insurance-eligibility-classifier**
5. Main file: **streamlit_app.py**
6. Click **Deploy**

✅ **Live App:** https://ashishbathulaab-lang-insurance-eligibility-classifier.streamlit.app

---

## 🐳 DOCKER DEPLOYMENT (Optional)

```bash
# Build image
docker build -t ashishbathulaab-lang/insurance-classifier:latest .

# Push to Docker Hub (requires login)
docker login
docker push ashishbathulaab-lang/insurance-classifier:latest

# Run locally
docker run -p 8501:8501 ashishbathulaab-lang/insurance-classifier:latest
```

---

## 📊 WHAT GETS DEPLOYED

✅ **Web App** (Streamlit) - Interactive predictions  
✅ **REST API** (Flask) - JSON predictions  
✅ **Python Module** - Import in your code  
✅ **Full Documentation** - 7 markdown files  
✅ **Docker Container** - For deployment  

---

## 🔗 YOUR GITHUB URLS

- **Repository:** https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier
- **Web App:** https://ashishbathulaab-lang-insurance-eligibility-classifier.streamlit.app
- **Docker Hub:** https://hub.docker.com/r/ashishbathulaab-lang/insurance-classifier
- **Issues:** https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier/issues
- **Pull Requests:** https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier/pulls

---

## ⚠️ BEFORE YOU PUSH

Checklist:
- [ ] Run `python3 export_model.py` (creates .pkl files)
- [ ] Verify `ls -la model.pkl scaler.pkl features.pkl` (all exist)
- [ ] Create GitHub repo at https://github.com/new
- [ ] Name it: `insurance-eligibility-classifier`
- [ ] Copy the HTTPS clone link from GitHub

---

## 🆘 TROUBLESHOOTING

**Q: "fatal: remote origin already exists"**  
A: Run: `git remote remove origin` then retry

**Q: "Permission denied: DEPLOY_NOW.sh"**  
A: Run: `chmod +x DEPLOY_NOW.sh` then `./DEPLOY_NOW.sh`

**Q: "export_model.py failed"**  
A: Make sure you have all dependencies:  
`pip install scikit-learn pandas numpy matplotlib seaborn`

**Q: Git authentication fails**  
A: Use GitHub Personal Access Token:  
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

---

**Generated:** January 26, 2026  
**Status:** ✅ Ready for Production
