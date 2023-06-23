import tensorflow as tf


class CustomModel(tf.keras.Model):
    def __init__(self, state_shape, num_sensors, ):
        super(CustomModel, self).__init__()
        self.reshape = tf.keras.layers.Reshape((state_shape, num_sensors), input_shape=(state_shape,))
        self.conv1_0 = tf.keras.layers.Conv1D(40, 200, activation=tf.nn.relu, input_shape=(state_shape, num_sensors))
        self.conv1_1 = tf.keras.layers.Conv1D(25, 10, activation=tf.nn.relu)
        self.max_pooling_0 = tf.keras.layers.MaxPooling1D(4)
        self.conv1_2 = tf.keras.layers.Conv1D(100, 10, activation=tf.nn.relu)
        self.conv1_3 = tf.keras.layers.Conv1D(50, 10, activation=tf.nn.relu)
        self.max_pooling_1 = tf.keras.layers.MaxPooling1D(4)
        self.dropout = tf.keras.layers.Dropout(0.5)
        self.conv1_4 = tf.keras.layers.Conv1D(100, 10, activation=tf.nn.relu)
        self.global_average_pooling = tf.keras.layers.GlobalAveragePooling1D()
        self.dense = tf.keras.layers.Dense(1,)

    def call(self, inputs, **kwargs):
        x = self.reshape(inputs[:, :-1])
        x = self.conv1_0(x)
        x = self.conv1_1(x)
        x = self.max_pooling_0(x)
        x = self.conv1_2(x)
        x = self.conv1_3(x)
        x = self.max_pooling_1(x)
        x = self.dropout(x)
        x = self.conv1_4(x)
        x = self.global_average_pooling(x)
        x = self.dense(x)
        action = inputs[:, -1:]
        return (action-0.5)*x
