import csv
import yaml

def csv_to_yaml(csv_path, yaml_path):
    # Read the CSV file
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = dict(reader)
    
    # Prepare the YAML structure
    yaml_data = {
        'layout': data['layout'],
        'inline': data['inline'] == 'false',  # Convert to boolean
        'group': data['group'],
        'group_rank': int(data['group_rank']),
        'title': data['title'],
        'description': data['description'],
        'lastname': data['lastname'],
        'publications': data['publications'],
        'teaser': data['teaser'],
        'profile': {
            'name': data['profile_name'],
            'position': data['profile_position'],
            'align': data['profile_align'],
            'image': data['profile_image'],
            'role': data['profile_role'],
            'orcid': data['profile_orcid'] or None,
            'website': data['profile_website'] or None,
            'email': data['profile_email'],
            'github': data['profile_github'] or None,
            'address': data['profile_address'].replace('\n', '</br>')
        }
    }
    
    # Write the YAML file
    with open(yaml_path, 'w') as yamlfile:
        yamlfile.write("---\n")
        yaml.dump(yaml_data, yamlfile, default_flow_style=False)
        yamlfile.write("\nSeniour Lecturer in NLP at Imperial College London. PhD from Cambridge University.\n\n")
        yamlfile.write("## Short Bio\n\n")
        yamlfile.write(data['short_bio'])

# Example usage
if __name__ == "__main__":
    csv_to_yaml('profile.csv', 'marek_rei.md')