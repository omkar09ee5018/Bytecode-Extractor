
class Fields:
    def __init__(self,pool_list):
        self.access_flags = ''
        self.name_index = ''
        self.descriptor_index = ''
        self.attributes_count = ''
        self.attributes = ''
        self.external_list = pool_list

    def str_to_int(s):
        i = int(s, 16)
        if i >= 2**23:
            i -= 2**24
        return i

    def getField(self, f, x): #(filename,field_number)
        print 'Field #:', x
        self.access_flags = "".join("{:02x}".format(ord(c)) for c in f.read(2))
        _access_flag = int(self.access_flags, 16)
        if self.access_flags == '0000':
            print 'No Flags'
        else:
            if _access_flag & 0b01:
                flag_found = 1
                print 'ACC_PUBLIC'
            if _access_flag & 0b10:
                flag_found = 1
                print 'ACC_PUBLIC'
            if _access_flag & 0b100:
                flag_found = 1
                print 'ACC_PROTECTED'
            if _access_flag & 0b1000:
                flag_found = 1
                print 'ACC_STATIC'
            if _access_flag & 0b10000:
                flag_found = 1
                print 'ACC_FINAL'
            if _access_flag & 0b100000:
                flag_found = 1
                print 'ACC_SYNCHRONIZED'
            if _access_flag & 0b01000000:
                flag_found = 1
                print 'ACC_BRIDGE'
            if _access_flag & 0b10000000:
                flag_found = 1
                print 'ACC_VARARGS'
            if _access_flag & 0b100000000:
                flag_found = 1
                print 'ACC_NATIVE'
            if _access_flag & 0b10000000000:
                flag_found = 1
                print 'ACC_ABSTRACT'
            if _access_flag & 0b100000000000:
                flag_found = 1
                print 'ACC_STRICT'
            if _access_flag & 0b1000000000000:
                flag_found = 1
                print 'ACC_SYNTHETIC'
            if flag_found != 1:
                print 'Invalid Flag'
        self.name_index = "".join("{:02x}".format(ord(c)) for c in f.read(2))
        print self.name_index
        self.descriptor_index = "".join("{:02x}".format(ord(c)) for c in f.read(2))
        print self.descriptor_index
        attributes_count = "".join("{:02x}".format(ord(c)) for c in f.read(2))
        print attributes_count
        _attributes_count = int(attributes_count, 16)
        self.attributes = "".join("{:02x}".format(ord(c)) for c in f.read(_attributes_count))
        print 'Attributes Count', _attributes_count
        for i in range(1, _attributes_count+1):
            print 'att_name_index', "".join("{:02x}".format(ord(c)) for c in f.read(2))
            self.att_length = "".join("{:02x}".format(ord(c)) for c in f.read(4))
            _att_length = int(self.att_length, 16)
            print 'att_length', _att_length
            print "".join("{:02x}".format(ord(c)) for c in f.read(_att_length))
        print 'attributes:', self.attributes

