FILE=Images

mv ~/Downloads/$FILE.zip ./../img/team
cd ../img/team
unzip $FILE.zip -d $PWD
mv $FILE/* .
rm $FILE
cd ../../downloads
