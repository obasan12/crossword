#!/usr/bin/env python3
"""
Demonstration script for the Random Crossword Generator
This script shows how to use the core components programmatically.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import WebScraper, CrosswordGenerator

def demo_web_scraping():
    """Demonstrate web scraping functionality"""
    print("🌐 Web Scraping Demonstration")
    print("=" * 50)
    
    scraper = WebScraper()
    
    # Example text to extract words from
    sample_text = """
    Python is a high-level programming language known for its simplicity and readability.
    Flask is a lightweight web framework for Python that makes it easy to build web applications.
    BeautifulSoup is a library for pulling data out of HTML and XML files.
    NLTK is a leading platform for building Python programs to work with human language data.
    """
    
    print("Sample text:")
    print(sample_text.strip())
    print()
    
    # Extract words
    words = scraper.extract_words_from_text(sample_text)
    print(f"Extracted {len(words)} words:")
    print(", ".join(words[:10]) + "..." if len(words) > 10 else ", ".join(words))
    print()
    
    # Get definitions for some words
    print("Word definitions:")
    for word in words[:5]:
        definition = scraper.get_word_definition(word)
        print(f"  {word}: {definition}")
    print()

def demo_crossword_generation():
    """Demonstrate crossword generation functionality"""
    print("🧩 Crossword Generation Demonstration")
    print("=" * 50)
    
    generator = CrosswordGenerator()
    
    # Sample words with definitions
    sample_words = [
        {'word': 'python', 'definition': 'A high-level programming language'},
        {'word': 'flask', 'definition': 'A lightweight web framework'},
        {'word': 'beautifulsoup', 'definition': 'A library for parsing HTML'},
        {'word': 'nltk', 'definition': 'Natural language processing toolkit'},
        {'word': 'web', 'definition': 'A system of interconnected documents'},
        {'word': 'data', 'definition': 'Information in digital form'},
        {'word': 'code', 'definition': 'Instructions for a computer'},
        {'word': 'app', 'definition': 'A software application'},
    ]
    
    print(f"Generating crossword with {len(sample_words)} words...")
    print("Words:", ", ".join([w['word'] for w in sample_words]))
    print()
    
    # Generate crossword
    puzzle = generator.generate_crossword(sample_words, time_limit=10)
    
    if puzzle:
        print("✅ Crossword generated successfully!")
        print(f"Words placed: {len(puzzle['words'])}")
        print(f"Puzzle score: {puzzle['score']:.1f}")
        print()
        
        # Display the grid
        print("Crossword Grid:")
        print("-" * (len(puzzle['grid'][0]) * 3 + 1))
        for row in puzzle['grid']:
            print("|", end=" ")
            for cell in row:
                if cell == ' ':
                    print(" ", end=" ")
                else:
                    print(cell, end=" ")
            print("|")
        print("-" * (len(puzzle['grid'][0]) * 3 + 1))
        print()
        
        # Display clues
        print("Clues:")
        for i, pos in enumerate(puzzle['positions']):
            direction = "Across" if pos['direction'] == 'horizontal' else "Down"
            print(f"  {i+1}. ({direction}) {pos['definition']}")
    else:
        print("❌ Could not generate a crossword puzzle")
    print()

def demo_full_workflow():
    """Demonstrate the complete workflow"""
    print("🔄 Complete Workflow Demonstration")
    print("=" * 50)
    
    print("This demonstrates the complete process:")
    print("1. Web scraping (simulated)")
    print("2. Word extraction and definition lookup")
    print("3. Crossword generation")
    print("4. Result display")
    print()
    
    # Simulate the complete workflow
    scraper = WebScraper()
    generator = CrosswordGenerator()
    
    # Step 1: Simulate web scraping
    print("Step 1: Web Scraping")
    print("  Scraping content from a sample website...")
    
    # Step 2: Extract words
    sample_content = """
    Artificial Intelligence is transforming the world of technology.
    Machine Learning algorithms can process vast amounts of data.
    Deep Learning networks mimic the human brain structure.
    Neural Networks are the foundation of modern AI systems.
    """
    
    words = scraper.extract_words_from_text(sample_content)
    print(f"  Extracted {len(words)} words from content")
    
    # Step 3: Get definitions
    words_with_definitions = []
    for word in words[:8]:  # Limit to 8 words for demo
        definition = scraper.get_word_definition(word)
        words_with_definitions.append({
            'word': word,
            'definition': definition
        })
    
    print(f"  Created {len(words_with_definitions)} word-definition pairs")
    
    # Step 4: Generate crossword
    print("\nStep 2: Crossword Generation")
    print("  Generating crossword puzzle...")
    
    puzzle = generator.generate_crossword(words_with_definitions, time_limit=15)
    
    if puzzle:
        print("  ✅ Puzzle generated successfully!")
        print(f"  Words included: {len(puzzle['words'])}")
        print(f"  Puzzle score: {puzzle['score']:.1f}")
        
        # Step 5: Display results
        print("\nStep 3: Results")
        print("  Final crossword puzzle:")
        
        # Show a simplified grid
        print("  Grid preview (showing only filled cells):")
        for i, row in enumerate(puzzle['grid']):
            row_display = ""
            for j, cell in enumerate(row):
                if cell != ' ':
                    row_display += cell
                else:
                    row_display += "."
            if any(cell != ' ' for cell in row):
                print(f"    Row {i}: {row_display}")
        
        print("\n  Clues:")
        for i, pos in enumerate(puzzle['positions']):
            direction = "→" if pos['direction'] == 'horizontal' else "↓"
            print(f"    {i+1}. {direction} {pos['definition']}")
    else:
        print("  ❌ Could not generate puzzle")
    
    print("\n" + "=" * 50)
    print("🎉 Demonstration completed!")
    print("\nTo run the full web application:")
    print("  python app.py")
    print("  Then open http://localhost:5000 in your browser")

if __name__ == "__main__":
    print("🚀 Random Crossword Generator - Demonstration")
    print("=" * 60)
    print()
    
    try:
        demo_web_scraping()
        demo_crossword_generation()
        demo_full_workflow()
        
    except Exception as e:
        print(f"❌ Demonstration failed with error: {e}")
        sys.exit(1) 