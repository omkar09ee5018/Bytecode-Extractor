class Method_info:
    def __init__(self, pool_list):
        self.access_flags = ''
        self.name_index = ''
        self.descriptor_index = ''
        self.attributes_count = ''
        self.attributes = ''
        self.external_list = pool_list

    #need flags decomposition
    def getmethodinfo(self, f, x):  #(self, filename, method#)
        class_info_list = []
        print 'METHOD_Info', '#', x
        self.access_flags = "".join("{:02x}".format(ord(c)) for c in f.read(2))

        _access_flag = int(self.access_flags, 16)
        #print bin(_access_flag)
        print 'access_flags:',
        if self.access_flags == '0000':
            print 'No Flags'
            class_info_list.append('No Flags')
        else:
            if _access_flag & 0b01:
                flag_found = 1
                print 'ACC_PUBLIC'
                class_info_list.append('ACC_PUBLIC')
            if _access_flag & 0b10:
                flag_found = 1
                print 'ACC_PUBLIC'
                class_info_list.append('ACC_PUBLIC')
            if _access_flag & 0b100:
                flag_found = 1
                print 'ACC_PROTECTED'
                class_info_list.append('ACC_PROTECTED')
            if _access_flag & 0b1000:
                flag_found = 1
                print 'ACC_STATIC'
                class_info_list.append('ACC_STATIC')
            if _access_flag & 0b10000:
                flag_found = 1
                print 'ACC_FINAL'
                class_info_list.append('ACC_FINAL')
            if _access_flag & 0b100000:
                flag_found = 1
                print 'ACC_SYNCHRONIZED'
                class_info_list.append('ACC_SYNCHRONIZED')
            if _access_flag & 0b01000000:
                flag_found = 1
                print 'ACC_BRIDGE'
                class_info_list.append('ACC_BRIDGE')
            if _access_flag & 0b10000000:
                flag_found = 1
                print 'ACC_VARARGS'
                class_info_list.append('ACC_VARARGS')
            if _access_flag & 0b100000000:
                flag_found = 1
                print 'ACC_NATIVE'
                class_info_list.append('ACC_NATIVE')
            if _access_flag & 0b10000000000:
                flag_found = 1
                print 'ACC_ABSTRACT'
                class_info_list.append('ACC_ABSTRACT')
            if _access_flag & 0b100000000000:
                flag_found = 1
                print 'ACC_STRICT'
                class_info_list.append('ACC_STRICT')
            if _access_flag & 0b1000000000000:
                flag_found = 1
                print 'ACC_SYNTHETIC'
                class_info_list.append('ACC_SYNTHETIC')
            if flag_found != 1:
                print 'Invalid Flag'
                class_info_list.append('Invalid Flag')
        self.name_index = "".join("{:02x}".format(ord(c)) for c in f.read(2))
        class_info_list.append(self.name_index)
        print "name_index", self.name_index
        self.descriptor_index = "".join("{:02x}".format(ord(c)) for c in f.read(2))
        class_info_list.append(self.descriptor_index)
        print 'descriptor_index', self.descriptor_index
        self.attributes_count = "".join("{:02x}".format(ord(c)) for c in f.read(2))
        class_info_list.append(self.attributes_count)
        _attributes_count = int(self.attributes_count, 16)
        print 'Attributes Count', _attributes_count
        attribute_list = []
        for i in range(1, _attributes_count+1):
            att_name_index = "".join("{:02x}".format(ord(c)) for c in f.read(2))
            print 'att_name_index', att_name_index
            attribute_list.append(att_name_index)
            _att_name_index = int(att_name_index, 16)
            constant_pool_entry = self.external_list[_att_name_index-1]
            self.att_length = "".join("{:02x}".format(ord(c)) for c in f.read(4))
            _att_length = int(self.att_length, 16)
            attribute_list.append(_att_length)
            #print 'att_length', _att_length
            attributes = "".join("{:02x}".format(ord(c)) for c in f.read(_att_length))
            #print 'attributes:', attributes
            print constant_pool_entry
            attribute_list.append(attributes)
            if constant_pool_entry[2] == 'Code':
                print '----------'
                _x = str(x)
                _x += '.byc'
                target = open(_x, 'w')
                target.write("method")
                target.write(_x)
                target.write('\n')
                print 'get code'
                split_list = list(attributes)
                print 'attributes', split_list
                max_stack = "".join(split_list[0:4])     #"".join(map(str,split_list[0:1]))
                print 'max_stack', max_stack
                target.write('stack size')
                target.write(' ')
                target.write(max_stack)
                target.write('\n')
                max_local = "".join(split_list[4:8])
                print 'max_local', max_local
                target.write('locals size')
                target.write(' ')
                target.write(max_local)
                target.write('\n')
                code_length = "".join(split_list[8:16])
                _code_length = int(code_length, 16)
                print 'code_length', _code_length
                code = "".join(split_list[16:(16+(_code_length*2))])
                print 'code', code
                target.write("code")
                target.write('\n')
                target.write(code)
                target.write('\n')
                target.truncate()
                print '----------'
            else:
                print ('Ignoring attribute')
            print 'attribute_info', attribute_list
        class_info_list.append(attribute_list)
        return class_info_list