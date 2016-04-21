import os.path
import time, zipfile, sys, binascii, math, StringIO
from Fields import Fields
from Method_info import Method_info


def checkfile():
    print 'importing file:', sys.argv[1]
    strsplit = sys.argv[1].split('.')
    if not strsplit[1] == "class":
        print "not a class file"

def getmagic(f):
    return "".join("{:02x}".format(ord(c)) for c in f.read(4))

def getminor(f):
    return "".join("{:02x}".format(ord(c)) for c in f.read(2))

def getmajor(f):
    return "".join("{:02x}".format(ord(c)) for c in f.read(2))

def getPoolSize(f):
    return "".join("{:02x}".format(ord(c)) for c in f.read(2))

# def getPool(f):
#    global _poolSize
#    return "".join("{:02x}".format(ord(c)) for c in f.read(_poolSize))

def getHex(binary_str):
    return "".join("{:02x}".format(ord(c)) for c in binary_str)

def str_to_int(s):
    i = int(s, 16)
    if i >= 2 ** 23:
        i -= 2 ** 24
    return i

def binStr_to_int(str):
    i = 0
    _str = list(str)[::-1]
    for x in range(0, len(_str)):
        i += math.pow(2, x) * int(_str[x])
    return i

def getPool(f):
    global pool_list, pool_offset
    i = 0
    poolSize = getPoolSize(f)
    _poolSize = str_to_int(poolSize)
    print '#Elements in pool:', _poolSize - 1
    print 'Constant Pool Table'
    file_cp = 'const_pool.byc'
    target = open(file_cp, 'w')
    target.write("CONSTANT POOL")
    target.write('\n')
    target.write('SIZE')
    target.write(poolSize)
    target.write('\n')
    while i < _poolSize-1:
        print 'Constant pool element #', i
        Current_pool_element = f.read(1)
        _Current_pool_element = ''.join(format(ord(x), 'b') for x in Current_pool_element)
        ___Current_pool_element = binStr_to_int(_Current_pool_element)
        # binascii.a2b_uu(Current_pool_element)
        # print
        internal_list = []
        if (___Current_pool_element == 9):
            internal_list.append('CONSTANT_Fieldref:')
            target.write('CONSTANT_Fieldref:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            line2 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            internal_list.append(line2)
            target.write(' ')
            target.write(line2)
            target.write('\n')
        elif (___Current_pool_element == 10):
            internal_list.append( 'CONSTANT_Methodref:')
            target.write('CONSTANT_Methodref:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            line2 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            internal_list.append(line2)
            target.write(' ')
            target.write(line2)
            target.write('\n')
        elif (___Current_pool_element == 11):
            internal_list.append( 'CONSTANT_InterfaceMethodref:')
            target.write('CONSTANT_InterfaceMethodref:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            line2 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            internal_list.append(line2)
            target.write(' ')
            target.write(line2)
            target.write('\n')
        elif (___Current_pool_element == 7):
            internal_list.append( 'CONSTANT_Class_info:')
            target.write('CONSTANT_Class_info:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            target.write('\n')
        elif (___Current_pool_element == 8):
            internal_list.append( 'CONSTANT_String')
            target.write('CONSTANT_String:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            target.write('\n')
        elif (___Current_pool_element == 3):
            internal_list.append( 'CONSTANT_Integer')
            target.write('CONSTANT_Integer:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(4)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            target.write('\n')
        elif (___Current_pool_element == 4):
            internal_list.append( 'CONSTANT_Float')
            target.write('CONSTANT_Float:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(4)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            target.write('\n')
        elif (___Current_pool_element == 5):
            internal_list.append('CONSTANT_Long')
            target.write('CONSTANT_Long:')
            line1 = ("".join("{:02x}".format(ord(c)) for c in f.read(4)))
            line2 = ("".join("{:02x}".format(ord(c)) for c in f.read(4)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            target.write('\n')
            pool_list.append(internal_list)
            internal_list = []
            target.write('CONSTANT_Long:')
            internal_list.append('CONSTANT_Long')
            internal_list.append(line2)
            target.write(' ')
            target.write(line2)
            target.write('\n')
            i += 1
        elif (___Current_pool_element == 6):
            internal_list.append('CONSTANT_Double')
            target.write('CONSTANT_Double:')
            line1 = ("".join("{:02x}".format(ord(c)) for c in f.read(4)))
            line2 = ("".join("{:02x}".format(ord(c)) for c in f.read(4)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            target.write('\n')
            pool_list.append(internal_list)
            internal_list = []
            internal_list.append('CONSTANT_Double')
            target.write('CONSTANT_Double:')
            internal_list.append(line2)
            target.write(' ')
            target.write(line2)
            target.write('\n')
            i += 1
        elif (___Current_pool_element == 12):
            internal_list.append('CONSTANT_NameAndType')
            target.write('CONSTANT_NameAndType:')
            line1 = ("".join("{:02x}".format(ord(c)) for c in f.read(2)))
            line2 = ("".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            internal_list.append(line2)
            target.write(' ')
            target.write(line2)
            target.write('\n')
        elif (___Current_pool_element == 1):
            internal_list.append( 'CONSTANT_Utf8')
            target.write('CONSTANT_Utf8:')
            Utf8_len = str_to_int("".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append( Utf8_len)
            target.write(' ')
            target.write(str(Utf8_len))
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(Utf8_len)).decode("hex"))
            internal_list.append( line1)
            target.write(' ')
            target.write(line1)
            target.write('\n')
        elif (___Current_pool_element == 15):
            internal_list.append( 'CONSTANT_MethodHandle')
            target.write('CONSTANT_MethodHandle:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(1)))
            line2 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            internal_list.append(line2)
            target.write(' ')
            target.write(line2)
            target.write('\n')
        elif (___Current_pool_element == 16):
            internal_list.append( 'CONSTANT_MethodType')
            target.write('CONSTANT_MethodType:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            target.write('\n')
        elif (___Current_pool_element == '18'):
            internal_list.append( 'CONSTANT_InvokeDynamic')
            target.write( 'CONSTANT_InvokeDynamic:')
            line1 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            line2 = ( "".join("{:02x}".format(ord(c)) for c in f.read(2)))
            internal_list.append(line1)
            target.write(' ')
            target.write(line1)
            internal_list.append(line2)
            target.write(' ')
            target.write(line2)
            target.write('\n')
        else:
            print 'invalid constant pool parse'
        pool_list.append(internal_list)
        i += 1


if __name__ == "__main__":
    pool_offset = 0
    pool_list = []
    filename = sys.argv[1]
    f = open(filename, 'rb')
    magic = getmagic(f)
    if magic != 'cafebabe':
        print 'class file format not supported'
        exit()
    minor = getminor(f)
    major = getmajor(f)
    print 'magic:', magic
    print 'version', 'minor:', minor,
    print 'major:', major
    getPool(f)
    print pool_list
    access_flags = "".join("{:02x}".format(ord(c)) for c in f.read(2))
    print 'flags', access_flags
    this_class = "".join("{:02x}".format(ord(c)) for c in f.read(2))
    print 'this class', this_class
    _this_class = int(this_class, 16)
    print '----------'
    print pool_list[_this_class-1]
    print '----------'
    super_class = "".join("{:02x}".format(ord(c)) for c in f.read(2))
    print 'super class', super_class
    _super_class = int(super_class, 16)
    if _super_class != 0:
        print '----------'
        print pool_list[_super_class-1]
        print '----------'
    interfaces_count = "".join("{:02x}".format(ord(c)) for c in f.read(2))
    print 'interfaces_count', interfaces_count
    _interfaces_count = str_to_int(interfaces_count)
    interfaces = "".join("{:02x}".format(ord(c)) for c in f.read((2 * _interfaces_count)))
    print 'interfaces', interfaces
    fields_count = "".join("{:02x}".format(ord(c)) for c in f.read(2))
    _fields_count = str_to_int(fields_count)
    print '#of fields', _fields_count
    if _fields_count != 0:
        fields = Fields(pool_list)
        for i in range(1, _fields_count + 1):
            fields.getField(f, i)
    method_count = "".join("{:02x}".format(ord(c)) for c in f.read(2))
    _method_count = str_to_int(method_count)
    # foo_ = foo()
    # foo_()
    method_info = Method_info(pool_list)
    method_list = []
    print '#of methods', _method_count
    for x in range(1, _method_count + 1):
        method_list.append(method_info.getmethodinfo(f, x))
    print 'Printing LIST'
    print method_list
    attribute_count_class_file = "".join("{:02x}".format(ord(c)) for c in f.read(2))
    _attribute_count_class_file = int(attribute_count_class_file, 16)
    print 'attribute_count_class_file', _attribute_count_class_file
    for i in range(1, _attribute_count_class_file + 1):
        print 'att_name_index', "".join("{:02x}".format(ord(c)) for c in f.read(2))
        att_length = "".join("{:02x}".format(ord(c)) for c in f.read(4))
        _att_length = int(att_length, 16)
        print 'att_length', _att_length
        print "".join("{:02x}".format(ord(c)) for c in f.read(_att_length))
    exit()
