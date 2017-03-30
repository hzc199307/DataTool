import md5
import sys
import shutil

def sumfile(fobj):    
    m = md5.new()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()


def md5sum(fname):    
    if fname == '-':
        ret = sumfile(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            return 'Failed to open file'
        ret = sumfile(f)
        f.close()
    return ret

if __name__ == '__main__':
#    for fname in sys.argv[1:]:
#        print '%32s  %s' % (md5sum(fname), fname)
    fileIn = open(sys.argv[1])
#fileOut = open(sys.argv[2],"w+")
    index = 0
    for line in fileIn:
        index += 1
        print index
	strs = line.strip().split()
  	shutil.move(strs[0],sys.argv[2]+"/"+md5sum(strs[0])+".jpg")
#	fileOut.write(md5sum(strs[0])+".jpg\t"+label+"\t"+strs[0]+"\n")
    fileIn.close()
#   fileOut.close()
