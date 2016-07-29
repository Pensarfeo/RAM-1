import tensorflow as tf
import tf_mnist_loader
import matplotlib.pyplot as plt
import numpy as np
import time
<<<<<<< HEAD
import math
=======
>>>>>>> QihongL-master
import random
import sys
try:
    xrange
except NameError:
    xrange = range

dataset = tf_mnist_loader.read_data_sets("mnist_data")
save_dir = "save-3scales/"
save_prefix = "save"
start_step = 0
#load_path = None
load_path = save_dir + save_prefix + str(start_step) + ".ckpt"
# to enable visualization, set draw to True
eval_only = False
animate = 0
draw = 0

# model parameters
minRadius = 4               # zooms -> minRadius * 2**<depth_level>
sensorBandwidth = 8         # fixed resolution of sensor
depth = 3                 # number of zooms
channels = 1                # mnist are grayscale images
totalSensorBandwidth = depth * channels * (sensorBandwidth **2)
<<<<<<< HEAD

# number of units
hg_size = 128               # input
hl_size = 128               # location
=======
nGlimpses = 5               # number of glimpses
loc_sd = 0.11               # std when setting the location

# network units
hg_size = 128               #
hl_size = 128               #
>>>>>>> QihongL-master
g_size = 256                #
cell_size = 256             #
cell_out_size = cell_size   #

<<<<<<< HEAD
nGlimpses = 5                # number of glimpses
n_classes = 10              # cardinality(Y)

batch_size = 20
max_iters = 1000000

mnist_size = 28             # side length of the picture

loc_sd = 0.11                # std when setting the location
mean_locs = []              #
baselines = []              #
sampled_locs = []           # ~N(mean_locs[.], loc_sd)
glimpse_images = []         # to show in window


SMALL_NUM = 1e-9
# lr = 1e-3
# minLr = 1e-5
# saturateEpoch = 50000
=======
# paramters about the training examples
n_classes = 10              # card(Y)
mnist_size = 28             # side length of the picture

# training parameters
max_iters = 1000000
batch_size = 20
SMALL_NUM = 1e-9

initLr = 3e-3
lrDecayRate = .99
lrDecayFreq = 100
momentumValue = .9


# resource prellocation
mean_locs = []              # expectation of locations
sampled_locs = []           # sampled locations ~N(mean_locs[.], loc_sd)
baselines = []              # baseline, the value prediction
glimpse_images = []         # to show in window


>>>>>>> QihongL-master

# set the weights to be small random values, with truncated normal distribution
def weight_variable(shape, myname, train):
    initial = tf.random_uniform(shape, minval=-0.1, maxval = 0.1)
    return tf.Variable(initial, name=myname, trainable=train)

# get local glimpses
def glimpseSensor(img, normLoc):
    loc = tf.round(((normLoc + 1) / 2) * mnist_size)  # normLoc coordinates are between -1 and 1
    loc = tf.cast(loc, tf.int32)

    img = tf.reshape(img, (batch_size, mnist_size, mnist_size, channels))

<<<<<<< HEAD
    zooms = []

    # process each image individually
=======
    # process each image individually
    zooms = []
>>>>>>> QihongL-master
    for k in xrange(batch_size):
        imgZooms = []
        one_img = img[k,:,:,:]
        max_radius = minRadius * (2 ** (depth - 1))
        offset = 2 * max_radius

        # pad image with zeros
        one_img = tf.image.pad_to_bounding_box(one_img, offset, offset, \
<<<<<<< HEAD
            max_radius * 4 + mnist_size, max_radius * 4 + mnist_size)
=======
                                               max_radius * 4 + mnist_size, max_radius * 4 + mnist_size)
>>>>>>> QihongL-master

        for i in xrange(depth):
            r = int(minRadius * (2 ** (i)))

            d_raw = 2 * r
            d = tf.constant(d_raw, shape=[1])
<<<<<<< HEAD

            d = tf.tile(d, [2])

            loc_k = loc[k,:]
            adjusted_loc = offset + loc_k - r


            one_img2 = tf.reshape(one_img, (one_img.get_shape()[0].value,\
                one_img.get_shape()[1].value))
=======
            d = tf.tile(d, [2])
            loc_k = loc[k,:]
            adjusted_loc = offset + loc_k - r
            one_img2 = tf.reshape(one_img, (one_img.get_shape()[0].value, one_img.get_shape()[1].value))
>>>>>>> QihongL-master

            # crop image to (d x d)
            zoom = tf.slice(one_img2, adjusted_loc, d)

            # resize cropped image to (sensorBandwidth x sensorBandwidth)
            zoom = tf.image.resize_bilinear(tf.reshape(zoom, (1, d_raw, d_raw, 1)), (sensorBandwidth, sensorBandwidth))
            zoom = tf.reshape(zoom, (sensorBandwidth, sensorBandwidth))
            imgZooms.append(zoom)

        zooms.append(tf.pack(imgZooms))

    zooms = tf.pack(zooms)

    glimpse_images.append(zooms)

    return zooms

# implements the input network
def get_glimpse(loc):
    # get input using the previous location
    glimpse_input = glimpseSensor(inputs_placeholder, loc)
    glimpse_input = tf.reshape(glimpse_input, (batch_size, totalSensorBandwidth))

    # the hidden units that process location & the input
<<<<<<< HEAD
    hg = tf.nn.relu(tf.matmul(glimpse_input, glimpse_hg) + bias_1)
    hl = tf.nn.relu(tf.matmul(loc, l_hl) + bias_2)

    # the hidden units that integrates the location & the glimpses
    g = tf.nn.relu(tf.matmul(hg, hg_g) + tf.matmul(hl, hl_g) + bias_3)
    g2 = tf.matmul(g, intrag) + bias_4
    return g2


# def get_next_input(output, i):
#     # the next location is computed by the location network
#     baseline = tf.sigmoid(tf.matmul(output,b_weights) + bias_5)
#     baselines.append(baseline)
#
#     mean_loc = tf.tanh(tf.matmul(output, h_l_out) + bias_6)
#     mean_locs.append(mean_loc)
#
#     sample_loc = tf.tanh(mean_loc + tf.random_normal(mean_loc.get_shape(), 0, loc_sd))
#     sampled_locs.append(sample_loc)
#
#     return get_glimpse(sample_loc)
=======
    act_glimpse_hidden = tf.nn.relu(tf.matmul(glimpse_input, Wg_g_h) + Bg_g_h)
    act_loc_hidden = tf.nn.relu(tf.matmul(loc, Wg_l_h) + Bg_l_h)

    # the hidden units that integrates the location & the glimpses
    glimpseFeature1 = tf.nn.relu(tf.matmul(act_glimpse_hidden, Wg_hg_gf1) + tf.matmul(act_loc_hidden, Wg_hl_gf1) + Bg_hlhg_gf1)
    # return g
    glimpseFeature2 = tf.matmul(glimpseFeature1, Wg_gf1_gf2) + Bg_gf1_gf2
    return glimpseFeature2
>>>>>>> QihongL-master


def get_next_input(output):
    # the next location is computed by the location network
<<<<<<< HEAD
    baseline = tf.sigmoid(tf.matmul(output,b_weights) + bias_5)
    baselines.append(baseline)

    mean_loc = tf.tanh(tf.matmul(output, h_l_out) + bias_6)
    mean_locs.append(mean_loc)

=======
    baseline = tf.sigmoid(tf.matmul(output,Wb_h_b) + Bb_h_b)
    baselines.append(baseline)
    # compute the next location, then impose noise
    mean_loc = tf.tanh(tf.matmul(output, Wl_h_l) + Bl_h_l)
    mean_locs.append(mean_loc)
>>>>>>> QihongL-master
    sample_loc = tf.tanh(mean_loc + tf.random_normal(mean_loc.get_shape(), 0, loc_sd))
    sampled_locs.append(sample_loc)

    return get_glimpse(sample_loc)



def affineTransform(x,output_dim):
    """
    affine transformation Wx+b
    assumes x.shape = (batch_size, num_features)
    """
    w=tf.get_variable("w", [x.get_shape()[1], output_dim])
    b=tf.get_variable("b", [output_dim], initializer=tf.constant_initializer(0.0))
    return tf.matmul(x,w)+b

<<<<<<< HEAD
# def model():
#     # initialize the location under unif[-1,1], for all example in the batch
#     initial_loc = tf.random_uniform((batch_size, 2), minval=-1, maxval=1)
#     # get the glimpse using the glimpse network
#     initial_glimpse = get_glimpse(initial_loc)
#
#     rnn_cell = tf.nn.rnn_cell.BasicRNNCell(cell_size)
#     initial_state = rnn_cell.zero_state(batch_size, tf.float32)
#
#     inputs = [initial_glimpse]
#     inputs.extend([0] * (nGlimpses - 1))
#
#     get_next_input(initial_glimpse,0)
#     outputs, _ = tf.nn.seq2seq.rnn_decoder(inputs, initial_state, rnn_cell, loop_function=get_next_input)
#
#     return outputs

=======
>>>>>>> QihongL-master
def model():
    # initialize the location under unif[-1,1], for all example in the batch
    initial_loc = tf.random_uniform((batch_size, 2), minval=-1, maxval=1)
    mean_locs.append(initial_loc)
    initial_loc = tf.tanh(initial_loc + tf.random_normal(initial_loc.get_shape(), 0, loc_sd))
    sampled_locs.append(initial_loc)

    # get the input using the input network
    initial_glimpse = get_glimpse(initial_loc)

<<<<<<< HEAD

=======
>>>>>>> QihongL-master
    # set up the recurrent structure
    inputs = [0] * nGlimpses
    outputs = [0] * nGlimpses
    glimpse = initial_glimpse
    REUSE = None
    for t in range(nGlimpses):
<<<<<<< HEAD

        # forward prop
        with tf.variable_scope("coreNetwork", reuse=REUSE):
            hiddenState = affineTransform(glimpse, cell_size)

        inputs[t] = glimpse
        outputs[t] = hiddenState
        # get the next input input
        if t != nGlimpses -1:
            glimpse = get_next_input(hiddenState)
        else:
            baseline = tf.sigmoid(tf.matmul(hiddenState, b_weights) + bias_5)
            baselines.append(baseline)

=======
        if t == 0:  # initialize the hidden state to be the zero vector
            hiddenState_prev = tf.zeros((batch_size, cell_size))
        else:
            hiddenState_prev = outputs[t-1]

        # forward prop
        with tf.variable_scope("coreNetwork", reuse=REUSE):
            # the next hidden state is a function of the previous hidden state and the current glimpse
            hiddenState = tf.nn.relu(affineTransform(hiddenState_prev, cell_size) + (tf.matmul(glimpse, Wc_g_h) + Bc_g_h))
        # save the current glimpse and the hidden state
        inputs[t] = glimpse
        outputs[t] = hiddenState
        # get the next input glimpse
        if t != nGlimpses -1:
            glimpse = get_next_input(hiddenState)
        else:
            baseline = tf.sigmoid(tf.matmul(hiddenState, Wb_h_b) + Bb_h_b)
            baselines.append(baseline)
>>>>>>> QihongL-master
        REUSE = True  # share variables for later recurrence

    return outputs


def dense_to_one_hot(labels_dense, num_classes=10):
<<<<<<< HEAD
  """Convert class labels from scalars to one-hot vectors."""
  # copied from TensorFlow tutorial
  num_labels = labels_dense.shape[0]
  index_offset = np.arange(num_labels) * n_classes
  labels_one_hot = np.zeros((num_labels, num_classes))
  labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
  return labels_one_hot
=======
    """Convert class labels from scalars to one-hot vectors."""
    # copied from TensorFlow tutorial
    num_labels = labels_dense.shape[0]
    index_offset = np.arange(num_labels) * n_classes
    labels_one_hot = np.zeros((num_labels, num_classes))
    labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
    return labels_one_hot
>>>>>>> QihongL-master


# to use for maximum likelihood with input location
def gaussian_pdf(mean, sample):
<<<<<<< HEAD
    Z = 1.0 / (loc_sd * tf.sqrt(2.0 * math.pi))
=======
    Z = 1.0 / (loc_sd * tf.sqrt(2.0 * np.pi))
>>>>>>> QihongL-master
    a = -tf.square(sample - mean) / (2.0 * tf.square(loc_sd))
    return Z * tf.exp(a)


def calc_reward(outputs):

<<<<<<< HEAD

    outputs_tensor = tf.convert_to_tensor(outputs)
    outputs_tensor = tf.transpose(outputs_tensor, perm=[1, 0, 2])
    b = tf.pack(baselines)
    b = tf.concat(2, [b, b])
    b = tf.reshape(b, (batch_size, (nGlimpses) * 2))

    # consider the action at the last time step
    outputs = outputs[-1] # look at ONLY THE END of the sequence
    outputs = tf.reshape(outputs, (batch_size, cell_out_size))

    # the hidden layer for the action network
    h_a_out = weight_variable((cell_out_size, n_classes), "h_a_out", True)
    # process its output
    p_y = tf.nn.softmax(tf.matmul(outputs, h_a_out) + bias_7)
    max_p_y = tf.arg_max(p_y, 1)
    # the targets
=======
    # consider the action at the last time step
    outputs = outputs[-1] # look at ONLY THE END of the sequence
    outputs = tf.reshape(outputs, (batch_size, cell_out_size))

    # get the baseline
    b = tf.pack(baselines)
    b = tf.concat(2, [b, b])
    b = tf.reshape(b, (batch_size, (nGlimpses) * 2))
    no_grad_b = tf.stop_gradient(b)

    # get the action(classification)
    p_y = tf.nn.softmax(tf.matmul(outputs, Wa_h_a) + Ba_h_a)
    max_p_y = tf.arg_max(p_y, 1)
>>>>>>> QihongL-master
    correct_y = tf.cast(labels_placeholder, tf.int64)

    # reward for all examples in the batch
    R = tf.cast(tf.equal(max_p_y, correct_y), tf.float32)
    reward = tf.reduce_mean(R) # mean reward
<<<<<<< HEAD
    #
=======
    R = tf.reshape(R, (batch_size, 1))
    R = tf.tile(R, [1, (nGlimpses)*2])

    # get the location
>>>>>>> QihongL-master
    p_loc = gaussian_pdf(mean_locs, sampled_locs)
    p_loc = tf.tanh(p_loc)
    p_loc_orig = p_loc
    p_loc = tf.reshape(p_loc, (batch_size, (nGlimpses) * 2))

<<<<<<< HEAD
    R = tf.reshape(R, (batch_size, 1))
    R = tf.tile(R, [1, (nGlimpses)*2])
    # 1 means concatenate along the row direction
    no_grad_b = tf.stop_gradient(b)


    J = tf.concat(1, [tf.log(p_y + SMALL_NUM) * (onehot_labels_placeholder), tf.log(p_loc + SMALL_NUM) * (R -  no_grad_b)])
    # sum the probability of action and location
    J = tf.reduce_sum(J, 1)
    J = J - tf.reduce_sum(tf.square(R - b), 1)
    # average over batch
    J = tf.reduce_mean(J, 0)
    cost = -J

    # Adaptive Moment Estimation
    # estimate the 1st and the 2nd moment of the gradients

    optimizer = tf.train.MomentumOptimizer(lr, .9)
    train_op = optimizer.minimize(cost, global_step)

    return cost, reward, max_p_y, correct_y, train_op, b, tf.reduce_mean(b), tf.reduce_mean(R - b), \
           p_loc_orig, p_loc, lr
=======
    # define the cost function
    J = tf.concat(1, [tf.log(p_y + SMALL_NUM) * (onehot_labels_placeholder), tf.log(p_loc + SMALL_NUM) * (R - no_grad_b)])
    J = tf.reduce_sum(J, 1)
    J = J - tf.reduce_sum(tf.square(R - b), 1)
    J = tf.reduce_mean(J, 0)
    cost = -J

    # define the optimizer
    optimizer = tf.train.MomentumOptimizer(lr, momentumValue)
    train_op = optimizer.minimize(cost, global_step)

    return cost, reward, max_p_y, correct_y, train_op, b, tf.reduce_mean(b), tf.reduce_mean(R - b), p_loc_orig, p_loc, lr
>>>>>>> QihongL-master


def evaluate():
    data = dataset.test
    batches_in_epoch = len(data._images) // batch_size
    accuracy = 0

    for i in xrange(batches_in_epoch):
        nextX, nextY = dataset.test.next_batch(batch_size)
        # nextX = convertTranslated(nextX)
        feed_dict = {inputs_placeholder: nextX, labels_placeholder: nextY,
                     onehot_labels_placeholder: dense_to_one_hot(nextY)}
        r = sess.run(reward, feed_dict=feed_dict)
        accuracy += r

    accuracy /= batches_in_epoch
<<<<<<< HEAD

    print("ACCURACY: " + str(accuracy))

=======
    print("ACCURACY: " + str(accuracy))


>>>>>>> QihongL-master
def convertTranslated(images):
    newimages = []
    for k in xrange(batch_size):
        image = images[k, :]
        image = np.reshape(image, (28, 28))
        randX = random.randint(0, 32)
        randY = random.randint(0, 32)
        image = np.lib.pad(image, ((randX, 32 - randX), (randY, 32 - randY)), 'constant', constant_values = (0))
        image = np.reshape(image, (60*60))
        newimages.append(image)
    return newimages



def toMnistCoordinates(coordinate_tanh):
    '''
    Transform coordinate in [-1,1] to mnist
    :param coordinate_tanh: vector in [-1,1] x [-1,1]
    :return: vector in the corresponding mnist coordinate
    '''
    return np.round(((coordinate_tanh + 1) / 2.0) * mnist_size)


<<<<<<< HEAD
with tf.Graph().as_default():

    global_step = tf.Variable(0, trainable=False)
    lr = tf.train.exponential_decay(3e-3, global_step, 100, .99, staircase=True)

    # the y vector
    labels = tf.placeholder("float32", shape=[batch_size, n_classes])
    # the input x and yhat
    inputs_placeholder = tf.placeholder(tf.float32, shape=(batch_size, mnist_size * mnist_size), name="images")
    labels_placeholder = tf.placeholder(tf.float32, shape=(batch_size), name="labels")
    onehot_labels_placeholder = tf.placeholder(tf.float32, shape=(batch_size, 10), name="oneHotLabels")
    b_placeholder = tf.placeholder(tf.float32, shape=(batch_size, (nGlimpses)*2), name="b")


    l_hl = weight_variable((2, hl_size), "l_hl", True)
    glimpse_hg = weight_variable((totalSensorBandwidth, hg_size), "glimpse_hg", True)


    #
    loc_mean = weight_variable((batch_size, nGlimpses, 2), "loc_mean", True)
    intrag = weight_variable((g_size, g_size), "intrag", True)
    hg_g = weight_variable((hg_size, g_size), "hg_g", True)
    hl_g = weight_variable((hl_size, g_size), "hl_g", True)
    h_l_out = weight_variable((cell_out_size, 2), "h_l_out", True)
    b_weights = weight_variable((g_size, 1), "b_weights", True)
    # b_weights1 = weight_variable((g_size, 56), "b_weights1", True)
    # b_weights2 = weight_variable((56, 1), "b_weights2", True)

    bias_1 = weight_variable((hg_size,), "bias_1", True)
    bias_2 = weight_variable((hl_size,),  "bias_2", True)
    bias_3 = weight_variable((g_size,),  "bias_3", True)
    bias_4 = weight_variable((g_size,),  "bias_4", True)
    bias_5 = weight_variable((1,), "bias_5", True)
    # bias_51 = weight_variable((56,),  "bias_51", True)
    # bias_52 = weight_variable((1,),  "bias_52", True)
    bias_6 = weight_variable((2,),  "bias_6", True)
    bias_7 = weight_variable((10,),  "bias_7", True)
=======
def variable_summaries(var, name):
    """Attach a lot of summaries to a Tensor."""
    with tf.name_scope('param_summaries'):
        mean = tf.reduce_mean(var)
        tf.scalar_summary('param_mean/' + name, mean)
        with tf.name_scope('param_stddev'):
            stddev = tf.sqrt(tf.reduce_sum(tf.square(var - mean)))
        tf.scalar_summary('param_sttdev/' + name, stddev)
        tf.scalar_summary('param_max/' + name, tf.reduce_max(var))
        tf.scalar_summary('param_min/' + name, tf.reduce_min(var))
        tf.histogram_summary(name, var)


with tf.Graph().as_default():

    # set the learning rate
    global_step = tf.Variable(0, trainable=False)
    lr = tf.train.exponential_decay(initLr, global_step, lrDecayFreq, lrDecayRate, staircase=True)

    # preallocate x, y, baseline
    labels = tf.placeholder("float32", shape=[batch_size, n_classes])
    labels_placeholder = tf.placeholder(tf.float32, shape=(batch_size), name="labels_raw")
    onehot_labels_placeholder = tf.placeholder(tf.float32, shape=(batch_size, 10), name="labels_onehot")
    inputs_placeholder = tf.placeholder(tf.float32, shape=(batch_size, mnist_size * mnist_size), name="images")
    b_placeholder = tf.placeholder(tf.float32, shape=(batch_size, (nGlimpses)*2), name="baseline")

    # declare the model parameters, here're naming rule:
    # the 1st captical letter: weights or bias (W = weights, B = bias)
    # the 2nd lowercase letter: the network (e.g.: g = glimpse network)
    # the 3rd and 4th letter(s): input-output mapping, which is clearly written in the variable name argument

    Wg_l_h = weight_variable((2, hl_size), "glimpseNet_wts_location_hidden", True)
    Bg_l_h = weight_variable((hl_size,), "glimpseNet_bias_location_hidden", True)

    Wg_g_h = weight_variable((totalSensorBandwidth, hg_size), "glimpseNet_wts_glimpse_hidden", True)
    Bg_g_h = weight_variable((hg_size,), "glimpseNet_bias_glimpse_hidden", True)
    
    Wg_hg_gf1 = weight_variable((hg_size, g_size), "glimpseNet_wts_hiddenGlimpse_glimpseFeature1", True)
    Wg_hl_gf1 = weight_variable((hl_size, g_size), "glimpseNet_wts_hiddenLocation_glimpseFeature1", True)
    Bg_hlhg_gf1 = weight_variable((g_size,), "glimpseNet_bias_hGlimpse_hLocs_glimpseFeature1", True)
    
    Wg_gf1_gf2 = weight_variable((g_size, g_size), "glimpseNet_wts_glimpseFeature1_glimpsedFeature2", True)
    Bg_gf1_gf2 = weight_variable((g_size,), "glimpseNet_bias_hidden_glimpsedFeature2", True)

    Wc_g_h = weight_variable((cell_size, g_size), "coreNet_wts_glimpse_hidden", True)
    Bc_g_h = weight_variable((g_size,), "coreNet_bias_glimpse_hidden", True)

    Wb_h_b = weight_variable((g_size, 1), "baselineNet_wts_hiddenState_baseline", True)
    Bb_h_b = weight_variable((1,), "baselineNet_bias_hiddenState_baseline", True)

    Wl_h_l = weight_variable((cell_out_size, 2), "locationNet_wts_hidden_location", True)
    Bl_h_l = weight_variable((2,),  "locationNet_bias_hidden_location", True)

    Wa_h_a = weight_variable((cell_out_size, n_classes), "actionNet_wts_hidden_action", True)
    Ba_h_a = weight_variable((n_classes,),  "actionNet_bias_hidden_action", True)
>>>>>>> QihongL-master

    # query the model ouput
    outputs = model()

    # convert list of tensors to one big tensor
    sampled_locs = tf.concat(0, sampled_locs)
    sampled_locs = tf.reshape(sampled_locs, (nGlimpses, batch_size, 2))
    sampled_locs = tf.transpose(sampled_locs, [1, 0, 2])
    mean_locs = tf.concat(0, mean_locs)
    mean_locs = tf.reshape(mean_locs, (nGlimpses, batch_size, 2))
    mean_locs = tf.transpose(mean_locs, [1, 0, 2])
    glimpse_images = tf.concat(0, glimpse_images)

<<<<<<< HEAD
    #
    cost, reward, predicted_labels, correct_labels, train_op, b, avg_b, rminusb, p_loc_orig, p_loc, lr = calc_reward(outputs)

=======
    # compute the reward
    cost, reward, predicted_labels, correct_labels, train_op, b, avg_b, rminusb, p_loc_orig, p_loc, lr = calc_reward(outputs)

    # tensorboard visualization for the parameters
    variable_summaries(Wg_l_h, "glimpseNet_wts_location_hidden")
    variable_summaries(Bg_l_h, "glimpseNet_bias_location_hidden")
    variable_summaries(Wg_g_h, "glimpseNet_wts_glimpse_hidden")
    variable_summaries(Bg_g_h, "glimpseNet_bias_glimpse_hidden")
    variable_summaries(Wg_hg_gf1, "glimpseNet_wts_hiddenGlimpse_glimpseFeature1")
    variable_summaries(Wg_hl_gf1, "glimpseNet_wts_hiddenLocation_glimpseFeature1")
    variable_summaries(Bg_hlhg_gf1, "glimpseNet_bias_hGlimpse_hLocs_glimpseFeature1")
    variable_summaries(Wg_gf1_gf2, "glimpseNet_wts_glimpseFeature1_glimpsedFeature2")
    variable_summaries(Bg_gf1_gf2, "glimpseNet_bias_glimpseFeature1_glimpsedFeature2")

    variable_summaries(Wc_g_h, "coreNet_wts_glimpse_hidden")
    variable_summaries(Bc_g_h, "coreNet_bias_glimpse_hidden")

    variable_summaries(Wb_h_b, "baselineNet_wts_hiddenState_baseline")
    variable_summaries(Bb_h_b, "baselineNet_bias_hiddenState_baseline")

    variable_summaries(Wl_h_l, "locationNet_wts_hidden_location")
    variable_summaries(Bl_h_l, "locationNet_bias_hidden_location")

    variable_summaries(Wa_h_a, 'actionNet_wts_hidden_action')
    variable_summaries(Ba_h_a, 'actionNet_bias_hidden_action')

    # tensorboard visualization for the performance metrics
>>>>>>> QihongL-master
    tf.scalar_summary("reward", reward)
    tf.scalar_summary("cost", cost)
    tf.scalar_summary("mean(b)", avg_b)
    tf.scalar_summary(" mean(R - b)", rminusb)
    summary_op = tf.merge_all_summaries()

<<<<<<< HEAD
=======

    ####################################### START RUNNING THE MODEL #######################################
>>>>>>> QihongL-master
    sess = tf.Session()
    saver = tf.train.Saver()
    b_fetched = np.zeros((batch_size, (nGlimpses)*2))

    init = tf.initialize_all_variables()
    sess.run(init)

    if eval_only:
        evaluate()
    else:
        summary_writer = tf.train.SummaryWriter("summary", graph=sess.graph)

        if draw:
            fig = plt.figure()
            txt = fig.suptitle("-", fontsize=36, fontweight='bold')
            plt.ion()
            plt.show()
            plt.subplots_adjust(top=0.7)
            plotImgs = []

        # training
        for step in xrange(start_step + 1, max_iters):
            start_time = time.time()

            # get the next batch of examples
            nextX, nextY = dataset.train.next_batch(batch_size)
            # nextX = convertTranslated(nextX)
            feed_dict = {inputs_placeholder: nextX, labels_placeholder: nextY, \
                         onehot_labels_placeholder: dense_to_one_hot(nextY), b_placeholder: b_fetched}
            fetches = [train_op, cost, reward, predicted_labels, correct_labels, glimpse_images, b, avg_b, rminusb, \
<<<<<<< HEAD
                       p_loc_orig, p_loc, mean_locs, sampled_locs, h_l_out, outputs[-1], lr]
=======
                       p_loc_orig, p_loc, mean_locs, sampled_locs, outputs[-1], lr]
>>>>>>> QihongL-master
            # feed them to the model
            results = sess.run(fetches, feed_dict=feed_dict)

            _, cost_fetched, reward_fetched, prediction_labels_fetched, correct_labels_fetched, f_glimpse_images_fetched, \
            b_fetched, avg_b_fetched, rminusb_fetched, p_loc_orig_fetched, p_loc_fetched, mean_locs_fetched, sampled_locs_fetched, \
<<<<<<< HEAD
            h_l_out_fetched, output_fetched, lr_fetched = results

            duration = time.time() - start_time

            # print np.shape(mean_locs_fetched[0,:,0])
            # print mean_locs_fetched[0, :, :]
            # sys.exit('STOP')
=======
            output_fetched, lr_fetched = results

            duration = time.time() - start_time

>>>>>>> QihongL-master

            if step % 20 == 0:
                if step % 1000 == 0:
                    # saver.save(sess, save_dir + save_prefix + str(step) + ".ckpt")
                    if step % 5000 == 0:
                        evaluate()

<<<<<<< HEAD

                ##### DRAW WINDOW ################
                # print tf.shape(f_glimpse_images_fetched)
                # print f_glimpse_images_fetched.shape
                # sys.exit('STOP')
                f_glimpse_images = np.reshape(f_glimpse_images_fetched, (nGlimpses, batch_size, depth, sensorBandwidth, sensorBandwidth)) #steps, THEN batch
=======
                ##### DRAW WINDOW ################
                f_glimpse_images = np.reshape(f_glimpse_images_fetched, \
                                              (nGlimpses, batch_size, depth, sensorBandwidth, sensorBandwidth))
>>>>>>> QihongL-master

                if draw:
                    if animate:
                        fillList = False
                        if len(plotImgs) == 0:
                            fillList = True

                        # display the first image in the in mini-batch
                        # display the entire image
                        nCols = depth+1
                        whole = plt.subplot2grid((depth, nCols), (0, 1), rowspan=depth, colspan=depth)
                        whole = plt.imshow(np.reshape(nextX[0, :], [mnist_size, mnist_size]),
                                           cmap=plt.get_cmap('gray'), interpolation="nearest")
                        whole.autoscale()
<<<<<<< HEAD
                        # transform the coordinate to mnist map
                        # sampled_locs_mnist_fetched = np.round(((sampled_locs_fetched + 1) / 2.0) * mnist_size)
                        sampled_locs_mnist_fetched = toMnistCoordinates(sampled_locs_fetched)
                        # visualize the trace of successive nGlimpses (note that x and y coordinates are "flipped")
                        plt.plot(sampled_locs_mnist_fetched[0, 0:-1, 1], sampled_locs_mnist_fetched[0, 0:-1, 0], '-o',
                                 color='lawngreen')
                        plt.plot(sampled_locs_mnist_fetched[0, -2, 1], sampled_locs_mnist_fetched[0, -2, 0], 'o',
                             color='red')
=======

                        # transform the coordinate to mnist map
                        sampled_locs_mnist_fetched = toMnistCoordinates(sampled_locs_fetched)
                        # visualize the trace of successive nGlimpses (note that x and y coordinates are "flipped")
                        plt.plot(sampled_locs_mnist_fetched[0, :, 1], sampled_locs_mnist_fetched[0, :, 0], '-o',
                                 color='lawngreen')
                        plt.plot(sampled_locs_mnist_fetched[0, -1, 1], sampled_locs_mnist_fetched[0, -1, 0], 'o',
                                 color='red')
>>>>>>> QihongL-master
                        fig.canvas.draw()

                        # display the glimpses
                        for y in xrange(nGlimpses):
                            txt.set_text('FINAL PREDICTION: %i\nTRUTH: %i\nSTEP: %i/%i'
                                         % (prediction_labels_fetched[0], correct_labels_fetched[0], (y + 1), nGlimpses))

                            for x in xrange(depth):
                                plt.subplot(depth, nCols, 1 + nCols * x)
                                if fillList:
                                    plotImg = plt.imshow(f_glimpse_images[y, 0, x], cmap=plt.get_cmap('gray'),
                                                         interpolation="nearest")
                                    plotImg.autoscale()
                                    plotImgs.append(plotImg)
                                else:
                                    plotImgs[x].set_data(f_glimpse_images[y, 0, x])
                                    plotImgs[x].autoscale()
                            fillList = False

                            fig.canvas.draw()
                            time.sleep(0.1)
                            plt.pause(0.0001)
                    else:
                        txt.set_text('PREDICTION: %i\nTRUTH: %i' % (prediction_labels_fetched[0], correct_labels_fetched[0]))
                        for x in xrange(depth):
                            for y in xrange(nGlimpses):
                                plt.subplot(depth, nGlimpses, x * nGlimpses + y + 1)
<<<<<<< HEAD
                                plt.imshow(f_glimpse_images[y, 0, x], cmap=plt.get_cmap('gray'),
                                           interpolation="nearest")
=======
                                plt.imshow(f_glimpse_images[y, 0, x], cmap=plt.get_cmap('gray'), interpolation="nearest")
>>>>>>> QihongL-master

                        plt.draw()
                        time.sleep(0.05)
                        plt.pause(0.0001)

                ################################

                print('Step %d: cost = %.5f reward = %.5f (%.3f sec) b = %.5f R-b = %.5f, LR = %.5f'
                      % (step, cost_fetched, reward_fetched, duration, avg_b_fetched, rminusb_fetched, lr_fetched))

<<<<<<< HEAD
                '''
                print('real b: ' )
                print(b_fetched)
                print('p_loc orig: ')
                print(p_loc_orig_fetched)
                print('p_loc: ')
                print(p_loc_fetched)
                '''
                summary_str = sess.run(summary_op, feed_dict=feed_dict)
                summary_writer.add_summary(summary_str, step)

sess.close()
=======
                summary_str = sess.run(summary_op, feed_dict=feed_dict)
                summary_writer.add_summary(summary_str, step)

    sess.close()
>>>>>>> QihongL-master