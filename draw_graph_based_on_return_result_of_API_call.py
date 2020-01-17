import matplotlib.pyplot as plt
import cv2
import numpy as np
import json

def process_api_return_value(str):

    class Stack(object):
        def __init__(self):
            self.stack = []

        def isEmpty(self):
            return self.stack == []

        def push(self, item):
            self.stack.append(item)

        def pop(self):
            if self.isEmpty():
                print('pop from empty stack')
                return
            return self.stack.pop()

        def peek(self):
            return self.stack[-1]

        def size(self):
            return len(self.stack)

    my_list = []
    stack = Stack()
    begin = 0

    for index, value in enumerate(str):
        if value == '{':
            if stack.isEmpty():
                begin = index
            stack.push(value)

        if value == '}':
            stack.pop()
            if stack.isEmpty():
                end = index
                my_list.append(str[begin:end + 1])

    boxes_list = []
    classes = []

    for value in my_list:
        boxes_list_each = []
        dic = json.loads(value)

        classes.append(dic['label'])

        coordinate_value = dic['points']

        for i in coordinate_value:
            boxes_list_each.append(i['x'])
            boxes_list_each.append(i['y'])
        boxes_list_each.append(dic['score'])

        boxes_list.append(boxes_list_each)

    boxes = np.array(boxes_list)

    return boxes, classes


def process_api_return_value_new(str):

    class Stack(object):
        def __init__(self):
            self.stack = []

        def isEmpty(self):
            return self.stack == []

        def push(self, item):
            self.stack.append(item)

        def pop(self):
            if self.isEmpty():
                print('pop from empty stack')
                return
            return self.stack.pop()

        def peek(self):
            return self.stack[-1]

        def size(self):
            return len(self.stack)

    my_list = []
    stack = Stack()
    begin = 0

    for index, value in enumerate(str):
        if value == '{':
            if stack.isEmpty():
                begin = index
            stack.push(value)

        if value == '}':
            stack.pop()
            if stack.isEmpty():
                end = index
                my_list.append(str[begin:end + 1])

    boxes_list = []
    classes = []

    for value in my_list:
        boxes_list_each = []
        dic = json.loads(value)

        classes.append(dic['label'])

        x1 = dic['X1']
        y1 = dic['Y1']
        x2 = dic['X2']
        y2 = dic['Y2']

        boxes_list_each.append(x1)
        boxes_list_each.append(y1)
        boxes_list_each.append(x2)
        boxes_list_each.append(y2)


        boxes_list_each.append(dic['score'])

        boxes_list.append(boxes_list_each)

    boxes = np.array(boxes_list)

    return boxes, classes

def get_class_string(class_name, score):
    return class_name + ' {:0.2f}'.format(score).lstrip('0')

def vis_one_image(
        im, class_names,
            boxes, classes,
                thresh=0.9, dpi=100,
                    box_alpha=0.0, show_class=True,
                        filename=None, ext='png'):
    if boxes is None \
        or boxes.shape[0] == 0 or \
            max(boxes[:, 4]) < thresh: return

    im = im[:, :, ::-1]

    fig = plt.figure(frameon=False)
    fig.set_size_inches(im.shape[1] / dpi, im.shape[0] / dpi)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.axis('off')
    fig.add_axes(ax)
    ax.imshow(im)

    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    sorted_inds = np.argsort(-areas)

    for i in sorted_inds:
        bbox = boxes[i, :4]
        score = boxes[i, -1]
        if score < thresh:
            continue

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1],
                          fill=False, edgecolor='g',
                          linewidth=1.0, alpha=box_alpha))

        if show_class:
            ax.text(
                bbox[0], bbox[1] - 2,
                get_class_string(class_names[classes[i]], score),
                fontsize=11,
                family='serif',
                bbox=dict(
                    facecolor='g', alpha=0.4, pad=0, edgecolor='none'),
                color='white')


    if filename is not None:
        fig.savefig(filename + '.' + ext, dpi=dpi)
        plt.close('all')
    else:
        plt.imshow(im)
        plt.show()

if __name__ == '__main__':
    # class_names = ['__background__',
    #            'wangzai_milk', 'carabao', 'letian_pear', 'yiyun', 'asamu_milk_tea',
    #            'ice_black_tea', 'green_tea', 'guolicheng',
    #            'lemon_diet_coke', 'paris_air_lemonade', 'coca_cola']
    class_names = ['__background__',  # always index 0
                    'bai_sui_shan','cestbon','cocacola','jing_tian','pepsi_cola','sprite', 'starbucks_black_tea','starbucks_matcha',
                   'starbucks_mocha', 'vita_lemon_tea', 'vita_soymilk_blue', 'wanglaoji_green']
    raw_image = cv2.imread("/home/zs/Downloads/825814315.jpg")
    api_return_value = '{"X1":183.16705,"X2":219.20607,"Y1":90.92888,"Y2":156.74188,"isValid":true,"label":12,"rotate":0.0,"scale":1.0,"score":0.91529673},{"X1":107.992,"X2":134.56369,"Y1":109.58552,"Y2":172.43378,"isValid":true,"label":12,"rotate":0.0,"scale":1.0,"score":0.8530557},{"X1":215.84003,"X2":247.98904,"Y1":91.2408,"Y2":158.44923,"isValid":true,"label":12,"rotate":0.0,"scale":1.0,"score":0.76213115},{"X1":147.57758,"X2":177.94997,"Y1":88.658325,"Y2":159.71234,"isValid":true,"label":11,"rotate":0.0,"scale":1.0,"score":0.6236997},{"X1":88.47448,"X2":113.25012,"Y1":110.82884,"Y2":175.39255,"isValid":true,"label":12,"rotate":0.0,"scale":1.0,"score":0.57547456},{"X1":297.39496,"X2":324.01883,"Y1":99.94556,"Y2":168.37982,"isValid":true,"label":12,"rotate":0.0,"scale":1.0,"score":0.32544965}'
    # api_return_value = '{ "score": 0.9997675, "label": 1, "points": [ { "x": 353, "y": 141 }, { "x": 399, "y": 185 } ] }, { "score": 0.9997595, "label": 1, "points": [ { "x": 345, "y": 467 }, { "x": 383, "y": 493 } ] }, { "label": 1, "points": [ { "x": 350, "y": 393 }, { "x": 395, "y": 432 } ], "score": 0.9997452 }, { "label": 1, "points": [ { "x": 469, "y": 395 }, { "x": 515, "y": 435 } ], "score": 0.9997329 }, { "label": 1, "points": [ { "x": 454, "y": 470 }, { "x": 496, "y": 495 } ], "score": 0.99970144 }, { "score": 0.9996629, "label": 4, "points": [ { "x": 265, "y": 171 }, { "x": 295, "y": 208 } ] }, { "score": 0.99965036, "label": 1, "points": [ { "x": 482, "y": 253 }, { "x": 533, "y": 308 } ] }, { "score": 0.9996132, "label": 1, "points": [ { "x": 584, "y": 153 }, { "x": 613, "y": 190 } ] }, { "label": 1, "points": [ { "x": 367, "y": 65 }, { "x": 407, "y": 88 } ], "score": 0.9995467 }, { "score": 0.99954516, "label": 1, "points": [ { "x": 251, "y": 374 }, { "x": 279, "y": 412 } ] }, { "score": 0.99953854, "label": 1, "points": [ { "x": 596, "y": 260 }, { "y": 303, "x": 626 } ] }, { "points": [ { "x": 656, "y": 272 }, { "x": 673, "y": 308 } ], "score": 0.99951994, "label": 2 }, { "score": 0.9995023, "label": 1, "points": [ { "x": 474, "y": 68 }, { "x": 512, "y": 91 } ] }, { "score": 0.999443, "label": 1, "points": [ { "y": 132, "x": 488 }, { "x": 532, "y": 173 } ] }, { "score": 0.99934644, "label": 1, "points": [ { "x": 587, "y": 371 }, { "x": 616, "y": 409 } ] }, { "score": 0.9993381, "label": 4, "points": [ { "x": 251, "y": 262 }, { "x": 278, "y": 302 } ] }, { "score": 0.9992448, "label": 1, "points": [ { "x": 330, "y": 262 }, { "y": 318, "x": 379 } ] }, { "score": 0.99916387, "label": 1, "points": [ { "x": 561, "y": 92 }, { "x": 591, "y": 121 } ] }, { "points": [ { "x": 266, "y": 447 }, { "x": 294, "y": 473 } ], "score": 0.9989454, "label": 1 }, { "score": 0.9987325, "label": 1, "points": [ { "x": 559, "y": 448 }, { "x": 591, "y": 476 } ] }, { "score": 0.9983511, "label": 4, "points": [ { "y": 266, "x": 200 }, { "x": 216, "y": 299 } ] }, { "label": 2, "points": [ { "x": 648, "y": 184 }, { "x": 666, "y": 217 } ], "score": 0.99830675 }, { "score": 0.9979704, "label": 2, "points": [ { "y": 123, "x": 623 }, { "x": 644, "y": 150 } ] }, { "score": 0.9977896, "label": 4, "points": [ { "x": 210, "y": 341 }, { "x": 228, "y": 372 } ] }, { "score": 0.9953903, "label": 2, "points": [ { "x": 624, "y": 421 }, { "x": 645, "y": 447 } ] }, { "score": 0.99503785, "label": 4, "points": [ { "x": 282, "y": 99 }, { "x": 307, "y": 124 } ] }, { "points": [ { "x": 650, "y": 351 }, { "x": 667, "y": 382 } ], "score": 0.99273527, "label": 2 }, { "score": 0.98872966, "label": 4, "points": [ { "x": 208, "y": 188 }, { "x": 225, "y": 219 } ] }, { "points": [ { "x": 226, "y": 129 }, { "x": 244, "y": 154 } ], "score": 0.9849327, "label": 4 }'

    boxes, classes = process_api_return_value_new(api_return_value)

    vis_one_image(raw_image, class_names, boxes, classes, thresh=0.0, box_alpha=1.0, show_class=True)

