from numpy import int64
from sqlalchemy import column
from ..utils.utils import pd,np,tf, normalizer

word_bank = {'address': 0,'adult': 1,
            'amount': 2,
            'asses': 3,
            'assessed': 4,
            'assessor': 5,
            'average': 6,
            'base': 7,
            'begin': 8,
            'best': 9,
            'bottle': 10,
            'bottles': 11,
            'bracket': 12,
            'brand': 13,
            'budget': 14,
            'category': 15,
            'charge': 16,
            'city': 17,
            'class': 18,
            'classification': 19,
            'clientele': 20,
            'cluster': 21,
            'code': 22,
            'cost': 23,
            'count': 24,
            'county': 25,
            'credential': 26,
            'ct': 27,
            'customer': 28,
            'date': 29,
            'dcoilwtico': 30,
            'description': 31,
            'division': 32,
            'dollars': 33,
            'earnings': 34,
            'effective': 35,
            'end': 36,
            'ending': 37,
            'expense': 38,
            'expiration': 39,
            'expiry': 40,
            'family': 41,
            'fee': 42,
            'gallons': 43,
            'genre': 44,
            'group': 45,
            'housi': 46,
            'id': 47,
            'income': 48,
            'industry': 49,
            'inventory': 50,
            'invoice': 51,
            'item': 52,
            'kind': 53,
            'label': 54,
            'life': 55,
            'list': 56,
            'liters': 57,
            'locale': 58,
            'location': 59,
            'marijuana': 60,
            'marke': 61,
            'market': 62,
            'medical': 63,
            'merchandising': 64,
            'ml': 65,
            'month': 66,
            'name': 67,
            'nbr': 68,
            'new': 69,
            'non': 70,
            'number': 71,
            'objectid': 72,
            'onpromotion': 73,
            'opm': 74,
            'pack': 75,
            'parce': 76,
            'period': 77,
            'permit': 78,
            'pin': 79,
            'price': 80,
            'pricing': 81,
            'product': 82,
            'products': 83,
            'profit': 84,
            'property': 85,
            'rate': 86,
            'ratio': 87,
            'recorded': 88,
            'registration': 89,
            'remarks': 90,
            'residential': 91,
            'retail': 92,
            'revenue': 93,
            'row': 94,
            'sale': 95,
            'sales': 96,
            'section': 97,
            'sell': 98,
            'serial': 99,
            'shelf': 100,
            'shipper': 101,
            'size': 102,
            'sold': 103,
            'sort': 104,
            'state': 105,
            'status': 106,
            'store': 107,
            'supervisor': 108,
            'supplier': 109,
            'table': 110,
            'tariff': 111,
            'taxpayer': 112,
            'time': 113,
            'timestamp': 114,
            'total': 115,
            'town': 116,
            'transactions': 117,
            'transferred': 118,
            'transfers': 119,
            'turnover': 120,
            'type': 121,
            'unit': 122,
            'use': 123,
            'used': 124,
            'valid': 125,
            'value': 126,
            'variable': 127,
            'vendor': 128,
            'volume': 129,
            'warehouse': 130,
            'week': 131,
            'wholesale': 132,
            'wholesalers': 133,
            'year': 134,
            'zip': 135}

number_to_wordbank = {0: 'address',
 1: 'adult',
 2: 'amount',
 3: 'asses',
 4: 'assessed',
 5: 'assessor',
 6: 'average',
 7: 'base',
 8: 'begin',
 9: 'best',
 10: 'bottle',
 11: 'bottles',
 12: 'bracket',
 13: 'brand',
 14: 'budget',
 15: 'category',
 16: 'charge',
 17: 'city',
 18: 'class',
 19: 'classification',
 20: 'clientele',
 21: 'cluster',
 22: 'code',
 23: 'cost',
 24: 'count',
 25: 'county',
 26: 'credential',
 27: 'ct',
 28: 'customer',
 29: 'date',
 30: 'dcoilwtico',
 31: 'description',
 32: 'division',
 33: 'dollars',
 34: 'earnings',
 35: 'effective',
 36: 'end',
 37: 'ending',
 38: 'expense',
 39: 'expiration',
 40: 'expiry',
 41: 'family',
 42: 'fee',
 43: 'gallons',
 44: 'genre',
 45: 'group',
 46: 'housi',
 47: 'id',
 48: 'income',
 49: 'industry',
 50: 'inventory',
 51: 'invoice',
 52: 'item',
 53: 'kind',
 54: 'label',
 55: 'life',
 56: 'list',
 57: 'liters',
 58: 'locale',
 59: 'location',
 60: 'marijuana',
 61: 'marke',
 62: 'market',
 63: 'medical',
 64: 'merchandising',
 65: 'ml',
 66: 'month',
 67: 'name',
 68: 'nbr',
 69: 'new',
 70: 'non',
 71: 'number',
 72: 'objectid',
 73: 'onpromotion',
 74: 'opm',
 75: 'pack',
 76: 'parce',
 77: 'period',
 78: 'permit',
 79: 'pin',
 80: 'price',
 81: 'pricing',
 82: 'product',
 83: 'products',
 84: 'profit',
 85: 'property',
 86: 'rate',
 87: 'ratio',
 88: 'recorded',
 89: 'registration',
 90: 'remarks',
 91: 'residential',
 92: 'retail',
 93: 'revenue',
 94: 'row',
 95: 'sale',
 96: 'sales',
 97: 'section',
 98: 'sell',
 99: 'serial',
 100: 'shelf',
 101: 'shipper',
 102: 'size',
 103: 'sold',
 104: 'sort',
 105: 'state',
 106: 'status',
 107: 'store',
 108: 'supervisor',
 109: 'supplier',
 110: 'table',
 111: 'tariff',
 112: 'taxpayer',
 113: 'time',
 114: 'timestamp',
 115: 'total',
 116: 'town',
 117: 'transactions',
 118: 'transferred',
 119: 'transfers',
 120: 'turnover',
 121: 'type',
 122: 'unit',
 123: 'use',
 124: 'used',
 125: 'valid',
 126: 'value',
 127: 'variable',
 128: 'vendor',
 129: 'volume',
 130: 'warehouse',
 131: 'week',
 132: 'wholesale',
 133: 'wholesalers',
 134: 'year',
 135: 'zip'}

unitable_columns = ['', 'Expiration date', 'category', 'date', 'name', 'price', 'sales', 'sold']

# beta test
def auto_column_test_predict(columns):

    columns_removed_signs = remove_signs(columns)
    columns_splitted_space = [col.split(' ') for col in columns_removed_signs]
    print("split",columns_splitted_space)
    # [[address, number],[]]
    columns_encoded = []
    # print(columns)
    # making bunch of zeros and ones, with one hot encoder machine learning technique
    for column_name in columns_splitted_space:
        # [address, number]
        # 0,71
        number_token = []
        
        for word in column_name:
            if word in word_bank:
                number_token.append(word_bank[word.lower()]) # append a number from word bank
        columns_encoded.append({
            "column" : column_name,
            'value'  : [one_hot_encoded(number_token)]
        })

        # print(column_name,number_token)


    model_yeszero = tf.keras.models.load_model('../models/unitable-model/unitable-classifier-v2-yeszero.keras')
    # model_nozero = tf.keras.models.load_model('../models/unitable-model/unitable-classifier-v2-nozero.keras')
    
    result = []

    for encoded_column in columns_encoded:
        res = model_yeszero.predict(encoded_column['value'])
        decoded = one_hot_decoded(res[0])
        result.append({
            'actual_column_name' : encoded_column['column'],
            'actual_encoded' : encoded_column['value'][0],
            'predicted' : res[0].tolist(),
            'predicted_decoded' : decoded,
            'predicted_decoded_str' : unitable_columns[decoded],
        })
    print(result)
    return result

def remove_signs(columns):
    signs = "(),.-_%$*&#@!}{|\\/<>;:"
    new_columns = []
    for col in columns:
        word = col
        for sign in signs:
            word = word.replace(sign,' ').strip()
        new_columns.append(word)
    print(new_columns)
    return new_columns

def one_hot_decoded(result):
    return int(np.where(result == np.max(result))[0][0])


def one_hot_encoded(number_token):
    if len(number_token) <= 0:
        return [0 for i in range(len(word_bank))]
    return [1 if i in number_token else 0 for i in range(len(word_bank))]

# test
# remove_signs(['name_label(),.-_%$*&#@!}{|\\/<>;:'])
auto_column_test_predict(['name_label','product'])             
