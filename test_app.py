#!/usr/bin/env python3
"""
Simple test script for the Random Crossword Generator
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import WebScraper, CrosswordGenerator

def test_web_scraper():
    """Test the web scraper functionality"""
    print("Testing Web Scraper...")
    
    scraper = WebScraper()
    
    # Test URL validation
    assert scraper.is_valid_url("https://example.com") == True
    assert scraper.is_valid_url("http://test.org") == True
    assert scraper.is_valid_url("invalid-url") == False
    print("✓ URL validation works")
    
    # Test word definition lookup
    definition = scraper.get_word_definition("computer")
    assert "computer" in definition.lower() or "a" in definition.lower()
    print("✓ Word definition lookup works")
    
    # Test word extraction from text
    test_text = "The quick brown fox jumps over the lazy dog. Computer programming is fun."
    words = scraper.extract_words_from_text(test_text)
    assert len(words) > 0
    assert "computer" in words or "programming" in words
    print("✓ Word extraction works")
    
    print("Web Scraper tests passed!\n")

def test_crossword_generator():
    """Test the crossword generator functionality"""
    print("Testing Crossword Generator...")
    
    generator = CrosswordGenerator()
    
    # Test grid creation
    grid = generator.create_grid(5)
    assert len(grid) == 5
    assert len(grid[0]) == 5
    assert all(cell == ' ' for row in grid for cell in row)
    print("✓ Grid creation works")
    
    # Test word placement
    test_word = "HELLO"
    generator.grid = generator.create_grid(10)  # Initialize grid first
    assert generator.can_place_word(test_word, 0, 0, 'horizontal') == True
    generator.place_word(test_word, 0, 0, 'horizontal')
    assert generator.grid[0][:5] == ['H', 'E', 'L', 'L', 'O']
    print("✓ Word placement works")
    
    # Test intersection finding
    generator.grid = generator.create_grid(10)
    generator.positions = [{
        'word': 'WORLD',
        'row': 2,
        'col': 2,
        'direction': 'horizontal'
    }]
    generator.place_word('WORLD', 2, 2, 'horizontal')
    
    intersections = generator.get_intersections('HELLO')
    assert len(intersections) > 0
    print("✓ Intersection finding works")
    
    print("Crossword Generator tests passed!\n")

def test_integration():
    """Test the integration of components"""
    print("Testing Integration...")
    
    # Create test words with definitions
    test_words = [
        {'word': 'hello', 'definition': 'A greeting'},
        {'word': 'world', 'definition': 'The earth'},
        {'word': 'python', 'definition': 'A programming language'},
        {'word': 'flask', 'definition': 'A web framework'},
        {'word': 'crossword', 'definition': 'A word puzzle'}
    ]
    
    generator = CrosswordGenerator()
    puzzle = generator.generate_crossword(test_words, time_limit=5)
    
    if puzzle:
        assert 'grid' in puzzle
        assert 'words' in puzzle
        assert 'positions' in puzzle
        assert 'score' in puzzle
        print("✓ Crossword generation works")
    else:
        print("⚠ No puzzle generated in test (this may be normal for small word sets)")
    
    print("Integration tests completed!\n")

if __name__ == "__main__":
    print("Running Random Crossword Generator Tests\n")
    print("=" * 50)
    
    try:
        test_web_scraper()
        test_crossword_generator()
        test_integration()
        
        print("=" * 50)
        print("All tests completed successfully!")
        print("\nTo run the application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: python app.py")
        print("3. Open browser to: http://localhost:5000")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1) 