# coding=utf-8
# by hezhichao
# 2017.01.31
# update 2017.01.31
# 把深图厦门包围盒数据做图片切分处理，然后可以应用到图片分类的任务里面

# 参考 http://www.programgo.com/article/5172415127/

import os
import sys

import md5
import cv2

_IMAGE_FORMATS = [".jpg",".jpeg",".png"]

class Md5Tool:

    @staticmethod
    def sumfile(fobj):    
        m = md5.new()
        while True:
            d = fobj.read(8096)
            if not d:
                break
            m.update(d)
        return m.hexdigest()

    @staticmethod
    def md5sum(fname):    
        if fname == '-':
            ret = sumfile(sys.stdin)
        else:
            try:
                f = file(fname, 'rb')
            except:
                return 'Failed to open file'
            ret = Md5Tool.sumfile(f)
            f.close()
        return ret

class ImageCut:

	@staticmethod
	def process(data_path,output_path):
		if os.path.isfile(data_path): # 如果是文件，就退出
			return
		if data_path.find("/")==-1:
			data_path += "/"
		if output_path.find("/")==-1:
			output_path += "/"
		imgs_path = data_path + "imgs/"
		labels_path = data_path + "labels/"
		output_imgs_path = output_path + "images/"
		output_imgslst_path = output_path + data_path.split("/")[-2] +"_image_original_labels.txt"
		output_imgslst_file = open(output_imgslst_path,"w+")
		count = 0
		if os.path.exists(labels_path)==False:
			print "There isn't any labels or images!"
			return
		if os.path.exists(output_imgs_path)==False:
			os.system("mkdir "+output_imgs_path)
		for filename in os.listdir(labels_path):
			count += 1
			print "No." + str(count)
			# print imgs_path+filename
			image = None
			image_path = imgs_path+filename[:-4]
			for _FORMAT in _IMAGE_FORMATS: # 为了适应多种格式的图片
				if os.path.exists(image_path + _FORMAT):
					image = cv2.imread(image_path + _FORMAT, cv2.CV_LOAD_IMAGE_COLOR)
					break
			if image == None:
				continue
			height, width, dept = image.shape
			print "origin: " + str(image.shape)+ " " + filename[:-4]
			file_read = open(labels_path+filename)
			for line in file_read:
				strs = line.strip().split()
				if strs[0] == "16" or strs[0] == "33":
					continue
				y1 = height * ( float(strs[2]) - 0.5*float(strs[4]) )
				x1 = width * ( float(strs[1]) - 0.5*float(strs[3]) )
				y2 = height * ( float(strs[2]) + 0.5*float(strs[4]) )
				x2 = width * ( float(strs[1]) + 0.5*float(strs[3]) )
				crop = image[y1:y2,x1:x2]
				cv2.imwrite( output_imgs_path+"md5.jpg" , crop)
				md5 = Md5Tool.md5sum(output_imgs_path+"md5.jpg")
				output_imgslst_file.write(md5+".jpg "+strs[0]+"\n")
				print "crop: " + str(crop.shape) + " " + md5
				os.system('mv '+output_imgs_path+'md5.jpg '+output_imgs_path+md5+".jpg")
			print ""
		output_imgslst_file.close()

if __name__ == '__main__':
    if(len(sys.argv)<3):
      print "python cut_image.py <output_path> [<data_path> ...]"
      print "# note: data_path include subfolders, such as 'imgs'/'labels'"
      exit()
    # data_paths = sys.argv[2]
    output_path = sys.argv[1]
    ImageCut.process(sys.argv[2],output_path)
    for i in range(3,len(sys.argv)):
        ImageCut.process(sys.argv[i],output_path)
