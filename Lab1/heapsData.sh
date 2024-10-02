for i in arg 
do
    python3 IndexFiles.py --index heaps --path path
    python3 CountWords.py --index heaps > dataHeaps$i.txt 
done;
