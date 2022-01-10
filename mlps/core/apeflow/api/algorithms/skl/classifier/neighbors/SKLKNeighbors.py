# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import log_loss

from mlps.common.Constants import Constants
from mlps.common.exceptions.ParameterError import ParameterError
from mlps.core.apeflow.api.algorithms.skl.SKLAlgAbstract import SKLAlgAbstract


class SKLKNeighbors(SKLAlgAbstract):
    # MODEL INFORMATION
    ALG_CODE = "SKLKNeighbors"
    ALG_TYPE = ["Classifier"]
    DATA_TYPE = ["Single"]
    VERSION = "1.0.0"
    DIST_TYPE = Constants.DIST_TYPE_SINGLE
    OUT_MODEL_TYPE = Constants.OUT_MODEL_PKL

    def __init__(self, param_dict, ext_data):
        super(SKLKNeighbors, self).__init__(param_dict, ext_data)

    def _check_parameter(self, param_dict):
        _param_dict = super(SKLKNeighbors, self)._check_parameter(param_dict)
        # Parameter Setting
        try:
            _param_dict["n_neighbors"] = int(param_dict["n_neighbors"])

        except:
            raise ParameterError
        return _param_dict

    def _build(self):
        n_neighbors = self.param_dict["n_neighbors"]
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)

    def learn(self, dataset):
        y = self._arg_max(dataset["y"])
        self.model.fit(dataset["x"], y)
        self.learn_result(dataset)

    def learn_result_classifier(self, dataset):
        results = dict()
        results["global_sn"] = self.param_dict["global_sn"]
        y = self._arg_max(dataset["y"])
        results["accuracy"] = self.model.score(X=dataset["x"], y=y)
        pred = self.predict(dataset["x"])
        loss = log_loss(y, pred)
        results["loss"] = loss
        results["step"] = self.learn_params.get("global_step", 1)

        result_list = list()
        result_list.append(results)

        return result_list


if __name__ == '__main__':
    __dataset = {
        "x": np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]]),
        # "y" : np.array([1, 1, 0, 0]),
        "y": np.array([[0, 1], [0, 1], [1, 0], [1, 0]]),
    }

    __param_dict = {
        "algorithm_code": "SKLKNeighbors",
        "algorithm_type": "Classifier",
        "data_type": "Single",
        "method_type": "Basic",
        "input_units": (2,),
        "output_units": "2",
        "global_step": "1000",
        "model_nm": "SKLKNeighbors__1",
        "alg_sn": "0",
        "job_type": "learn",
        "depth": "0",
        "global_sn": "0",

        "early_type": "0",
        "job_key": "125445555",
        "params": {"n_neighbors": "2"}
    }

    GSSG = SKLKNeighbors(__param_dict, None)
    GSSG._build()

    GSSG.learn(dataset=__dataset)
    GSSG.learn_result(__dataset)
    print(GSSG.predict(np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])))
    GSSG.saved_model()

    temp = SKLKNeighbors(__param_dict, None)
    temp.load_model()

    eval_data = {"x": np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]]),
                 "y": np.array([[0, 1], [0, 1], [1, 0], [1, 0]]), }
    print(GSSG.eval(dataset=eval_data))

