# How to convert data:

1. Download table (it will have the name NLPLists(People.csv))
Download the following table:
https://imperiallondon-my.sharepoint.com/:x:/r/personal/nr1713_ic_ac_uk/_layouts/15/Doc.aspx?sourcedoc=%7B4DE58410-CE4A-4C23-9257-39C162C37101%7D&file=NLPLists.xlsx&action=default&mobileredirect=true

2. Generate example profiles:
Then run:
```bash
python3 convert.py
```

3. IF READY TO OVERRIDE PRODUCTION:
```bash
python3 convert.py production
```

4. Generate BIB entries:
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
bundle exec jekyll serve
```