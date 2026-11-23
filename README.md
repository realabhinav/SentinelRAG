# SentinelRAG
A source-grounded command-line copilot with five original guidance files. Run from this directory with Python 3.10+.

    python copilot.py "How should we restore backups?"
    python -m unittest -v

For optional generated prose, set GEMINI_API_KEY in your environment and supply --model followed by an available Gemini model ID. That mode sends the question and selected excerpts to Gemini. The default returns quoted passages with source IDs offline. Retrieval uses smoothed TF-IDF over words and adjacent word pairs, L2 normalization and cosine similarity. Any positive match qualifies, so inspect weak hits. The sources array identifies retrieved passages and is not a factuality score. This portable edition uses a CLI.
