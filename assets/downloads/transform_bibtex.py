import re
import os
import sys

def extract_arxiv_number(text):
    """
    Extract only the arXiv number (YYMM.NNNNN) from text
    
    Args:
        text (str): The text to search for an arXiv number
    
    Returns:
        str or None: The matched arXiv number or None if no match
    """
    # Regex pattern to match just the arXiv number format
    pattern = r'\d{4}\.\d{5}'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    return match.group(0) if match else None

def transform_bibtex_entry(original_entry):
    """
    Transform a single BibTeX entry by adding html, abbr, and bibtex_show fields.
    
    Args:
        original_entry (str): The original BibTeX entry
    
    Returns:
        str: Transformed BibTeX entry
    """
    # Remove trailing comma and newline at the end of the entry
    original_entry = original_entry.strip().rstrip(',')
    
    new_fields = ['  bibtex_show = {true},']

    # Extract the journal for the abbr field
    # journal_match = re.search(r'journal\s*=\s*{([^}]+)}', original_entry)
    # abbr = journal_match.group(1).strip() if journal_match else ''
    

    # Extract the URL for the html field
    url_match = re.search(r'url\s*=\s*{([^}]+)}', original_entry)
    html = url_match.group(1).strip() if url_match else ''
    if not html:
        arxiv_number = extract_arxiv_number(original_entry)
        if arxiv_number:
            html = f"https://arxiv.org/abs/{arxiv_number}"
            new_fields.append('  html = {' + html + '},')
    # else: #don't need this as already present
    #     new_fields.append('  html = {' + html + '},')


    pdf_match = re.search(r'pdf\s*=\s*{([^}]+)}', original_entry)
    pdf = pdf_match.group(1).strip() if pdf_match else ''
    if not pdf:
        arxiv_number = extract_arxiv_number(original_entry)
        if arxiv_number:
            pdf = f"https://arxiv.org/pdf/{arxiv_number}"
            new_fields.append('  pdf = {' + pdf + '},')
    # else: #don't need this as already present
    #     new_fields.append('  pdf = {' + pdf + '},')

    abbr_match = re.search(r'abbr\s*=\s*{([^}]+)}', original_entry)
    abbr = abbr_match.group(1).strip() if abbr_match else ''

    # ADD in if you want default tags for all papers.
    # if not abbr:
    #     abbr = "NLP"
    #     new_fields.append('  abbr = {' +abbr+ '},')
       
    # Split the original entry into lines
    lines = original_entry.split('\n')
    
    # Find the index to insert new fields (after the first line)
    insert_index = 1
    
    # Insert the new fields
    for new_field in reversed(new_fields):
        lines.insert(insert_index, new_field)
    
    # Rejoin the lines
    transformed_entry = '\n'.join(lines)
    
    return transformed_entry

def extract_bibtex_entries(input_file):
    """
    Extract BibTeX entries from a single file.
    
    Args:
        input_file (str): Path to the input BibTeX file
    
    Returns:
        list: List of BibTeX entries
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            file_contents = f.read()
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        return []
    
    # Split the file into individual entries
    # This regex looks for entries starting with @ and ending with a closing }

    # pattern = r'@(?:[^@]*})' #problem with @ inside bib entry
    # pattern = r'@\w+\{(?:[^{}]*\{[^{}]*\}[^{}]*|[^{}])*\}' #does not work with tripple nesting of {}
    # pattern = r'@\w+\{(?:[^{}]*\{[^{}]*\}[^{}]*|[^{}]|[^{}]*\{[^{}]*\{[^{}]*\}[^{}]*\}[^{}]*)*\}' #this one has three patterns of brackets inside outside brackets.
    pattern = r'@\w+\{(?:[^{}]|[^{}]*\{[^{}]*\}[^{}]*|[^{}]*\{[^{}]*\{[^{}]*\}[^{}]*\}[^{}]*|[^{}]*\{[^{}]*\{[^{}]*\{[^{}]*\}[^{}]*\}[^{}]*\}[^{}]*)*\}' #zero, 1, 2 and 3 inside brackets.
    entries = re.findall(pattern, file_contents, re.DOTALL)
    
    return entries

def accumulate_and_transform_bibtex(input_directory, output_file):
    """
    Accumulate and transform BibTeX entries from all .bib files in a directory.
    
    Args:
        input_directory (str): Path to the input directory containing .bib files
        output_file (str): Path to the output accumulated and transformed BibTeX file
    
    Returns:
        list: Paths to all processed files
    """
    # Validate input directory
    if not os.path.isdir(input_directory):
        print(f"Error: {input_directory} is not a valid directory.")
        return []
    
    # List to store all entries and processed files
    all_entries = []
    processed_files = []
    
    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        print(f"Processing FIle:{filename}")
        # Check if the file is a .bib file
        if filename.endswith('.bib'):
            input_file = os.path.join(input_directory, filename)
            
            # Extract entries from the file
            entries = extract_bibtex_entries(input_file)
            print(f"Len entries in file:{len(entries)}")
            
            # Transform entries
            transformed_entries = [transform_bibtex_entry(entry) for entry in entries]
            
            # Add to accumulated entries
            all_entries.extend(transformed_entries)
            processed_files.append(input_file)
    
    # Write accumulated entries to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(all_entries))
        
        print(f"Accumulated and transformed entries from {len(processed_files)} files.")
        print(f"Total entries: {len(all_entries)}")
        print(f"Output written to {output_file}")
    except Exception as e:
        print(f"Error writing to file {output_file}: {e}")
        return []
    
    return processed_files

def main():
    input_folder=os.path.join("..","bibliography")
    output_file = os.path.join("_bibliography","papers.bib")

    if len(sys.argv) == 2:
        if sys.argv[1] == "production":
            output_file = os.path.join("..","..",output_file)

    accumulate_and_transform_bibtex(input_folder, output_file)
    
if __name__ == '__main__':
    main()
#     bibentry="""
# @inproceedings{collins2018evolutionary,
# title={Evolutionary Data Measures: Understanding the Difficulty of Text Classification Tasks},
# author={Collins, Edward and Rozanov, Nikolai and Zhang, Bingbing},
# booktitle={Proceedings of the 22nd Conference on Computational Natural Language Learning},
# pages={380--391},
# year={2018}
# }
# """
#     print(transform_bibtex_entry(bibentry))