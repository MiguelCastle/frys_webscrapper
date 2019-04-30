class product(object):
    def __init__(self, name, plu, model, price, specs_list, short_descr, model_id, feats_list):
        self.name = name
        self.plu = plu
        self.model = model
        self.price = price
        self.specs = specs_list
        self.descr = short_descr
        self.id = model_id
        self.feats = feats_list
