
for (( i=1; i <=$1; i++ ))
do
    nohup java -jar wiki.jar -a 100 -p 27017 -d dict.txt & 
done


