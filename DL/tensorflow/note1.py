#coding:utf-8

import tensorflow as tf

try:
    hello = tf.constant('Hello, TensorFlow!')
    global ss
    ss = tf.Session()
    hi = ss.run(hello)
    print(hi.decode())

    a = tf.constant(10)
    b = tf.constant(32)
    ab = ss.run(a + b)
    print(ab)
finally:
    ss.close()
