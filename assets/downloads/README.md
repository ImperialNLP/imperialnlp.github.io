# Building the NLP website
 
Imperial NLP Website:
[https://nlp.doc.ic.ac.uk]

Code lives on github: https://github.com/ImperialNLP/imperialnlp.github.io
It consists of:

1. Spreadsheet URL: (Keeps track of people as a spreadsheet)
(NLPLists.xlsx)[https://imperiallondon-my.sharepoint.com/:x:/g/personal/nr1713_ic_ac_uk/ERCE5U1KziNMklc5wWLDcQEBu73pj8BkJvrJiKg2yT0NTw?e=KiRNiE]

2. Bibliography Folder: (Keeps track of papers in form of .bib files) [attached is a screenshot that describes what is what in each bib entry]
Bibliography
[https://imperiallondon-my.sharepoint.com/:f:/g/personal/nr1713_ic_ac_uk/Et2ck1_xp7FIg9rupamDGa8B7kFHGBFfQdeeoDMfOUzWwQ?e=gLqVrb]

3. Images Folder: (Keeps track of photos for people and other images) [profile pictures should be ideally in square format]
Images
[https://imperiallondon-my.sharepoint.com/:f:/g/personal/nr1713_ic_ac_uk/EhtrbA5yP3xFqz9J98mmq9gBtUVx5VZP8ogeZa5IX4aNqw?e=lG1evL]

## How to convert data:

1. Download table (it will have the name NLPLists(People.csv))
Download the following table:
[https://imperiallondon-my.sharepoint.com/:x:/r/personal/nr1713_ic_ac_uk/_layouts/15/Doc.aspx?sourcedoc=%7B4DE58410-CE4A-4C23-9257-39C162C37101%7D&file=NLPLists.xlsx&action=default&mobileredirect=true]

2. Generate example profiles:
Run:
```bash
python3 convert.py
```

3. IF READY TO OVERRIDE PRODUCTION:
Run:
```bash
python3 convert.py production
```

## How to convert Bib entries:
1. Download Bib files from:
[https://imperiallondon-my.sharepoint.com/my?id=%2Fpersonal%2Fnr1713%5Fic%5Fac%5Fuk%2FDocuments%2FNLP%20Website%2FBibliography&ga=1]

2. Generate BIB entries (PRODUCTION):
```bash
python3 transform_bibtext.py production
```


### Testing website locally:

1. Installation
```bash
bundle install
```

2. Running locally:
```bash
bundle exec jekyll serve -l -H localhost
```

<!-- bundle exec jekyll serve
 -->

<!-- bundle install -->
<!-- bundle exec jekyll serve -l -H localhost -->