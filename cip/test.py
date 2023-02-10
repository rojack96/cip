from cip import Cip

if __name__ == '__main__':
    cip = Cip("it")
    
    test = cip.read_file('/path/file')
    print('{\n"test":',test,' \n}')