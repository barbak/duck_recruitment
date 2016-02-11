# coding=utf-8
f = open('mac.txt', 'r')
b = 87
for i, r in enumerate(f.readlines()):

    a = r.lower().strip('\n')
    if b+i ==93:
        b=88
    print "host D250_{i} {{ hardware ethernet {mac};  fixed-address 192.168.2.{ip};}}".format(i=i, mac=a,
                                                                                            ip=b+i)
