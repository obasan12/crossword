#!/bin/bash

# Setup script for GitHub repository
echo "🚀 Setting up Random Crossword Generator for GitHub..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Random Crossword Generator

- Flask web application for generating crossword puzzles
- Web scraping with BeautifulSoup and NLTK
- Interactive crossword grid with JavaScript
- Vercel deployment ready
- Comprehensive testing and documentation"

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    echo "🌐 No remote repository found."
    echo "Please create a repository on GitHub and run:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/random-crossword-generator.git"
    echo "git branch -M main"
    echo "git push -u origin main"
else
    echo "✅ Remote repository already configured."
    echo "You can push your changes with: git push"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a repository on GitHub"
echo "2. Add the remote: git remote add origin https://github.com/YOUR_USERNAME/random-crossword-generator.git"
echo "3. Push to GitHub: git push -u origin main"
echo "4. Deploy to Vercel: https://vercel.com/new"
echo ""
echo "Happy coding! 🧩" 