orig_dir="$PWD"
directory="$1" 
pattern='.*\.cs'


cd $directory
git reset HEAD --hard
find . -type d -iname "bin" -o -iname "obj" | xargs rm -rf

python $orig_dir/main.py `find ./MTS* -regextype grep -type f -iregex $pattern`
python $orig_dir/main.py `find ./Ip* -regextype grep -type f -iregex $pattern`
python $orig_dir/main.py `find ./Web* -regextype grep -type f -iregex $pattern`
python $orig_dir/main.py `find ./Communication -regextype grep -type f -iregex $pattern`
python $orig_dir/main.py `find ./MQTT* -regextype grep -type f -iregex $pattern`
python $orig_dir/main.py `find ./Nano* -regextype grep -type f -iregex $pattern`
python $orig_dir/main.py `find ./Zeroconf* -type f -iregex $pattern`
python $orig_dir/main.py `find ./ByMe_Lib -regextype grep -type f -iregex $pattern`
python $orig_dir/main.py `find ./WidgetsLib_ -regextype grep -type f -iregex $pattern`

git checkout `find -type f -iname 'logbroker\.cs'`  
git checkout `find -type f -iname 'fourthphase\.xaml\.cs'`  
git checkout `find -type f -iname 'ipcclient\.cs'`  
git checkout `find -type f -name  'SetPointPage\.xaml\.cs'`  
git checkout `find -type f -name  'Extensions\.cs'`  

cd $orig_dir
