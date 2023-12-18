from settings import MEREK_SCALE,DEV_SCALE_brand,DEV_SCALE_porsi,DEV_SCALE_ukuran,DEV_SCALE_sambel,DEV_SCALE_hadiah,DEV_SCALE_harga

class BaseMethod():

    def __init__(self, data_dict, **setWeight):

        self.dataDict = data_dict

        # 1-7 (Kriteria)
        self.raw_weight = {
            'brand': 5, 
            'nama': 3, 
            'porsi': 4, 
            'ukuran': 3, 
            'sambel': 4, 
            'hadiah': 5, 
            'harga': 1,
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        return [{
            'id': rumahmakan['id'],
            'nama': MEREK_SCALE[rumahmakan['nama']],
            'brand': DEV_SCALE_brand[rumahmakan['brand']],
            'porsi': DEV_SCALE_porsi[rumahmakan['porsi']],
            'ukuran': DEV_SCALE_ukuran[rumahmakan['ukuran']],
            'sambel': DEV_SCALE_sambel[rumahmakan['sambel']],
            'hadiah': DEV_SCALE_hadiah[rumahmakan['hadiah']],
            'harga': DEV_SCALE_harga[rumahmakan['harga']]
        } for rumahmakan in self.dataDict]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        brand = [] # max
        nama = [] # max
        porsi = [] # max
        ukuran = [] # max
        sambel = [] # max
        hadiah = [] # max
        harga = [] # min
        for data in self.data:
            brand.append(data['brand'])
            nama.append(data['nama'])
            porsi.append(data['porsi'])
            ukuran.append(data['ukuran'])
            sambel.append(data['sambel'])
            hadiah.append(data['hadiah'])
            harga.append(data['harga'])

        max_brand = max(brand)
        max_nama = max(nama)
        max_porsi = max(porsi)
        max_ukuran = max(ukuran)
        max_sambel = max(sambel)
        max_hadiah = max(hadiah)
        min_harga = min(harga)

        return [
            {   'id': data['id'],
                'brand': data['brand']/max_brand, # benefit
                'nama': data['nama']/max_nama, # benefit
                'porsi': data['porsi']/max_porsi, # benefit
                'ukuran': data['ukuran']/max_ukuran, # benefit
                'sambel': data['sambel']/max_sambel, # benefit
                'hadiah': data['hadiah']/max_hadiah, # benefit
                'harga': min_harga/data['harga'] # cost
                }
            for data in self.data
        ]
 

class WeightedProduct(BaseMethod):
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
    round(
        row['brand'] ** weight['brand'] *
        row['nama'] ** weight['nama'] *
        row['porsi'] ** weight['porsi'] *
        row['ukuran'] ** weight['ukuran'] *
        row['sambel'] ** weight['sambel'] *
        row['hadiah'] ** (-weight['hadiah']) *
        row['harga'] ** weight['harga']
        , 2
    )
    for row in self.normalized_data}

        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))