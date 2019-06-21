import file.mk2


print("helloWorld")
var1 = 'fdfdfdf'

print(var1)

if 1 == 1:
    print("1")
else:
    print("2")

#rang方法是产生一个序列，一个参数时，代表的是0开始的几个数据，两个参数时代表什么开始到什么结束，但是不包含最后的
for i in range(5,10,2):
    print(i)

def ask_ok(p,r=4):
    print(r)

ask_ok(10)


dic = {"aa":100,"bbb":10}
print(dic["aa"])



list1 = ['1','2']

print(list1)

list1.append('3')

print(list1)

file.mk2.fun1()