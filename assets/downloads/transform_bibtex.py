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

# Characters allowed in a citation key, e.g. "lauscher-2026" or "smith2020nlp"
ENTRY_ID_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:+-]*$')

def _split_top_level(text):
    """
    Split text on the commas that are not nested inside braces.

    Args:
        text (str): Text to split (typically the body of a BibTeX entry)

    Returns:
        list: The comma separated segments, in order
    """
    parts = []
    current = ''
    depth = 0
    for i, char in enumerate(text):
        if char == '{':
            depth += 1
            current += char
        elif char == '}':
            depth -= 1
            current += char
            if depth < 0:
                # The entry itself is closed; keep the remainder untouched
                current += text[i + 1:]
                break
        elif char == ',' and depth == 0:
            parts.append(current)
            current = ''
        else:
            current += char
    parts.append(current)
    return parts

def extract_entry_id(original_entry):
    """
    Extract the citation key (e.g. lauscher-2026) of a BibTeX entry.

    The key is the first segment after "@type{" that is not a "field = {value}"
    assignment. This tolerates entries where a field such as
    "bibtex_show = {true}" was placed before the key.

    Args:
        original_entry (str): The original BibTeX entry

    Returns:
        str or None: The citation key or None if it could not be found
    """
    match = re.match(r'\s*@[A-Za-z]+\s*\{', original_entry)
    if not match:
        return None

    for segment in _split_top_level(original_entry[match.end():]):
        stripped = segment.strip()
        if not stripped or stripped == '}':
            continue
        if '=' in stripped:
            # A field (e.g. bibtex_show = {true}) precedes the citation key
            continue
        return stripped
    return None

def validate_entry_id(original_entry):
    """
    Validate the citation key of an entry.

    A valid key directly follows the entry type (e.g. "@article{lauscher-2026,")
    and only consists of allowed characters. A field such as
    "bibtex_show = {true}" placed in front of the key is reported as invalid.

    Args:
        original_entry (str): The original BibTeX entry

    Returns:
        tuple(str or None, bool): The citation key and whether it is valid
    """
    entry_id = extract_entry_id(original_entry)
    if entry_id is None:
        print("  [warning] Could not find a citation key in this entry.")
        return None, False

    match = re.match(r'\s*@[A-Za-z]+\s*\{\s*([^,\s}]*)', original_entry)
    follows_type = bool(match) and match.group(1) == entry_id
    valid_chars = bool(ENTRY_ID_PATTERN.match(entry_id))

    if not follows_type:
        print(f"  [warning] Citation key '{entry_id}' does not directly follow the "
              f"entry type (a field such as bibtex_show = {{true}} precedes it).")
    if not valid_chars:
        print(f"  [warning] Citation key '{entry_id}' contains unexpected characters.")

    return entry_id, follows_type and valid_chars

def normalize_entry_header(original_entry, entry_id):
    """
    Move the citation key directly behind the entry type, e.g. "@article{ID,".

    Args:
        original_entry (str): The original BibTeX entry
        entry_id (str): The citation key of the entry

    Returns:
        str: The entry with the citation key in the correct position
    """
    match = re.match(r'(\s*@[A-Za-z]+\s*\{)(.*)', original_entry, re.DOTALL)
    if not match:
        return original_entry
    header, body = match.group(1), match.group(2)

    kept = []
    removed = False
    for segment in _split_top_level(body):
        if not removed and segment.strip() == entry_id:
            removed = True
            continue
        kept.append(segment)

    rest = ','.join(kept).lstrip()
    if not rest:
        return f"{header}{entry_id},\n"
    return f"{header}{entry_id},\n  {rest}"

def transform_bibtex_entry(original_entry):
    """
    Transform a single BibTeX entry by adding html, abbr, and bibtex_show fields.
    
    Args:
        original_entry (str): The original BibTeX entry
    
    Returns:

        tuple(str or None, str): The citation key of the entry (None if it could
        not be determined) and the transformed BibTeX entry
    """
    # Validate the citation key and repair its position if necessary
    entry_id, is_valid = validate_entry_id(original_entry)
    if entry_id is not None and not is_valid:
        original_entry = normalize_entry_header(original_entry, entry_id)

    # Remove trailing comma and newline at the end of the entry
    original_entry = original_entry.strip().rstrip(',')
    

    new_fields = []
    # Don't add bibtex_show twice (it may already be present)
    if not re.search(r'\bbibtex_show\s*=', original_entry):
        new_fields.append('  bibtex_show = {true},')

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
    

    return entry_id, transformed_entry

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
    # pattern = r'@\w+\{(?:[^{}]|[^{}]*\{[^{}]*\}[^{}]*|[^{}]*\{[^{}]*\{[^{}]*\}[^{}]*\}[^{}]*|[^{}]*\{[^{}]*\{[^{}]*\{[^{}]*\}[^{}]*\}[^{}]*\}[^{}]*)*\}' #zero, 1, 2 and 3 inside brackets.
    # print("running regex...")
    # entries = re.findall(pattern, file_contents, re.DOTALL)
    
    # Alternative approach: find all @-starting entries and then parse them
    # This function is not thread-safe, so we need to use a lock
    # import threading
    # lock = threading.Lock()
    entries = []
    lines = file_contents.split('\n')
    current_entry = None
    bracket_count = 0
    for line in lines:
        if line.startswith('@'):
            if current_entry is not None:
                entries.append(current_entry)
            current_entry = line + '\n'
            bracket_count = line.count('{') - line.count('}')
        elif current_entry is not None:
            current_entry += line + '\n'
            bracket_count += line.count('{') - line.count('}')
            if bracket_count == 0:
                entries.append(current_entry)
                current_entry = None
    if current_entry is not None:
        entries.append(current_entry)

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

    # Track citation keys so every entry is only written once
    seen_ids = set()
    duplicate_ids = []
    entries_without_id = []
    total_entries = 0
    
    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        print("---")
        print(f"Processing File:{filename}")
        # Check if the file is a .bib file
        if filename.endswith('.bib'):
            input_file = os.path.join(input_directory, filename)
            
            print("Extracting bib entries...")
            # Extract entries from the file
            entries = extract_bibtex_entries(input_file)
            print(f"Len entries in file:{len(entries)}")






            total_entries += len(entries)

            # Transform entries and keep only unique ones
            for entry in entries:
                entry_id, transformed_entry = transform_bibtex_entry(entry)

                if entry_id is None:
                    print(f"  [warning] Entry without a citation key in {filename}; "
                          f"keeping it, but it cannot be de-duplicated.")
                    entries_without_id.append(filename)
                    all_entries.append(transformed_entry)
                    continue

                if entry_id in seen_ids:
                    print(f"  [duplicate] Skipping '{entry_id}' (already collected).")
                    duplicate_ids.append(entry_id)
                    continue

                seen_ids.add(entry_id)
                all_entries.append(transformed_entry)

            processed_files.append(input_file)
        else:
            print("skipping (not .bib file).")
    
    # Write accumulated entries to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(all_entries))
        
        print(f"Accumulated and transformed entries from {len(processed_files)} files.")

        print(f"Entries found: {total_entries}")
        print(f"Unique citation keys: {len(seen_ids)}")
        if duplicate_ids:
            print(f"Skipped {len(duplicate_ids)} duplicate(s): "
                  f"{', '.join(sorted(set(duplicate_ids)))}")
        if entries_without_id:
            print(f"Warning: {len(entries_without_id)} entries had no detectable "
                  f"citation key (in {', '.join(sorted(set(entries_without_id)))}).")
        print(f"Total entries written: {len(all_entries)}")
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