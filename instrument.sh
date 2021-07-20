orig_dir="$PWD"
directory="$1" 
pattern='.*\.cs'


cd $directory
git reset HEAD --hard
find . -type d -iname "bin" -o -iname "obj" | xargs rm -rf

rm `find -type f -iname 'setpointpage.xaml.cs'`

python3 $orig_dir/track_memory_allocs.py `find ./MTS* -regextype grep -type f -iregex $pattern`
python3 $orig_dir/track_memory_allocs.py `find ./Ip* -regextype grep -type f -iregex $pattern`
python3 $orig_dir/track_memory_allocs.py `find ./Web* -regextype grep -type f -iregex $pattern`
python3 $orig_dir/track_memory_allocs.py `find ./Communication -regextype grep -type f -iregex $pattern`
python3 $orig_dir/track_memory_allocs.py `find ./MQTT* -regextype grep -type f -iregex $pattern`
python3 $orig_dir/track_memory_allocs.py `find ./Nano* -regextype grep -type f -iregex $pattern`
python3 $orig_dir/track_memory_allocs.py `find ./Zeroconf* -type f -iregex $pattern`
python3 $orig_dir/track_memory_allocs.py `find ./ByMe_Lib -regextype grep -type f -iregex $pattern`
python3 $orig_dir/track_memory_allocs.py `find ./WidgetsLib_ -regextype grep -type f -iregex $pattern`

git checkout './ByMe_Lib/ByMe_Lib/Resx/AppResources.Designer.cs'  
git checkout './WidgetsLib_/CommonLandscapeView/Sensors/SetPointPage.xaml.cs'


cd $orig_dir
