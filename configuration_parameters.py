'''
    Parameters used to configure your apartment search.
    vastike is hoitovastike
    price is velaton
'''
__all__ = ["price_range", "area_range", "year_range", "vastike_range", "floor_range", "rooms_range",
           "zone_range", "zone_weights", "number_of_apartments_to_plot", "number_of_apartments_to_rank"]
K = 1000

# Ranges used for normalization
price_range     = (100*K, 400*K)
area_range      = (50, 150)
year_range      = (1950, 2022)
vastike_range   = (10, 450)
floor_range     = (0, 10)
rooms_range     = (1, 5)
zone_range      = (0, 1)

# Weights used for weighted sum
# Assign your weights from 0 to 1 (check zone_range) for the zones that you value the most
zone_weights = {"matinkylä": 1, "leppävaara": 1, "tiistilä": 1, "olari": 0.5}

price_weight = 1.0
area_weight  = 1.0
year_weight  = 1.0
vastike_weight = 1.0
floor_weight = 1.0
rooms_weight = 1.0

number_of_apartments_to_plot = 5
number_of_apartments_to_rank = 10

locations_url = '''&locations=%5B%5B814,4, \
%22Lepp%C3%A4vaara,%20Espoo%22%5D,%5B798,4, \
%22Matinkyl%C3%A4,%20Espoo%22%5D,%5B335047,4, \
%22Tiistil%C3%A4,%20Espoo%22%5D,%5B797,4, \
%22Olari,%20Espoo%22%5D,%5B815,4, \
%22Kilo,%20Espoo%22%5D,%5B5694675,4, \
%22Finnoo,%20Espoo%22%5D,%5B13736198,4, \
%22Vermonniitty,%20Espoo%22%5D,%5B13617407,3, \
%22Peril%C3%A4nniitty,%20Espoo%22%5D,%5B880,4, \
%22M%C3%A4kkyl%C3%A4,%20Espoo%22%5D%5D'''
