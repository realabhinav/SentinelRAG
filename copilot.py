"""Retrieve guidance and optionally synthesize a response with Gemini."""
import argparse
import json
import math
import os
import re
import urllib.request
from collections import Counter
from pathlib import Path


def features(text):
    terms = re.findall(r"[a-z0-9]+", text.lower())
    return Counter(terms + [" ".join(pair) for pair in zip(terms, terms[1:])])


def retrieve(question, corpus, k=2):
    documents = {name: features(body) for name, body in corpus.items()}
    vocabulary = set().union(*documents.values())
    idf = {term: 1 + math.log((1+len(corpus))/(1+sum(term in doc for doc in documents.values())))
           for term in vocabulary}

    def normalize(counts):
        weighted = {term: count*idf[term] for term, count in counts.items() if term in idf}
        norm = math.sqrt(sum(x*x for x in weighted.values())) or 1
        return {term: x/norm for term, x in weighted.items()}

    q = normalize(features(question))
    ranked = []
    for name, doc in documents.items():
        score = sum(q.get(term, 0)*weight for term, weight in normalize(doc).items())
        if score > 0:
            ranked.append((score, name))
    return [name for _, name in sorted(ranked, key=lambda row: (-row[0],row[1]))[:k]]


def answer(prompt, corpus, model=None):
    names = retrieve(prompt, corpus)
    if not names:
        return {"answer":"No matching evidence.", "sources":[]}
    passages = "\n".join(f"[{name}] {corpus[name]}" for name in names)
    if model:
        if not re.fullmatch(r"[a-zA-Z0-9.-]+", model):
            raise ValueError("Invalid model name")
        instruction = "Use the supplied excerpts as evidence. Cite their IDs. If insufficient, say so."
        payload = {"systemInstruction":{"parts":[{"text":instruction}]},
                   "contents":[{"parts":[{"text":json.dumps({"question":prompt,"excerpts":passages})}]}]}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        req = urllib.request.Request(url, json.dumps(payload).encode(),
                                     {"Content-Type":"application/json","x-goog-api-key":os.environ["GEMINI_API_KEY"]})
        with urllib.request.urlopen(req, timeout=20) as response:
            parts = json.load(response)["candidates"][0]["content"]["parts"]
        passages = " ".join(part.get("text","") for part in parts)
    return {"answer":passages,"sources":names}


def load_corpus():
    return {p.stem:p.read_text(encoding="utf8").strip() for p in
            sorted(Path(__file__).with_name("guidance").glob("*.txt"))}


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("question")
    cli.add_argument("--model")
    args = cli.parse_args()
    print(json.dumps(answer(args.question, load_corpus(), args.model), indent=2))
