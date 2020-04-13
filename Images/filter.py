import os
os.chdir('loading')
dirFiles = os.listdir('.')
for i in dirFiles:
    a=i.split('_')
    n=int(a[1])
    os.rename(i, str(n)+'.gif')
    print(n)
