import os
import tensorflow as tf
from PIL import Image
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from tensorflow.examples.tutorials.mnist import input_data

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
TRAINING_STEPS = 10000
MOVING_AVERAGE_DECAY = 0.99

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

    y = inference(x , None , weights1 ,biases1 , weights2 , biases2)

    global_step = tf.Variable(0 , trainable=False)


    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY , global_step)



    variable_averages_op = variable_averages.apply(tf.trainable_variables())


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

    accuracy = tf.reduce_mean(tf.cast(conrrect_prediction, tf.float32), name="accuracy")

    mnist = input_data.read_data_sets("../mnist_data", one_hot=True)


    saver = tf.train.Saver()

    filename_queue = tf.train.string_input_producer(["minist4.tfrecords"])  # create a queue

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)  # return file_name and file
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw': tf.FixedLenFeature([], tf.string),
                                       })  # return image and label

    img = tf.decode_raw(features['img_raw'], tf.uint8)
    print(img)
    # 转换图像格式
    img = tf.cast(img, tf.float32)
    img = tf.reshape(img, [784])
    print(img)

    label = tf.cast(features['label'], tf.int64)  #label是一个张量了 神经网络的输入是一维数组长度为10  这个怎么转换
    print(label)
    label = tf.one_hot(label, 10, 1, 0)
    print(label)


    xs, ys = tf.train.shuffle_batch([img, label],
                                    batch_size=BATCH_SIZE,
                                    num_threads=64,
                                    capacity=2000,
                                    min_after_dequeue=1500,
                                    )



    print(xs.shape)
    print(ys.shape)

    with tf.Session() as sess:
        tf.global_variables_initializer().run()

        validate_feed = {x: mnist.validation.images, y_: mnist.validation.labels}

        test_feed = {x: mnist.test.images, y_: mnist.test.labels}

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        xs, ys = sess.run([xs, ys])


        #迭代次数
        for i in range(TRAINING_STEPS):
            if i % 1000 == 0:
                validate_acc = sess.run(accuracy, feed_dict=validate_feed)
                print("After %d traing step(s),validation accuracy using average model is %g" % (i, validate_acc))

            #print(ys)
            sess.run(train_op,feed_dict={x:xs,y_:ys})

        saver.save(sess, "../Model/mnistModel4.ckpt")

        # 停止所有线程
        coord.request_stop()
        coord.join(threads)

        print("success")



def main(argv=None):

    train()


if __name__ == '__main__':
    tf.app.run()





