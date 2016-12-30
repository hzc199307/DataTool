# coding=utf-8
# by hezhichao
# 2016.12.29

import os
import json
import sys

class ModelsMerge:

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
        self.dp_json = json.load(open(dp_json_file))
        caffe_root = self.dp_json["caffe_config"]["caffe_root"]  # this file should be run from {caffe_root}/examples (otherwise change this line)
        sys.path.insert(0, caffe_root + 'python')
        import caffe
        caffe.set_device(int(self.dp_json["caffe_config"]["device"]))
        if (self.dp_json["caffe_config"]["mode"] == "gpu") | (self.dp_json["caffe_config"]["mode"] == "GPU"):
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()

    def process(self):
        # 先载入共享的model
        output_net = None
        if self.dp_json.has_key("init_model"):
            init_weights = str(self.dp_json["init_model"]["weights"])
            assert os.path.exists(init_weights)
            init_prototxt = str(self.dp_json["init_model"]["prototxt"])
            output_net = caffe.Net(init_prototxt, init_weights, caffe.TEST)
        # 再载入每个子model
        if self.dp_json.has_key("sub_models"):
            for sub_model in self.dp_json["sub_models"]:
                sub_weights = str(sub_model["weights"])
                assert os.path.exists(init_weights)
                sub_prototxt = str(sub_model["prototxt"])
                sub_net = caffe.Net(sub_prototxt, sub_weights, caffe.TEST)
                if output_net!=None:
                    ModelsMerge.transplant(output_net, sub_net, prefix=sub_model["prefix"], suffix='')
                else:
                    output_net = sub_net
        # 将合并后的model保存
        if self.dp_json.has_key("output_path"):
            output_net.save(str(self.dp_json["output_path"]))

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print "python models_merge.py mm_json_file"
        print "# example of mm_json_file : ../rule/greendam_v7_2_4.mm.json"
        exit()
    mm_json_file = sys.argv[1]
    modelsMerge = ModelsMerge()
    modelsMerge.read_dp_json(mm_json_file)
    import caffe
    modelsMerge.process()

