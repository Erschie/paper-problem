from collections import defaultdict
from langchain_openai import OpenAI
import re

def get_matches(text, key_phrases):
    pattern = re.compile(r'|'.join([re.escape(phrase) for phrase in key_phrases]), re.IGNORECASE)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    matching_sentences = [sentence for sentence in sentences if pattern.search(sentence)]
    
    return matching_sentences

def similarity_score(sentence1, sentence2):
    prompt = prompt_template.format(sentence1=sentence1, sentence2=sentence2)
    response = llm(prompt)
    score = response.strip()
    return score


def paper_to_problem(filepath):
    key_phrases = ["we present", "we address", "we describe", "we conclude", "our work presents", "our work addresses", "our work describes", "our work concludes", "this paper presents", "this paper addresses", "this paper describes", "this paper concludes", "overall", "in conclusion", "in this paper"]

    with open(filepath, 'r') as file:
        content = file.read()
    
    matches = get_matches(content, key_phrases)

    similarity_dict = defaultdict(int)
    for i in range(len(matches)):
        for j in range(i + 1, len(matches)):
            similarity = similarity_score(matches[i], matches[j])
            similarity_dict[i] += int(similarity)
            similarity_dict[j] += int(similarity)

    if (len(matches) != 0):
        max_key = max(similarity_dict, key=similarity_dict.get)
        return matches[max_key]
    else:
        return "No matches"

llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.0)
prompt_template = """
You are an AI model tasked with evaluating the similarity between two sentences.

Please give a similarity score between the following two sentences based on how closely they are related in terms of meaning, on a scale of 0 to 10, where 0 means not related at all and 10 means highly related.

Sentence 1: "{sentence1}"
Sentence 2: "{sentence2}"

Give only the score, no explanation.
"""

file_path = '/Users/mitchellwang/Documents/paper_problem/output.txt'
print(paper_to_problem(file_path))
