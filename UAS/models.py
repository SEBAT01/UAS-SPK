import numpy as np
import pandas as pd
from spk_model import WeightedProduct

class Rumahmakan():

    def __init__(self) -> None:
        self.rumahmakan = pd.read_csv('data/rumahmakan.csv')
        self.rumahmakans = np.array(self.rumahmakan)

    @property
    def rumahmakan_data(self):
        data = []
        for rumahmakan in self.rumahmakans:
            data.append({'id': rumahmakan[0], 'nama': rumahmakan[1]})
        return data

    @property
    def rumahmakan_data_dict(self):
        data = {}
        for rumahmakan in self.rumahmakans:
            data[rumahmakan[0]] = rumahmakan[1] 
        return data

    def get_recs(self, kriteria:dict):
        wp = WeightedProduct(self.rumahmakan.to_dict(orient="records"), kriteria)
        return wp.calculate