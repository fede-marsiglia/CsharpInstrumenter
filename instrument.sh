for d in `find ../../Documents/byme_app_mobile -maxdepth 1 -type d`
do 
	if [[ $d != *"Xamarin"* ]]; then

		python main.py `find $d -type f -iregex '.*\.cs'`

	fi
done
