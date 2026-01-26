#!/bin/bash

# 🚀 Insurance Eligibility Classifier - Deployment Script
# Author: ashishbathulaab-lang
# Email: ashishbathula.ab@gmail.com
# Created: January 26, 2026

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Insurance Eligibility Classifier - Deployment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Repository: ashishbathulaab-lang/insurance-eligibility-classifier"
echo "Email: ashishbathula.ab@gmail.com"
echo ""

# Step 1: Export Model
echo "✅ Step 1: Exporting trained model..."
echo "   Running: python3 export_model.py"
echo ""
python3 export_model.py

if [ $? -eq 0 ]; then
    echo "✅ Model exported successfully"
else
    echo "❌ Model export failed. Please check export_model.py"
    exit 1
fi

echo ""

# Step 2: Verify Files
echo "✅ Step 2: Verifying model files..."
if [ -f "model.pkl" ] && [ -f "scaler.pkl" ] && [ -f "features.pkl" ]; then
    echo "   ✅ All model files created:"
    ls -lh *.pkl
else
    echo "❌ Some model files are missing"
    exit 1
fi

echo ""

# Step 3: Initialize Git
echo "✅ Step 3: Initializing Git repository..."
if [ -d ".git" ]; then
    echo "   ℹ️  Git repository already initialized"
else
    git init
    echo "   ✅ Git repository initialized"
fi

# Step 4: Configure Git
echo "✅ Step 4: Configuring Git user..."
git config user.email "ashishbathula.ab@gmail.com"
git config user.name "ashishbathula"
echo "   ✅ Git user configured"

echo ""

# Step 5: Add Files
echo "✅ Step 5: Adding files to Git..."
git add .
echo "   ✅ Files added"

echo ""

# Step 6: Commit
echo "✅ Step 6: Creating commit..."
git commit -m "Insurance eligibility classifier - Complete ML pipeline with MinMax scaling and Logistic Regression"
echo "   ✅ Commit created"

echo ""

# Step 7: Setup Remote
echo "✅ Step 7: Setting up GitHub remote..."
if git remote get-url origin &> /dev/null; then
    echo "   ℹ️  Remote 'origin' already exists"
    git remote remove origin
    echo "   ✅ Old remote removed"
fi

git branch -M main
git remote add origin https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier.git
echo "   ✅ Remote added: https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier.git"

echo ""

# Step 8: Ready to Push
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ALL SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. CREATE GITHUB REPOSITORY"
echo "   • Go to: https://github.com/new"
echo "   • Repository name: insurance-eligibility-classifier"
echo "   • Description: ML pipeline for insurance eligibility prediction"
echo "   • Click 'Create repository'"
echo ""
echo "2. PUSH TO GITHUB"
echo "   git push -u origin main"
echo ""
echo "3. DEPLOY TO STREAMLIT CLOUD (Recommended)"
echo "   • Go to: https://streamlit.io/cloud"
echo "   • Sign in with GitHub account"
echo "   • Click 'New app'"
echo "   • Select: ashishbathulaab-lang/insurance-eligibility-classifier"
echo "   • Set main file: streamlit_app.py"
echo "   • Click 'Deploy'"
echo ""
echo "   Your app will be live at:"
echo "   🌐 https://ashishbathulaab-lang-insurance-eligibility-classifier.streamlit.app"
echo ""
echo "4. (OPTIONAL) TEST LOCALLY"
echo "   streamlit run streamlit_app.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
