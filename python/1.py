#!/usr/bin/env python

from time import time 

def Test1():
    t = time() 
    list = ['a','b','is','python','jason','hello','hill','with','phone',
        'test','dfdf','apple','pddf','ind','basic','none','baecr','var','bana','dd','wrd'] 
    list = dict.fromkeys(list, True)
    print list
    filter = [] 
    for i in range (1000000): 
        for find in ['is','hat','new','list','old','.']: 
            if find not in list: 
                filter.append(find) 
    print "total run time:",
    print time()-t



def Test2():
    t = time()
    s = ""
    list = ['a','b','b','d','e','f','g','h','i','j','k','l','m','n']
    for i in range (10000):
#        for substr in list:
#            s += substr
        s = "".join(list)
    print "total run time:",
    print time() - t



if __name__ == '__main__':
    Test2()
