import math
import os
import random
from abc import ABC, abstractmethod

import numpy as np
import tensorflow as tf
from filelock import Timeout, FileLock
from tensorflow import Graph

from arpreprocessing.dataset import Dataset
from multimodal_classfiers.cnn_lstm import ClassifierCnnLstm
from multimodal_classfiers.encoder import ClassifierEncoder
from multimodal_classfiers.fcn import ClassifierFcn
from multimodal_classfiers.hyperparameters import Hyperparameters
from multimodal_classfiers.inception_time import ClassifierInception
from multimodal_classfiers.mcdcnn import ClassifierMcdcnn
from multimodal_classfiers.mlp import ClassifierMlp
from multimodal_classfiers.mlp_lstm import ClassifierMlpLstm
from multimodal_classfiers.resnet import ClassifierResnet
from multimodal_classfiers.stresnet import ClassifierStresnet
from multimodal_classfiers.time_cnn import ClassifierTimeCnn
from utils.utils import get_new_session, prepare_data

CLASSIFIERS = ("mcdcnnM", "cnnM", "mlpM", "fcnM", "encoderM", "resnetM", "inceptionM", "stresnetM", "mlpLstmM",
               "cnnLstmM")


class NoSuchClassifier(Exception):
    def __init__(self, classifier_name):
        self.message = "No such classifier: {}".format(classifier_name)


def create_classifier(classifier_name, input_shapes, nb_classes, output_directory, verbose=False,
                      sampling_rates=None, ndft_arr=None, hyperparameters=None, model_init=None):
    if classifier_name == 'fcnM':
        return ClassifierFcn(output_directory, input_shapes, nb_classes, verbose, hyperparameters,
                             model_init=model_init)
    if classifier_name == 'mlpM':
        return ClassifierMlp(output_directory, input_shapes, nb_classes, verbose, hyperparameters,
                             model_init=model_init)
    if classifier_name == 'resnetM':
        return ClassifierResnet(output_directory, input_shapes, nb_classes, verbose, hyperparameters,
                                model_init=model_init)
    if classifier_name == 'encoderM':
        return ClassifierEncoder(output_directory, input_shapes, nb_classes, verbose, hyperparameters,
                                 model_init=model_init)
    if classifier_name == 'mcdcnnM':
        return ClassifierMcdcnn(output_directory, input_shapes, nb_classes, verbose, hyperparameters,
                                model_init=model_init)
    if classifier_name == 'cnnM':
        return ClassifierTimeCnn(output_directory, input_shapes, nb_classes, verbose, hyperparameters,
                                 model_init=model_init)
    if classifier_name == 'inceptionM':
        depth = hyperparameters.depth if hyperparameters and hyperparameters.depth else 6
        return ClassifierInception(output_directory, input_shapes, nb_classes, depth=depth, verbose=verbose,
                                   hyperparameters=hyperparameters, model_init=model_init)
    if classifier_name == 'stresnetM':
        return ClassifierStresnet(output_directory, input_shapes, sampling_rates,
                                  ndft_arr, nb_classes, verbose=verbose,
                                  hyperparameters=hyperparameters,
                                  model_init=model_init)
    if classifier_name == 'cnnLstmM':
        return ClassifierCnnLstm(output_directory, input_shapes, nb_classes, hyperparameters=hyperparameters,
                                 model_init=model_init)
    if classifier_name == 'mlpLstmM':
        return ClassifierMlpLstm(output_directory, input_shapes, nb_classes, verbose, hyperparameters,
                                 model_init=model_init)

    raise NoSuchClassifier(classifier_name)


class ExperimentalSetup():
    def __init__(self, name, x_train, y_train, x_val, y_val, x_test, y_test, input_shapes, sampling_val, ndft_arr,
                 nb_classes, nb_ecpochs_fn, batch_size_fn):
        self.name = name
        self.x_train = x_train
        self.y_train = y_train
        self.x_val = x_val
        self.y_val = y_val
        self.x_test = x_test
        self.y_test = y_test
        self.input_shapes = input_shapes
        self.sampling_val = sampling_val
        self.ndft_arr = ndft_arr
        self.nb_classes = nb_classes
        self.nb_epochs_fn = nb_ecpochs_fn
        self.batch_size_fn = batch_size_fn


class Experiment(ABC):
    def __init__(self, dataset_name: str, logger, no_channels, dataset_name_suffix=""):
        self._tuning_iteration = 0
        self.dataset_name = dataset_name
        self.logger_obj = logger
        self.experimental_setups = None
        self.no_channels = no_channels
        self.experiment_path = f"results/{self.dataset_name}{dataset_name_suffix}"

        self.prepare_experimental_setups()

    @abstractmethod
    def prepare_experimental_setups(self):
        pass

    def perform(self, iterations, classifiers=CLASSIFIERS):
        for iteration in range(iterations):
            for classifier_name in classifiers:
                self.perform_on_one_classifier(classifier_name, iteration)

    def perform_on_one_classifier(self, classifier_name, iteration, hyperparameters=None, gpu=0):
        with Graph().as_default():
            session = get_new_session()
            with session.as_default():
                with tf.device(f'/device:GPU:{gpu}'):
                    model_init = None

                    for setup in self.experimental_setups:
                        output_directory = f"{self.experiment_path}/{iteration}/{classifier_name}/{setup.name}/"
                        os.makedirs(output_directory, exist_ok=True)

                        try:
                            session.run(tf.global_variables_initializer())
                            model_init = self.perform_single_experiment(classifier_name, output_directory, setup,
                                                                        iteration, hyperparameters, model_init)
                        except Timeout:
                            self.logger_obj.info("Experiment is being performed by another process")

    def perform_single_experiment(self, classifier_name: str, output_directory: str, setup: ExperimentalSetup,
                                  iteration, hyperparameters: Hyperparameters, model_init):
        logging_message = "Experiment for {} dataset, classifier: {}, setup: {}, iteration: {}".format(
            self.dataset_name, classifier_name, setup.name, iteration)
        self.logger_obj.info(logging_message)

        with FileLock(output_directory + "DOING.lock", timeout=0):
            done_dict_path = output_directory + "DONE"
            if os.path.exists(done_dict_path):
                self.logger_obj.info("Experiment already performed")
                return

            classifier = create_classifier(classifier_name, setup.input_shapes, setup.nb_classes,
                                           output_directory,
                                           verbose=False,
                                           sampling_rates=setup.sampling_val, ndft_arr=setup.ndft_arr,
                                           hyperparameters=hyperparameters, model_init=model_init)
            self.logger_obj.info(
                f"Created model for {self.dataset_name} dataset, classifier: {classifier_name}, setup: {setup.name}, iteration: {iteration}")
            classifier.fit(setup.x_train, setup.y_train, setup.x_val, setup.y_val, setup.y_test,
                           x_test=setup.x_test, nb_epochs=setup.nb_epochs_fn(classifier_name),
                           batch_size=setup.batch_size_fn(classifier_name))
            self.logger_obj.info(
                f"Fitted model for {self.dataset_name} dataset, classifier: {classifier_name}, setup: {setup.name}, iteration: {iteration}")

            os.makedirs(done_dict_path)
            #self._clean_up_files(output_directory)
            self.logger_obj.info("Finished e" + logging_message[1:])

            return classifier.model

    @staticmethod
    def _clean_up_files(output_directory):
        best_model_path = output_directory + "best_model.hdf5"
        if os.path.exists(best_model_path):
            os.remove(best_model_path)


def get_experimental_setup(logger_obj, channels_ids, test_ids, train_ids, val_ids, name, dataset_name):
    path = "archives/mts_archive/"
    dataset = Dataset(dataset_name, None, logger_obj)
    x_test, y_test, sampling_test = dataset.load(path, test_ids, channels_ids)
    x_val, y_val, sampling_val = dataset.load(path, val_ids, channels_ids)
    x_train, y_train, sampling_train = dataset.load(path, train_ids, channels_ids)
    x_train = [np.expand_dims(np.array(x), 2) for x in x_train]
    x_val = [np.expand_dims(np.array(x), 2) for x in x_val]
    x_test = [np.expand_dims(np.array(x), 2) for x in x_test]
    input_shapes, nb_classes, y_val, y_train, y_test, y_true = prepare_data(x_train, y_train, y_val, y_test)
    ndft_arr = [get_ndft(x) for x in sampling_test]

    if len(input_shapes) != len(ndft_arr):
        raise Exception("Different sizes of input_shapes and ndft_arr")

    for i in range(len(input_shapes)):
        if input_shapes[i][0] < ndft_arr[i]:
            raise Exception(
                f"Too big ndft, i: {i}, ndft_arr[i]: {ndft_arr[i]}, input_shapes[i][0]: {input_shapes[i][0]}")
    experimental_setup = ExperimentalSetup(name, x_train, y_train, x_val, y_val, x_test, y_test, input_shapes,
                                           sampling_val, ndft_arr, nb_classes, lambda x: 150, get_batch_size)
    return experimental_setup


def get_ndft(sampling):
    if sampling <= 2:
        return 8
    if sampling <= 4:
        return 16
    if sampling <= 8:
        return 32
    if sampling <= 16:
        return 64
    if sampling <= 32:
        return 128
    if sampling in [70, 64]:
        return 256
    raise Exception(f"No such sampling as {sampling}")


def get_batch_size(classifier_name):
    if classifier_name == "inceptionM":
        return 2
    if classifier_name == "resnetM":
        return 4
    if classifier_name == "encoderM":
        return 2
    if classifier_name == "mlpLstmM":
        return 16
    if classifier_name == "fcnM":
        return 4
    return 32


def n_fold_split(subject_ids, n, seed=5):
    result = []

    random.seed(seed)
    subject_ids = list(subject_ids)
    random.shuffle(subject_ids)

    test_sets = [subject_ids[i::n] for i in range(n)]

    for test_set in test_sets:
        rest = [x for x in subject_ids if x not in test_set]
        val_set = random.sample(rest, math.ceil(len(rest) / 5))
        train_set = [x for x in rest if x not in val_set]
        result.append({"train": train_set, "val": val_set, "test": test_set})

    random.seed()
    return result


def prepare_experimental_setups_n_iterations(self_experiment: Experiment, train_ids, val_ids, test_ids, iterations=5):
    self_experiment.experimental_setups = []

    for i in range(iterations):
        self_experiment.experimental_setups.append(
            get_experimental_setup(self_experiment.logger_obj, tuple(range(self_experiment.no_channels)),
                                   test_ids, train_ids, val_ids, f"it_{i:02d}", self_experiment.dataset_name))
