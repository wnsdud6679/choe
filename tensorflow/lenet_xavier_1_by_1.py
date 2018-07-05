from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
import tensorflow as tf
sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
sess.run(tf.initialize_all_variables())
y = tf.nn.softmax(tf.matmul(x,W) + b)
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

#W_conv3 = weight_variable([1, 1, 1, 3])
W_conv3 = tf.get_variable("W_conv3", shape=[1, 1, 1, 3],
           initializer=tf.contrib.layers.xavier_initializer())
b_conv3 = bias_variable([3])
x_image = tf.reshape(x, [-1,28,28,1])

h_conv3 = conv2d(x_image, W_conv3) + b_conv3

#W_conv1 = weight_variable([5, 5, 3, 20])
W_conv1 = tf.get_variable("W_conv1", shape=[5, 5, 3, 20],
           initializer=tf.contrib.layers.xavier_initializer())
b_conv1 = bias_variable([20])

h_conv1= conv2d(h_conv3, W_conv1) + b_conv1

h_pool1 = max_pool_2x2(h_conv1)

#W_conv2 = weight_variable([5, 5, 20, 50])
W_conv2 = tf.get_variable("W_conv2", shape=[5, 5, 20, 50],
           initializer=tf.contrib.layers.xavier_initializer())
b_conv2 = bias_variable([50])

h_conv2 = conv2d(h_pool1, W_conv2) + b_conv2

h_pool2 = max_pool_2x2(h_conv2)

#W_fc1 = weight_variable([7 * 7 * 50, 500])
W_fc1 = tf.get_variable("W_fc1", shape=[7 * 7 * 50, 500],
           initializer=tf.contrib.layers.xavier_initializer())
b_fc1 = bias_variable([500])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*50])

h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

#W_fc2 = weight_variable([500, 10])
W_fc2 = tf.get_variable("W_fc2", shape=[500, 10],
           initializer=tf.contrib.layers.xavier_initializer())
b_fc2 = bias_variable([10])

y_conv=tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.initialize_all_variables())
for i in range(5000):
  batch = mnist.train.next_batch(64)
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={
        x:batch[0], y_: batch[1]})
    print("step %d, training accuracy %g"%(i, train_accuracy))
  train_step.run(feed_dict={x: batch[0], y_: batch[1]})

print("test accuracy %g"%accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels}))