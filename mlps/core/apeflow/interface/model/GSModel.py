# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : Manki.Baek@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from datetime import datetime
import json
import os

from mlps.core.apeflow.interface.model.ModelAbstract import ModelAbstract
from mlps.core.apeflow.api.algorithms.gs.GSAlgAbstract import GSAlgAbstract
from mlps.core.RestManager import RestManager


class GSModel(ModelAbstract):
    def __init__(self, param_dict, ext_data=None):
        ModelAbstract.__init__(self, param_dict, ext_data)
        self.model: GSAlgAbstract = self._build()

    def learn(self, dataset):
        start_time = datetime.now()
        self.model.learn(dataset)
        learn_time_sec = (datetime.now() - start_time).total_seconds()
        self.model.learn_result(len(dataset['x']), learn_time_sec)

        self.model.saved_model()
