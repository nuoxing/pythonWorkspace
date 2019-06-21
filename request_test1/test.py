import  re


def createGenerator() :
  mylist = range(3)
  for i in mylist :
     yield i*i

for i in createGenerator():
    print(i)