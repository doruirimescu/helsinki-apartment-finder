'''
    Parameters used for your apartment search.
    vastike is hoitovastike
    price is velaton
'''
__all__ = ["price_range", "area_range", "year_range", "vastike_range", "floor_range", "rooms_range",
           "zone_range", "zone_weights", "number_of_apartments_to_plot", "number_of_apartments_to_rank"]
K = 1000

price_range     = (100*K, 400*K)
area_range      = (50, 150)
year_range      = (1950, 2022)
vastike_range   = (10, 450)
floor_range     = (0, 10)
rooms_range     = (1, 5)
zone_range      = (0, 1)

# Assign your weights from 0 to 1 (check zone_range) for the zones that you value the most
zone_weights = {"matinkylä": 1, "leppävaara": 1, "tiistilä": 1, "olari": 0.5}

number_of_apartments_to_plot = 5
number_of_apartments_to_rank = 10
