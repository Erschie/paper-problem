import re

def remove_latex_commands(text):
    # Remove LaTex comments and everything after
    text = re.sub(r'%.*', '', text)

    # Remove everything before and including begin{abstract}
    text = re.sub(r'.*?\\begin{abstract}', '', text, flags=re.DOTALL)

    # Remove everything after and including \appendix
    text = re.sub(r'\\appendix.*', '', text, flags=re.DOTALL)

    # Remove figures
    text = re.sub(r'\\begin{figure}.*?\\end{figure}', '', text, flags=re.DOTALL)

    # Replace equations with just "equation"
    text = re.sub(r'\\begin{equation}.*?\\end{equation}', 'equation.', text, flags=re.DOTALL)

    # Replace equations with just "compactenum"
    text = re.sub(r'\\begin{compactenum}.*?\\end{compactenum}', 'compactenum.', text, flags=re.DOTALL)

    # Remove everything from ~\cite{ to }
    text = re.sub(r'~\\cite{[^}]*}', '', text)

    # Replace \ref with just the reference name
    text = re.sub(r'~\\ref{[^:]*:([^}]*)}', r' \1', text)

    # Remove inline math
    text = re.sub(r'\$.*?\$', '', text)

    # Remove every line that starts with \
    text = re.sub(r'^\\.*', '', text, flags=re.MULTILINE)

    # Remove remaining backslashes and braces
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'[{}]', '', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove any remaining new lines
    text = re.sub(r'\\\\', '', text)
    
    return text

def tex_to_plaintext(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
    
    plain_text = remove_latex_commands(content)
    
    return plain_text

file_path = '/Users/mitchellwang/Downloads/arXiv-1904.00687v4/arxiv-version.tex'
plain_text = tex_to_plaintext(file_path)

with open('output.txt', 'w') as output_file:
    output_file.write(plain_text)
