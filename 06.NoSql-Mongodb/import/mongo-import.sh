for f in *.csv
do
    filename=$(basename "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    echo 'mongoimport -d sample -c "' + $filename + '" --type csv --file "' + $f + '" --headerline'
    mongoimport -d sample -c "$filename" --type csv --file "$f" --headerline
done
