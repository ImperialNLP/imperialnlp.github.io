#  FILE=OneDrive_1_16-04-2025.zip
FILE=Bibliography

 mv ~/Downloads/$FILE.zip ../bibliography
 cd ../bibliography
 unzip $FILE.zip
 mv $FILE/* .
rm $FILE.zip
 cd ../downloads
 python3 transform_bibtex.py production