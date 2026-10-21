#  FILE=OneDrive_1_16-04-2025.zip
FILE=Bibliography.zip

#  mv ~/Downloads/$FILE ../bibliography
 cd ../bibliography
 unzip $FILE
 cd ../downloads
 python3 transform_bibtex.py production