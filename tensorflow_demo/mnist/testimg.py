import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
from PIL import Image
"""
全连接的前向传播神经网络
"""
INPUT_NODE = 784
OUTPUT_NODE = 10

LAYER1_NODE = 500


BATCH_SIZE = 100

LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99

REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99

#定义一个前传全连接神经网络
def inference(input_tensor , avg_class , weights1 , biases1 , weights2 , biases2):
    if avg_class is None:
        layer1 = tf.nn.relu(tf.matmul(input_tensor,weights1)+ biases1)

        return tf.matmul(layer1,weights2) + biases2

    else:
        layer1 = tf.nn.relu(tf.matmul(input_tensor,avg_class.average(weights1)) + avg_class.average(biases1))

        return tf.matmul(layer1,avg_class.average(weights2))+avg_class.average(biases2)


def train():
    x = tf.placeholder(tf.float32 , [None,INPUT_NODE],name='x-input')
    y_ = tf.placeholder(tf.float32,[None,OUTPUT_NODE],name='y-input')

    weights1 = tf.Variable(tf.truncated_normal([INPUT_NODE,LAYER1_NODE],stddev=0.1))
    biases1 = tf.Variable(tf.constant(0.1,shape=[LAYER1_NODE]))

    weights2 = tf.Variable(tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
    biases2 = tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]))

    #获取神经网络
    y = inference(x , None , weights1 ,biases1 , weights2 , biases2)

    global_step = tf.Variable(0 , trainable=False)


    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY , global_step)



    variable_averages_op = variable_averages.apply(tf.trainable_variables())

    # 获取神经网络
    average_y = inference(x , variable_averages ,weights1 , biases1 , weights2 , biases2)


    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_,1))

    cross_entropy_mean = tf.reduce_mean(cross_entropy)


    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)

    regularization = regularizer(weights1) + regularizer(weights2)


    loss = cross_entropy_mean + regularization

    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE , global_step ,55000 / BATCH_SIZE,LEARNING_RATE_DECAY)


    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss,global_step=global_step)

    with tf.control_dependencies([train_step,variable_averages_op]):
        train_op = tf.no_op(name='train')

    conrrect_prediction = tf.equal(tf.argmax(average_y,1),tf.argmax(y_,1))

    accuracy = tf.reduce_mean(tf.cast(conrrect_prediction,tf.float32), name="accuracy")


    img = Image.open('E:/01.jpg')


    # 变成灰度图，转换成矩阵
    im_arr = np.array(img.convert("L"))

    # 将图像矩阵拉成1行784列，并将值变成浮点型（像素要求的仕0-1的浮点型输入）
    nm_arr = im_arr.reshape([1, 784])
    nm_arr = nm_arr.astype(np.float32)
    img_ready = np.multiply(nm_arr, 1.0 / 255.0)

    preValue = tf.argmax(average_y, 1)#返回最大数值的下标

    saver = tf.train.Saver()

    with tf.Session() as sess:
        tf.global_variables_initializer().run()

        saver.restore(sess, "../Model/mnistModel4.ckpt")  # 这里使用了之前保存的模型参数

        preValue = sess.run(preValue, feed_dict={x: img_ready})

        print(preValue)



def main(argv=None):

    train()


if __name__ == '__main__':
    tf.app.run()





