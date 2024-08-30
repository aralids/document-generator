inotifywait -m /home/kali/document-generator/input -e create -e delete -e moved_from -e moved_to |
    while read dir action file; do
    	if [ $action = "CREATE" ]
    	then
    	     echo .bp | groff -T pdf > /home/kali/document-generator/output/${file%.*}.pdf
        elif [ $action = "MOVED_TO" ]
        then 
            python /home/kali/document-generator/main.py $dir/$file "${file%.*}"
        elif [ $action = "MOVED_FROM" ] || [ $action = "DELETE" ]
        then
            rm /home/kali/document-generator/output/${file%.*}.pdf
        fi
    done
