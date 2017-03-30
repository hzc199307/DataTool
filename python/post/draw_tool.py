# coding=utf-8
# by hezhichao
# 2017.02.13
# update 2017.03.07
# 画图

import os

# do this before importing pylab or pyplot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np



class DrawTool:

    # data_list是存储的坐标数据,它是一个数组。每个元素存储了一条线的数据，它的格式可以是 ([],[])
	@staticmethod
	def draw(data_list, legends, title, save_path=None, show=False, xlabel='x', ylabel='y'):
		print 'Draw ', title
		assert (len(data_list) == len(legends))
		lines = []
		ymin = 1
		ymax = 0
		plt.figure()
		for x, y in data_list:
			# print x, y
			line, = plt.plot(x, y, linewidth=2)
			# if x.shape[0] != 0:
			# if len(x) != 0:
			# 	ymax = np.max(y) if np.max(y) > ymax else ymax
			# 	ymin = np.min(y) if np.min(y) < ymin else ymin
			lines.append(line)
		plt.title(title)
		plt.legend(lines, legends, loc='best')
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		axes = plt.gca()
		axes.set_ylim([0.0, 1.0])# 限制y轴 #axes.set_ylim([ymin - 0.01, ymax + 0.01]) # 限制y轴
		axes.set_xlim([0.8, 1.0])
		# axes.set_ylim([0, 1])
		if save_path != None:
			plt.savefig(save_path)
		if show:
			plt.show()

	# data_list是存储的坐标数据,它是一个数组。每个元素存储了一条线的数据，它的格式可以是 ([],[])
	@staticmethod
	def draw_for_tprr(data_list, legends, title, save_path=None, show=False, xlabel='x', ylabel='y'):
		print 'drawing', title
		assert (len(data_list) == len(legends))
		lines = []
		ymin = 1
		ymax = 0
		fig = plt.figure()
		plt.title(title)
		ax1 = None
		for i in range(0,len(legends)):
			x, y = data_list[i]
			legend = legends[i]
			if legend == "precision" or legend == "recall":
				ax1 = fig.add_subplot(111)
				ax1.plot(x, y,label = legend )
				ax1.legend(loc='upper left')
				ax1.set_xlim([0.8, 1.0])
				ax1.set_ylim([0.0, 1.0])
				ax1.set_ylabel('precision & recall')
			if legend == "review":
				if len(x) != 0:
					ymax = np.max(y) if np.max(y) > ymax else ymax
					# 	ymin = np.min(y) if np.min(y) < ymin else ymin
				ax2 = None
				if ax1 == None:
					ax2 = fig.add_subplot(111)
				else:
					ax2 = ax1.twinx()  # this is the important function
				ax2.plot(x, y, 'r', label = legend)
				ax2.legend(loc='upper right')
				ax2.set_xlim([0.8, 1.0])
				ax2.set_ylim([0.0, ymax])
				ax2.set_ylabel('review')
				ax2.set_xlabel('x')
		if save_path != None:
			plt.savefig(save_path)
		if show:
			plt.show()