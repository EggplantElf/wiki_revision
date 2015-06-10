ssh -f xiangyu@bergbussard.ims.uni-stuttgart.de -L 3308:localhost:3306 -N
setenv LC_ALL C
mongod --dbpath ../db &
java -jar wiki.jar -t list.txt 

