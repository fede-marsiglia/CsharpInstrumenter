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

for d in  `find ./WidgetsLib_ -maxdepth 1 -type d`
do 
	python $orig_dir/main.py `find $d -regextype grep -type f -iregex $pattern`
done

git checkout `find -type f -iname 'logbroker\.cs'`  
git checkout `find -type f -iname 'fourthphase\.xaml\.cs'`  
git checkout `find -type f -iname 'ipcclient\.cs'`  
git checkout `find -type f -name  'SetPointPage\.xaml\.cs'`  

python $orig_dir/mainIpcClient.py `find . -regextype grep -type f -iname ipcclient.cs`

cd $orig_dir
