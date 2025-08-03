from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from collections import defaultdict
import threading
from urllib.parse import urljoin, urlparse
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

class CrosswordGenerator:
    def __init__(self):
        self.grid = []
        self.words = []
        self.positions = []
        self.max_size = 20
        
    def create_grid(self, size):
        """Create an empty grid"""
        return [[' ' for _ in range(size)] for _ in range(size)]
    
    def can_place_word(self, word, row, col, direction):
        """Check if a word can be placed at the given position"""
        if direction == 'horizontal':
            if col + len(word) > len(self.grid[0]):
                return False
            for i, letter in enumerate(word):
                if self.grid[row][col + i] != ' ' and self.grid[row][col + i] != letter:
                    return False
        else:  # vertical
            if row + len(word) > len(self.grid):
                return False
            for i, letter in enumerate(word):
                if self.grid[row + i][col] != ' ' and self.grid[row + i][col] != letter:
                    return False
        return True
    
    def place_word(self, word, row, col, direction):
        """Place a word on the grid"""
        if direction == 'horizontal':
            for i, letter in enumerate(word):
                self.grid[row][col + i] = letter
        else:  # vertical
            for i, letter in enumerate(word):
                self.grid[row + i][col] = letter
    
    def get_intersections(self, word):
        """Get all possible intersection points for a word"""
        intersections = []
        for pos in self.positions:
            existing_word = pos['word']
            for i, letter1 in enumerate(word):
                for j, letter2 in enumerate(existing_word):
                    if letter1 == letter2:
                        if pos['direction'] == 'horizontal':
                            # Try placing new word vertically
                            new_row = pos['row'] + j
                            new_col = pos['col'] - i
                            if new_row >= 0 and new_col >= 0:
                                intersections.append((new_row, new_col, 'vertical'))
                        else:
                            # Try placing new word horizontally
                            new_row = pos['row'] - i
                            new_col = pos['col'] + j
                            if new_row >= 0 and new_col >= 0:
                                intersections.append((new_row, new_col, 'horizontal'))
        return intersections
    
    def generate_crossword(self, words_with_definitions, time_limit=60):
        """Generate a crossword puzzle within the time limit"""
        start_time = time.time()
        best_puzzle = None
        best_score = 0
        
        # Sort words by length (longer words first for better placement)
        sorted_words = sorted(words_with_definitions, key=lambda x: len(x['word']), reverse=True)
        
        attempts = 0
        max_attempts = 100
        
        while time.time() - start_time < time_limit and attempts < max_attempts:
            attempts += 1
            
            # Create new grid
            self.grid = self.create_grid(self.max_size)
            self.positions = []
            self.words = []
            
            center_row = self.max_size // 2
            center_col = self.max_size // 2
            
            # Place first word in center
            if sorted_words:
                first_word = sorted_words[0]
                word = first_word['word'].upper()
                if len(word) <= self.max_size:
                    start_col = center_col - len(word) // 2
                    if self.can_place_word(word, center_row, start_col, 'horizontal'):
                        self.place_word(word, center_row, start_col, 'horizontal')
                        self.positions.append({
                            'word': word,
                            'row': center_row,
                            'col': start_col,
                            'direction': 'horizontal',
                            'definition': first_word['definition']
                        })
                        self.words.append(word)
            
            # Try to place remaining words
            for word_data in sorted_words[1:]:
                word = word_data['word'].upper()
                if len(word) <= self.max_size:
                    intersections = self.get_intersections(word)
                    
                    # Try each intersection
                    placed = False
                    for row, col, direction in intersections:
                        if self.can_place_word(word, row, col, direction):
                            self.place_word(word, row, col, direction)
                            self.positions.append({
                                'word': word,
                                'row': row,
                                'col': col,
                                'direction': direction,
                                'definition': word_data['definition']
                            })
                            self.words.append(word)
                            placed = True
                            break
                    
                    # If no intersection found, try random placement
                    if not placed and len(self.words) < 3:
                        for _ in range(10):
                            row = random.randint(0, self.max_size - len(word))
                            col = random.randint(0, self.max_size - len(word))
                            direction = random.choice(['horizontal', 'vertical'])
                            
                            if self.can_place_word(word, row, col, direction):
                                self.place_word(word, row, col, direction)
                                self.positions.append({
                                    'word': word,
                                    'row': row,
                                    'col': col,
                                    'direction': direction,
                                    'definition': word_data['definition']
                                })
                                self.words.append(word)
                                break
            
            # Calculate score for this puzzle
            score = self.calculate_puzzle_score()
            
            if score > best_score:
                best_score = score
                # Separate across and down clues
                across_clues = []
                down_clues = []
                for i, pos in enumerate(self.positions):
                    clue_data = {
                        'number': i + 1,
                        'definition': pos['definition']
                    }
                    if pos['direction'] == 'horizontal':
                        across_clues.append(clue_data)
                    else:
                        down_clues.append(clue_data)
                
                best_puzzle = {
                    'grid': [row[:] for row in self.grid],
                    'words': self.words[:],
                    'positions': self.positions[:],
                    'score': score,
                    'across_clues': across_clues,
                    'down_clues': down_clues
                }
        
        return best_puzzle
    
    def calculate_puzzle_score(self):
        """Calculate a score for the puzzle quality"""
        if not self.words:
            return 0
        
        # Count filled cells
        filled_cells = sum(1 for row in self.grid for cell in row if cell != ' ')
        total_cells = len(self.grid) * len(self.grid[0])
        density = filled_cells / total_cells
        
        # Bonus for more words
        word_bonus = len(self.words) * 10
        
        # Bonus for longer words
        length_bonus = sum(len(word) for word in self.words)
        
        # Penalty for empty space
        empty_penalty = (1 - density) * 100
        
        return word_bonus + length_bonus - empty_penalty

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def is_valid_url(self, url):
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def get_word_definition(self, word):
        """Get definition for a word using WordNet"""
        try:
            synsets = wordnet.synsets(word.lower())
            if synsets:
                return synsets[0].definition()
            return f"A {word.lower()}"
        except:
            return f"A {word.lower()}"
    
    def extract_words_from_text(self, text):
        """Extract meaningful words from text"""
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Filter words
        words = []
        for token in tokens:
            if (len(token) >= 3 and 
                token.isalpha() and 
                token not in ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']):
                words.append(token)
        
        return list(set(words))  # Remove duplicates
    
    def scrape_website(self, url):
        """Scrape website and extract words with definitions"""
        if not self.is_valid_url(url):
            raise ValueError("Invalid URL provided")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text from various elements
            text_elements = []
            
            # Get text from paragraphs
            for p in soup.find_all('p'):
                text_elements.append(p.get_text())
            
            # Get text from headings
            for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text_elements.append(h.get_text())
            
            # Get text from list items
            for li in soup.find_all('li'):
                text_elements.append(li.get_text())
            
            # Get text from divs (limited to avoid too much content)
            for div in soup.find_all('div')[:10]:
                text_elements.append(div.get_text())
            
            # Combine all text
            full_text = ' '.join(text_elements)
            
            # Extract words
            words = self.extract_words_from_text(full_text)
            
            # Get definitions and create word list
            words_with_definitions = []
            for word in words[:50]:  # Limit to 50 words
                definition = self.get_word_definition(word)
                words_with_definitions.append({
                    'word': word,
                    'definition': definition
                })
            
            return words_with_definitions
            
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch website: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing website: {str(e)}")

# Global instances
scraper = WebScraper()
crossword_gen = CrosswordGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_crossword():
    url = request.form.get('url', '').strip()
    
    if not url:
        return render_template('index.html', error="Please provide a URL")
    
    try:
        # Scrape website
        words_with_definitions = scraper.scrape_website(url)
        
        if not words_with_definitions:
            return render_template('index.html', error="No suitable words found on the website")
        
        # Generate crossword
        puzzle = crossword_gen.generate_crossword(words_with_definitions, time_limit=60)
        
        if not puzzle:
            return render_template('index.html', error="Could not generate a crossword puzzle")
        
        return render_template('result.html', puzzle=puzzle, source_url=url)
        
    except ValueError as e:
        return render_template('index.html', error=str(e))
    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {str(e)}")

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for AJAX requests"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'Please provide a URL'}), 400
    
    try:
        # Scrape website
        words_with_definitions = scraper.scrape_website(url)
        
        if not words_with_definitions:
            return jsonify({'error': 'No suitable words found on the website'}), 400
        
        # Generate crossword
        puzzle = crossword_gen.generate_crossword(words_with_definitions, time_limit=60)
        
        if not puzzle:
            return jsonify({'error': 'Could not generate a crossword puzzle'}), 400
        
        return jsonify({
            'success': True,
            'puzzle': puzzle,
            'source_url': url
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/test')
def test_template():
    """Test route to debug template rendering"""
    test_puzzle = {
        'words': ['test', 'word'],
        'score': 10.5,
        'across_clues': [{'number': 1, 'definition': 'Test clue'}],
        'down_clues': [{'number': 2, 'definition': 'Another clue'}]
    }
    return render_template('test.html', puzzle=test_puzzle)

# For Vercel deployment
app.debug = False

# WSGI application for Vercel
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000) 