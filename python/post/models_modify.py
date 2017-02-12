# coding=utf-8
# by hezhichao
# 2016.12.29

import numpy as np
import os
import json
import sys
import copy

class ModelsModify:

    @staticmethod
    def modify_layer_weights(net, layer_name, weights=None):
        print "modify_layer_weights"
        for p in net.params:
            print p
            if p == layer_name:
                for i in range(len(net.params[p])):
                    
                    print weights.ndim
                    print "\n# net.params[p]["+str(i)+"].data.shape :"
                    print net.params[p][i].data.shape
                    print "\n# net.params[p]["+str(i)+"].data.ndim :"
                    print net.params[p][i].data.ndim
                    print "\n# net.params[p]["+str(i)+"].data.flat :"
                    print net.params[p][i].data.flat
                    net.params[p][i].data.flat = weights
                    continue # 只弄weights，不弄bias
                continue

    @staticmethod
    def copy_layer_weights(net, layer_name_dst, net_src, layer_name_src):
        print "\n# net.params[\"loss3/classifier_scene23_merge\"][0].data.shape :" + str(net.params["loss3/classifier_scene23_merge"][0].data.shape)
        print "copy_layer_weights"
        layer_src = []
        for p in net.params:
            if p == layer_name_src:
                print "### Find " + p
                for i in range(len(net.params[p])):
                    print "\n# net.params[p]["+str(i)+"].data.ndim :" + str(net.params[p][i].data.ndim)
                    print "\n# net.params[p]["+str(i)+"].data.shape :" + str(net.params[p][i].data.shape)
                    print "\n# net.params[p]["+str(i)+"].data.flat :" + str(net.params[p][i].data.flat)
                    print len(net.params[p][i].data.flat)
                    layer_src.append(net.params[p][i].data.flat)
                continue
        for p in net.params:
            if p == layer_name_dst:
                print "### Find " + p
                for i in range(len(net.params[p])):
                    print "------ "
                    print len(layer_src[i])
                    print layer_src[i][0]
                    print net.params[p][i].data.flat[0]
                    net.params[p][i].data.flat = layer_src[i]
                    print net.params[p][i].data.flat[0]
                print "copy from "+layer_name_src+" to "+layer_name_dst
                continue
        net.params[layer_name_dst][0].data.flat = net_src.params[layer_name_src][0].data.flat 
        
    def scene23_modify_v2(self,net):
        zeros = np.zeros((1024,1024,2,1))
        for j in range(0,1024):
            zeros[j][j][1][0] = 1
        ModelsModify.modify_layer_weights(net, "below_pool5/7x7_s1_below", zeros)
        net.save("./tmp.caffemodel")
        

    def scene23_modify_v3(self,net,net_src):
        ModelsModify.copy_layer_weights(net, "loss3/classifier_scene23_below", net_src,"loss3/classifier_scene23")
        zeros = np.zeros((23,46))
        for j in range(0,23):
            if j==6 or j==8 or j==9 or j==12 or j==13:
                zeros[j][j+23] = 2
            else:
                zeros[j][j] = 1
        ModelsModify.modify_layer_weights(net, "loss3/classifier_scene23_merge", zeros)
        net.save("/home/hezhichao/work/greendam/models/scene_v2_model/v2_1_0_lr0001/scene_v2_1_0_lr00001_iter16k_modify_v3.caffemodel")

    def scene23_modify_v4(self,net,net_src):
        ModelsModify.copy_layer_weights(net, "loss3/classifier_scene23_below", net_src,"loss3/classifier_scene23")
        zeros = np.zeros((23,46))
        for j in range(0,23):
            if j==6 or j==8 or j==9 or j==12 or j==13:
                zeros[j][j+23] = 1
            zeros[j][j] = 1
        ModelsModify.modify_layer_weights(net, "loss3/classifier_scene23_merge", zeros)
        net.save("/home/hezhichao/work/greendam/models/scene_v2_model/v2_1_0_lr0001/scene_v2_1_0_lr00001_iter16k_modify_v4.caffemodel")

    def scene23_modify_v5(self,net):
        zeros_above = np.zeros((23,1024,3,1))
        zeros_center = np.zeros((23,1024,3,1))
        zeros_below = np.zeros((23,1024,3,1))
        for i in range(net.params["loss3/classifier_scene23"][0].data.shape[0]):
            for j in range(net.params["loss3/classifier_scene23"][0].data.shape[1]):
                zeros_above[i][j][0][0] = net.params["loss3/classifier_scene23"][0].data.flat[i*1024+j]
                zeros_center[i][j][1][0] = net.params["loss3/classifier_scene23"][0].data.flat[i*1024+j]
                zeros_below[i][j][2][0] = net.params["loss3/classifier_scene23"][0].data.flat[i*1024+j]
        ModelsModify.modify_layer_weights(net, "loss3/classifier_scene23_above", zeros_above)
        ModelsModify.modify_layer_weights(net, "loss3/classifier_scene23_center", zeros_center)
        ModelsModify.modify_layer_weights(net, "loss3/classifier_scene23_below", zeros_below)
        zeros_del0 = np.zeros((23,23))
        for i in range(1,23):
            zeros_del0[i][i]=1
        ModelsModify.modify_layer_weights(net, "prob_scene_above_del0", zeros_del0)
        ModelsModify.modify_layer_weights(net, "prob_scene_center_del0", zeros_del0)
        ModelsModify.modify_layer_weights(net, "prob_scene_below_del0", zeros_del0)
        net.save("/home/hezhichao/work/greendam/models/scene_v2_model/v2_1_0_lr0001/scene_v2_1_0_lr00001_iter16k_modify_v5_1.caffemodel")

    @staticmethod
    def transplant(new_net, net, prefix='',suffix=''):
        """
        Transfer weights by copying matching parameters, coercing parameters of
        incompatible shape, and dropping unmatched parameters.
        The coercion is useful to convert fully connected layers to their
        equivalent convolutional layers, since the weights are the same and only
        the shapes are different.  In particular, equivalent fully connected and
        convolution layers have shapes O x I and O x I x H x W respectively for O
        outputs channels, I input channels, H kernel height, and W kernel width.
        Both  `net` to `new_net` arguments must be instantiated `caffe.Net`s.
        """
        for p in net.params:
            # classifier采用后缀形式，其他layer一律采取了前缀模式
            p_new = p
            print p + " prefix=" + prefix + " suffix=" + suffix
            if p.find(prefix)==-1 or p.find(suffix)==-1:
                if prefix != '':
                    p_new = prefix + "_" + p
                if suffix != '':
                    p_new = p + "_" + suffix
            if p_new not in new_net.params:
                print 'dropping', p
                continue
            for i in range(len(net.params[p])):
                if i > (len(new_net.params[p_new]) - 1):
                    print 'dropping', p, i
                    break
                if net.params[p][i].data.shape != new_net.params[p_new][i].data.shape:
                    print 'coercing', p, i, 'from', net.params[p][i].data.shape, 'to', new_net.params[p_new][i].data.shape
                else:
                    print 'copying', p, ' -> ', p_new, i
                new_net.params[p_new][i].data.flat = net.params[p][i].data.flat

    def read_dp_json(self, dp_json_file):
        sys.path.insert(0, '/home/hezhichao/work/caffe/python')
        import caffe
        caffe.set_device(0)
        caffe.set_mode_gpu()
        # self.dp_json = json.load(open(dp_json_file))
        # caffe_root = self.dp_json["caffe_config"]["caffe_root"]  # this file should be run from {caffe_root}/examples (otherwise change this line)
        # sys.path.insert(0, caffe_root + 'python')
        # import caffe
        # caffe.set_device(int(self.dp_json["caffe_config"]["device"]))
        # if (self.dp_json["caffe_config"]["mode"] == "gpu") | (self.dp_json["caffe_config"]["mode"] == "GPU"):
        #     caffe.set_mode_gpu()
        # else:
        #     caffe.set_mode_cpu()

    def process(self,caffemodel,prototxt,version):
        net = caffe.Net(prototxt, caffemodel, caffe.TEST)
        if version == "v5":
            self.scene23_modify_v5(net)
        elif version == "v2":
            self.scene23_modify_v2(net)

        # self.scene23_modify_v2(net)
        # self.scene23_modify_v4(net,caffe.Net(prototxt, caffemodel, caffe.TEST))
        # # 先载入共享的model
        # output_net = None
        # if self.dp_json.has_key("init_model"):
        #     init_weights = str(self.dp_json["init_model"]["weights"])
        #     assert os.path.exists(init_weights)
        #     init_prototxt = str(self.dp_json["init_model"]["prototxt"])
        #     output_net = caffe.Net(init_prototxt, init_weights, caffe.TEST)
        # # 再载入每个子model
        # if self.dp_json.has_key("sub_models"):
        #     for sub_model in self.dp_json["sub_models"]:
        #         sub_weights = str(sub_model["weights"])
        #         assert os.path.exists(init_weights)
        #         sub_prototxt = str(sub_model["prototxt"])
        #         sub_net = caffe.Net(sub_prototxt, sub_weights, caffe.TEST)
        #         if output_net!=None:
        #             ModelsMerge.transplant(output_net, sub_net, prefix=sub_model["prefix"], suffix='')
        #         else:
        #             output_net = sub_net
        # # 将合并后的model保存
        # if self.dp_json.has_key("output_path"):
        #     output_net.save(str(self.dp_json["output_path"]))

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print "python models_modify.py caffemodel prototxt version"
        print "# example of mm_json_file : ../../rule/greendam_v7_2_4.mm.json"
        exit()
    mm_json_file = sys.argv[1]
    caffemodel = sys.argv[1]
    prototxt = sys.argv[2]
    version = sys.argv[3]
    modelsModify = ModelsModify()
    modelsModify.read_dp_json(mm_json_file)
    import caffe
    modelsModify.process(str(caffemodel),prototxt,version)

