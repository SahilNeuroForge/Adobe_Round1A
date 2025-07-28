# challenge_1b/analyzer/summarizer.py

def summarize(text, max_sentences=2):
    """Extractive summarizer: returns first N sentences."""
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = ' '.join(sentences[:max_sentences])
    return summary
