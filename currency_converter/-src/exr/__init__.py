"""
The `exr` module contains an useful and up-to-date
`exchange_rate` method that allows to convert all 
the currencies that can be accessed by the 
EBC's RESTful API, on which the whole module is based.

Click [here](https://data.ecb.europa.eu/help/api/data) 
for further information about the API.
"""

from .exchange import CURRENCIES
from .exchange import exchange_rate