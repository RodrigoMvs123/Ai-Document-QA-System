"""
SENTIMENT ANALYSIS SCRIPT
Analyzes text to determine sentiment score from 0.00 to 1.00
0.00 = Most Negative | 0.50 = Neutral | 1.00 = Most Positive
"""

# ============================================================================
# WORD LISTS
# ============================================================================

# List of positive words (base forms)
POSITIVE_WORDS = [
    "good", "great", "excellent", "amazing", "wonderful", "fantastic",
    "love", "like", "happy", "joy", "perfect", "best", "awesome",
    "beautiful", "brilliant", "superb", "outstanding", "magnificent",
    "delightful", "pleasant", "enjoy", "positive", "success", "win",
    "hope", "improve", "better", "nice", "kind", "friendly"
]

# List of negative words (base forms)
NEGATIVE_WORDS = [
    "bad", "terrible", "awful", "horrible", "poor", "worst", "hate",
    "dislike", "sad", "unhappy", "angry", "disappointing", "failure",
    "fail", "lose", "problem", "issue", "wrong", "negative", "difficult",
    "hard", "pain", "hurt", "ugly", "boring", "annoying", "frustrating",
    "disgusting", "nasty", "unpleasant"
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def normalize_word(word):
    """
    Normalize a word to its base form for matching.
    Handles:
    - Case insensitivity (Good -> good)
    - Plural forms (goods -> good)
    - Common suffixes (running -> run, happiness -> happy)
    """
    # Convert to lowercase
    word = word.lower()
    
    # Remove common suffixes to get base form
    suffixes = ['ing', 'ed', 's', 'es', 'ly', 'ness', 'ful', 'less']
    
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            # Try removing suffix
            base = word[:-len(suffix)]
            
            # Special case: if word ends in 'ies', replace with 'y'
            if word.endswith('ies') and len(word) > 4:
                base = word[:-3] + 'y'
            
            # Check if base form exists in our word lists
            if base in POSITIVE_WORDS or base in NEGATIVE_WORDS:
                return base
    
    return word

def clean_text(text):
    """
    Clean and prepare text for analysis.
    Removes punctuation and splits into words.
    """
    # Remove common punctuation
    punctuation = ".,!?;:\"'()[]{}..."
    for char in punctuation:
        text = text.replace(char, " ")
    
    # Split into words and filter empty strings
    words = [word.strip() for word in text.split() if word.strip()]
    
    return words

def calculate_sentiment_score(positive_count, negative_count):
    """
    Calculate sentiment score between 0.00 and 1.00
    
    Formula:
    - If no sentiment words: 0.50 (neutral)
    - Otherwise: positive_count / (positive_count + negative_count)
    
    Returns:
        float: Score from 0.00 (most negative) to 1.00 (most positive)
    """
    total_sentiment_words = positive_count + negative_count
    
    # If no sentiment words found, return neutral (0.50)
    if total_sentiment_words == 0:
        return 0.50
    
    # Calculate score: ratio of positive to total sentiment words
    score = positive_count / total_sentiment_words
    
    # Round to 2 decimal places
    return round(score, 2)

# ============================================================================
# MAIN SENTIMENT ANALYSIS FUNCTION
# ============================================================================

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Dictionary containing:
            - positive_count: Number of positive words found
            - negative_count: Number of negative words found
            - sentiment_score: Score from 0.00 to 1.00
            - sentiment_label: Text label (Positive/Negative/Neutral)
            - positive_words_found: List of positive words detected
            - negative_words_found: List of negative words detected
    """
    # Clean and split text into words
    words = clean_text(text)
    
    # Initialize counters
    positive_count = 0
    negative_count = 0
    positive_words_found = []
    negative_words_found = []
    
    # Analyze each word
    for word in words:
        # Normalize the word (handle case, plurals, etc.)
        normalized = normalize_word(word)
        
        # Check if word is positive
        if normalized in POSITIVE_WORDS:
            positive_count += 1
            positive_words_found.append(word)  # Store original word
        
        # Check if word is negative
        elif normalized in NEGATIVE_WORDS:
            negative_count += 1
            negative_words_found.append(word)  # Store original word
    
    # Calculate sentiment score (0.00 to 1.00)
    sentiment_score = calculate_sentiment_score(positive_count, negative_count)
    
    # Determine sentiment label based on score
    if sentiment_score > 0.60:
        sentiment_label = "Positive"
    elif sentiment_score < 0.40:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    
    # Return analysis results
    return {
        "positive_count": positive_count,
        "negative_count": negative_count,
        "sentiment_score": sentiment_score,
        "sentiment_label": sentiment_label,
        "positive_words_found": positive_words_found,
        "negative_words_found": negative_words_found
    }

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

def display_results(text, results):
    """
    Display the sentiment analysis results in a formatted way.
    """
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS RESULTS")
    print("="*60)
    print(f"\nText analyzed: \"{text}\"")
    print(f"\n📊 Positive words found: {results['positive_count']}")
    if results['positive_words_found']:
        print(f"   Words: {', '.join(results['positive_words_found'])}")
    
    print(f"\n📊 Negative words found: {results['negative_count']}")
    if results['negative_words_found']:
        print(f"   Words: {', '.join(results['negative_words_found'])}")
    
    # Display sentiment score with visual indicator
    score = results['sentiment_score']
    print(f"\n🎯 SENTIMENT SCORE: {score:.2f}")
    print(f"   Scale: 0.00 (Most Negative) ← 0.50 (Neutral) → 1.00 (Most Positive)")
    
    # Visual bar representation
    bar_length = 40
    filled = int(score * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"   [{bar}]")
    
    print(f"\n   Label: {results['sentiment_label']}")
    print("="*60 + "\n")

# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """
    Main program loop - allows user to analyze multiple texts.
    """
    print("="*60)
    print("SENTIMENT ANALYSIS TOOL")
    print("="*60)
    print("\nThis tool analyzes text sentiment on a scale from 0.00 to 1.00")
    print("  • 0.00 = Most Negative")
    print("  • 0.50 = Neutral")
    print("  • 1.00 = Most Positive")
    print("\nFeatures:")
    print("  ✓ Case insensitive (Good = good)")
    print("  ✓ Handles plurals (goods = good)")
    print("  ✓ Ignores punctuation")
    print("\nType 'quit' or 'exit' to stop.\n")
    
    while True:
        # Get user input
        text = input("Enter a phrase to analyze: ").strip()
        
        # Check if user wants to quit
        if text.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using Sentiment Analysis Tool! 👋")
            break
        
        # Skip empty input
        if not text:
            print("Please enter some text to analyze.\n")
            continue
        
        # Perform sentiment analysis
        results = analyze_sentiment(text)
        
        # Display results
        display_results(text, results)

# ============================================================================
# RUN PROGRAM
# ============================================================================

if __name__ == "__main__":
    main()
