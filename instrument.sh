python="python"
if ! [ -x "$(command -v python)" ]; then
  echo 'Python is not installed. Trying python3'
fi

python="python3"
if ! [ -x "$(command -v python3)" ]; then
  echo 'Ppython is not installed.'
fi

orig_dir="$PWD"
directory="$1" 
pattern='.*\.cs'


cd $directory
git reset HEAD --hard
find . -type d -iname "bin" -o -iname "obj" | xargs rm -rf

$python $orig_dir/main.py `find ./Mobile* -regextype grep -type f -iregex $pattern`
$python $orig_dir/main.py `find ./MTS* -regextype grep -type f -iregex $pattern`
$python $orig_dir/main.py `find ./Ip* -regextype grep -type f -iregex $pattern`
$python $orig_dir/main.py `find ./Web* -regextype grep -type f -iregex $pattern`
$python $orig_dir/main.py `find ./Communication -regextype grep -type f -iregex $pattern`
$python $orig_dir/main.py `find ./MQTT* -regextype grep -type f -iregex $pattern`
$python $orig_dir/main.py `find ./Widgets* -regextype grep -type f -iregex $pattern`
$python $orig_dir/main.py `find ./Nano* -regextype grep -type f -iregex $pattern`
$python $orig_dir/main.py `find ./Zeroconf* -type f -iregex $pattern`
$python $orig_dir/main.py `find ./ANR* -regextype grep -type f -iregex $pattern`

cd $orig_dir