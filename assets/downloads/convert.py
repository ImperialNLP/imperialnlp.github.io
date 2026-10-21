import os
import csv
import sys
import re


def clean_url(url, site):
    """
    Check if the URL is already an ID, and if not, extract the ID from the URL.
    """
    if not url:
        return url

    if site == "orcid":
        if not url.startswith("http"):
            return url
        else:
            return re.search(r"orcid\.org/(\w+)", url).group(1)
    if site == "scholar":
        if not url.startswith("http"):
            return url
        else:
            return re.search(r"user=(\w+)", url).group(1)
    if site == "linkedin":
        if not url.startswith("http"):
            return url
        else:
            return re.search(r"linkedin\.com/in/(\w+)", url).group(1)

    if site == "github":
        if not url.startswith("http"):
            return url
        else:
            return re.search(r"github\.com/(\w+)", url).group(1)

    return url

def assign_group_rank(status):
    """
    Faculty -> 1
    Postdoc -> 2
    PhD -> 3
    Fellow -> 4
    Visitor -> 5
    Alumni -> 6
    """
    if status.lower() == "faculty":
        return 1
    elif status.lower() == "postdoc":
        return 2
    elif status.lower() == "phd":
        return 3
    elif status.lower() == "fellow":
        return 4
    elif status.lower() == "visitor":
        return 5
    elif status.lower() == "alumni":
        return 6
    else:
        return 7

def transform_tsv_to_yaml(input_file, output_dir='_members'):
    """
    Transform a TSV file with researcher information into a YAML/Markdown profile.
    
    Args:
        input_file (str): Path to the input TSV file
    """
    os.makedirs(output_dir, exist_ok=True)

    # Read the TSV file
    with open(input_file, 'r', encoding='utf-8') as tsv_file:
    # with open(input_file, 'r') as tsv_file:

        tsv_reader = csv.DictReader(tsv_file) #, delimiter='\t') #in case we want tsv file instead.

        # Process each row (assuming single row in this case)
        for row in tsv_reader:
            # Clean all key names
            new_row = {}
            for key, value in row.items():
                cleaned_key = key.replace('\ufeff', '')
                new_row[cleaned_key] = value
            row = new_row
            print(row.keys())
            # Generate the output
            output = f"""---
layout: about
inline: false
group: {row['Status']}
group_rank: {assign_group_rank(row['Status'])}

title: {row['Name']}
lastname: {row['Name'].split()[-1]}
publications: 'author^=*{row['Name'].split()[-1]}'

teaser: >
    {row['Short Snippet']}

profile:
    name: {row['Name']}
    position: {row['Position']}
    image: {row['Picture']}
    role: {row['Status']}
    orcid: {clean_url(row['ORCID'], 'orcid')}
    website: {clean_url(row['Website'], 'website')}
    scholar: {clean_url(row['Google Scholar'], 'scholar')}
    email: {row['Email']}
    github: {clean_url(row['Github'], 'github')}
    linkedin: {clean_url(row['Linkedin'], 'linkedin')}
    supervisor: {row['Supervisor']}
    personal_site: {'true' if row['Website'] else 'false'}
    address: >
        {row['Room']}{'<br />' if row['Room'] else ''}
        Imperial College London<br />
        London
---


## Short Bio

{row['Longer Bio']}

"""
            first_name = row['Name'].split()[0].lower()
            if (first_name.lower() == "dr") or first_name.lower() == "dr." or first_name.lower() == "prof" or first_name.lower() == "prof." or first_name.lower() == "professor":
                first_name = row["Name"].split()[1].lower()

            # Create output filename
            output_filename = os.path.join(output_dir, f"{first_name}.md")
            
            # Write to file
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(output)
            
            print(f"Created profile for {row['Name']} at {output_filename}")


def main():

    input_file="NLPLists(People).csv"
    output = "_members"

    if len(sys.argv) == 2:
        if sys.argv[1] == "production":
            output = "../../_members"


    transform_tsv_to_yaml(input_file, output)

if __name__ == "__main__":
    main()