# 🧩 Random Crossword Generator

A modern Flask web application that automatically generates crossword puzzles from any website's content. Simply enter a URL, and watch as the app scrapes the website, extracts meaningful words, and creates an interactive crossword puzzle!

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/random-crossword-generator)

## ✨ Features

- 🌐 **Web Scraping**: Automatically crawls websites and extracts text content
- 🧠 **Smart Word Processing**: Uses NLTK and WordNet for intelligent word filtering and definition lookup
- 🎯 **Advanced Crossword Generation**: Creates multiple puzzles and selects the best one using sophisticated scoring algorithms
- 🎨 **Interactive UI**: Modern, responsive design with interactive crossword grid
- 📱 **Mobile Friendly**: Works perfectly on desktop and mobile devices
- 🖨️ **Print Support**: Generate print-friendly puzzle layouts
- ⚡ **Fast Performance**: Optimized for quick puzzle generation
- 🛡️ **Error Handling**: Comprehensive error handling for invalid URLs and scraping issues

## 🚀 Live Demo

Try it out: [Random Crossword Generator](https://your-vercel-app.vercel.app)

## 🛠️ How It Works

1. **Web Scraping**: The app uses BeautifulSoup to scrape website content, extracting text from paragraphs, headings, and list items
2. **Word Extraction**: NLTK tokenizes and filters meaningful words (3+ characters, excluding common stop words)
3. **Definition Lookup**: WordNet provides contextually relevant definitions for extracted words
4. **Puzzle Generation**: Multiple crossword puzzles are generated within a time limit, with the best one selected based on scoring criteria
5. **Interactive Display**: The final puzzle is displayed with an interactive grid and organized clues

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/random-crossword-generator.git
   cd random-crossword-generator
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## 🌐 Deployment

### Vercel (Recommended)

1. **Fork this repository** to your GitHub account
2. **Connect to Vercel**:
   - Go to [Vercel](https://vercel.com)
   - Click "New Project"
   - Import your forked repository
   - Vercel will automatically detect the Python configuration
3. **Deploy**: Click "Deploy" and your app will be live!

### Other Platforms

- **Heroku**: Add `Procfile` with `web: gunicorn app:app`
- **Railway**: Connect your GitHub repository
- **DigitalOcean App Platform**: Deploy directly from GitHub

## 🎯 Usage

1. **Enter a URL**: Input any website URL in the form field
2. **Generate Puzzle**: Click "Generate Crossword Puzzle" and wait (up to 1 minute)
3. **Enjoy**: The generated puzzle will display with:
   - Interactive crossword grid
   - Across and Down clues
   - Puzzle statistics
   - Print option

## 💡 Tips for Better Results

- Choose websites with rich text content (articles, blogs, documentation)
- Avoid image-heavy sites or those with minimal text
- Ensure the website is publicly accessible
- The process may take up to a minute for complex websites

## 🔧 Technical Details

### Crossword Generation Algorithm

The crossword generator uses an advanced approach:

1. **Grid Creation**: Creates a 20x20 grid
2. **Word Placement**: Places the longest word in the center
3. **Intersection Finding**: Finds valid intersection points for remaining words
4. **Scoring System**: Evaluates puzzles based on:
   - Number of words included
   - Word length bonuses
   - Grid density (penalty for empty space)
5. **Time Limit**: Generates multiple attempts within 60 seconds

### Web Scraping Features

- **User-Agent Spoofing**: Uses realistic browser headers
- **Content Extraction**: Focuses on meaningful content (p, h1-h6, li, div)
- **Text Cleaning**: Removes scripts, styles, and unnecessary formatting
- **Error Handling**: Graceful handling of network issues and invalid URLs

### Word Processing

- **Tokenization**: Uses NLTK's word_tokenize for accurate word splitting
- **Filtering**: Removes short words and common stop words
- **Definition Lookup**: Uses WordNet for word definitions
- **Case Handling**: Converts all words to uppercase for consistency

## 📁 Project Structure

```
random-crossword-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── README.md             # This file
├── test_app.py           # Unit tests
├── demo.py               # Demonstration script
└── templates/
    ├── base.html         # Base template with styling
    ├── index.html        # Home page with URL form
    ├── result.html       # Results page with crossword display
    └── test.html         # Test template
```

## 🧪 Testing

Run the test suite:
```bash
python test_app.py
```

Run the demonstration:
```bash
python demo.py
```

## 🔌 API Endpoints

- `GET /`: Home page with URL input form
- `POST /generate`: Generate crossword from URL
- `POST /api/generate`: JSON API endpoint for AJAX requests
- `GET /test`: Test route for debugging

## 🛠️ Dependencies

- **Flask**: Web framework
- **requests**: HTTP library for web scraping
- **BeautifulSoup4**: HTML parsing
- **NLTK**: Natural language processing
- **gunicorn**: WSGI server for production

## 🌍 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## 🐛 Troubleshooting

### Common Issues

1. **"No suitable words found"**: Try a different website with more text content
2. **"Failed to fetch website"**: Check if the URL is accessible and publicly available
3. **"Could not generate a crossword puzzle"**: The website may not have enough suitable words

### Installation Issues

- Ensure you're using Python 3.7+
- Try upgrading pip: `pip install --upgrade pip`
- On Windows, you may need to install Visual C++ build tools for some packages

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python test_app.py`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [NLTK](https://www.nltk.org/) and [WordNet](https://wordnet.princeton.edu/) for natural language processing
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Font Awesome](https://fontawesome.com/) for icons
- [Vercel](https://vercel.com/) for hosting

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/random-crossword-generator)
![GitHub forks](https://img.shields.io/github/forks/yourusername/random-crossword-generator)
![GitHub issues](https://img.shields.io/github/issues/yourusername/random-crossword-generator)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/random-crossword-generator)
![GitHub license](https://img.shields.io/github/license/yourusername/random-crossword-generator)

---

⭐ **Star this repository if you found it helpful!** 