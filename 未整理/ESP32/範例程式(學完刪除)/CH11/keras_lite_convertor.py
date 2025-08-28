"""Keras lite convertor
"""

import os
import json
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

__version__ = '1.0.2'


class Data_reader():
    """
    Args:
        path_name: A string,
            dataset path, which may represent a folder path or a file path.
        mode: A string,
            model mode, one of 'regression', 'binary', 'categorical'.
        label_name: A list of string,
            list of class names (must match names of subdirectories).
            Used to control the order of the classes
            (otherwise alphanumerical order is used).
    """
    def __init__(self, path_name: str, mode='categorical', label_name=None):
        self.path_name = path_name
        self.mode = mode
        if mode in ('regression', 'binary', 'categorical'):
            if label_name is None and mode != 'regression':
                self.label_name = [
                    f[:(f.rfind('.'))]for f in os.listdir(path_name)
                    if not f.startswith('.')]
                self.label_name.sort()
                if len(self.label_name) > 2 and mode == 'binary':
                    raise ValueError(
                        'Found more than two files, '
                        'please assign parameter `label_name`.')
            else:
                self.label_name = label_name
        else:
            raise ValueError(f'Invalid mode: {mode}')

    def read(self, maxlen=None,
             shuffle=True, random_seed=None,
             encoding='utf-8'):
        """
        Args:
            maxlen: An integer or None,
                maximum length of data.
            shuffle: A boolean,
                whether to shuffle data.
            random_seed: An integer,
                random seed for shuffling data.
            encoding: A string.
        """
        train_data = []
        label_data = []

        if self.mode == 'regression':
            with open(self.path_name,
                      encoding=encoding, errors='ignore') as file:
                for line in file:
                    try:
                        data = line.split(' ')
                        train_value = list(map(float,data[0].split(',')))
                        label_value = list(map(float,data[1].split(',')))
                        train_data.append(train_value)
                        label_data.append(label_value)
                    except Exception as ecp:
                        print(ecp)

            label_data = np.array(label_data)

        else:
            file_list = [
                f for f in os.listdir(self.path_name)
                if not f.startswith('.')]

            for name in file_list:
                with open(
                    os.path.join(self.path_name, name),
                    encoding=encoding, errors='ignore') as file:
                    label = self.label_name.index(name[:(name.rfind('.'))])
                    for line in file:
                        try:
                            data = list(map(float, line.split(',')))
                            train_data.append(data)
                            label_data.append(label)
                        except Exception as ecp:
                            print(ecp)

            if self.mode == 'categorical':
                label_data = to_categorical(label_data)
            elif self.mode == 'binary':
                label_data = np.array(label_data)

        if maxlen is None:
            train_data = np.array(train_data)
        else:
            train_data = pad_sequences(
                train_data, maxlen=maxlen,
                truncating='post').astype('float')

        if shuffle:
            np.random.seed(random_seed)
            shuffle_index = np.arange(len(train_data))
            np.random.shuffle(shuffle_index)
            train_data = train_data[shuffle_index]
            label_data = label_data[shuffle_index]

        return train_data, label_data

sup_activation = ('linear', 'relu', 'sigmoid', 'softmax')


def save(model, path):
    """Save tf.Keras model as keras_lite model.

    Args:
        model: A tf.Keras model.
        path: A string, keras_lite model output path.
    """
    arch = json.loads(model.to_json())
    model_dict = {}
    has_input_layer = False
    arch_class_name = arch['class_name']
    if arch_class_name == 'Sequential':
        layers = []
        o_layers = arch['config']['layers']
        for i_layer, o_layer in enumerate(o_layers):
            layer = {}
            if i_layer == 0:
                layer['batch_input_shape'] = (
                    o_layer['config']['batch_input_shape'])
            o_layer_class_name = o_layer['class_name']

            if o_layer_class_name == 'InputLayer':
                has_input_layer = True
                layer['class_name'] = 'InputLayer'

            elif o_layer_class_name == 'Dense':
                layer['class_name'] = 'Dense'
                layer['units'] = o_layer['config']['units']
                acti_func = o_layer['config']['activation']
                if acti_func in sup_activation:
                    layer['activation'] = acti_func
                else:
                    raise ValueError(f'Invalid activation: {acti_func}')

                weights = [0, 0]
                layer_weights = (
                    model.layers[i_layer - has_input_layer].get_weights())
                weights[0] = layer_weights[0].tolist()
                if len(layer_weights) > 1:
                    weights[1] = layer_weights[1].tolist()

                layer['weights'] = weights

            elif o_layer_class_name == 'Reshape':
                layer['class_name'] = 'Reshape'
                layer['target_shape'] = o_layer['config']['target_shape']

            elif o_layer_class_name == 'Conv1D':
                layer['class_name'] = 'Conv1D'
                layer['strides'] = o_layer['config']['strides'][0]
                layer['kernel_size'] = o_layer['config']['kernel_size'][0]
                layer['padding'] = o_layer['config']['padding']
                acti_func = o_layer['config']['activation']
                if acti_func in sup_activation[:3]:
                    layer['activation'] = acti_func
                else:
                    raise ValueError(f'Invalid activation: {acti_func}')

                weights = [0, 0]
                layer_weights = (
                    model.layers[i_layer - has_input_layer].get_weights())
                weights[0] = layer_weights[0].reshape(
                    (-1, layer_weights[0].shape[-1])).tolist()
                if len(layer_weights) > 1:
                    weights[1] = layer_weights[1].tolist()
                layer['weights'] = weights

            elif o_layer_class_name == 'MaxPooling1D':
                layer['class_name'] = 'MaxPooling1D'
                layer['pool_size'] = o_layer['config']['pool_size'][0]
                layer['strides'] = o_layer['config']['strides'][0]

            elif o_layer_class_name == 'AveragePooling1D':
                layer['class_name'] = 'AveragePooling1D'
                layer['pool_size'] = o_layer['config']['pool_size'][0]
                layer['strides'] = o_layer['config']['strides'][0]

            elif o_layer_class_name == 'GlobalMaxPooling1D':
                layer['class_name'] = 'GlobalMaxPooling1D'

            elif o_layer_class_name == 'GlobalAveragePooling1D':
                layer['class_name'] = 'GlobalAveragePooling1D'

            elif o_layer_class_name == 'Flatten':
                layer['class_name'] = 'Flatten'

            else:
                raise ValueError(f'Invalid layer: {o_layer_class_name}')

            layers.append(layer)

        model_dict['layers'] = layers

        with open(path, mode='w', encoding="utf-8") as file:
            file.write(json.dumps(model_dict))
    else:
        raise ValueError(
            f'Unable to save non-sequential model: {arch_class_name}')
