import os
import csv
import sys

def transform_tsv_to_yaml(input_file, output_dir='_members'):
    """
    Transform a TSV file with researcher information into a YAML/Markdown profile.
    
    Args:
        input_file (str): Path to the input TSV file
    """
    os.makedirs(output_dir, exist_ok=True)

    # Read the TSV file
    with open(input_file, 'r', encoding='utf-8') as tsv_file:

        tsv_reader = csv.DictReader(tsv_file) #, delimiter='\t') #in case we want tsv file instead.

        # Process each row (assuming single row in this case)
        for row in tsv_reader:
            # Generate the output
            output = f"""---
layout: about
inline: false
group: {row['Status']}
group_rank: {1 if "marek rei" in row["Name"].lower() else 2}

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
    orcid: {row['ORCID']}
    website: {row['Website']}
    scholar: {row['Google Scholar']}
    email: {row['Email']}
    github: {row['Github']}
    linkedin: {row['Linkedin']}
    supervisor: {row['Supervisor']}
    personal_site: {'true' if row['Website'] else 'false'}
    address: >
        {row['Room']}<br />
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