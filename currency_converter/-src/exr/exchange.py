import json
import os

from requests import get
from requests.exceptions import RequestException


with open('data/ISO4217', 'r', encoding='UTF-8') as iso4217:
    CURRENCIES = frozenset(line.split('\t')[1] for line in iso4217.readlines())


def retrieve_data(numerator: str, verbose: bool = True) -> float:
    """
    Retrieves exchange rates through the EBC's RESTful API.

    Parameters
    ----------
    numerator : str
        The currency indicated with 3 uppercase
        characters according to ISO 4217.
    verbose : bool
        If True, adds additional information. Default is True.

    Returns
    -------
    float
        The exchage rate numerator/EUR.

    Raises
    ------
    JSONDecodeError
        Whenever the API Request generates some
        invalid or not compatible file JSON.
    KeyError
        When trying to access to a non-existent item 
        in a dictionary decoded from the JSON file.
    IndexError
        When trying to access to a non-existent 
        position in a list decoded from the JSON file.
    RequestException
        A generic exception that indicates a failure caused by:
        - `TimeoutError`: probably due 
        to unstable internet connection
        - `HTTPerror`: poorly formulated headers
        by the API call or migrated domain
        - other unknown kinds of bad request.
    """
    
    numerator = numerator.upper()
    resp = get(
        f"https://data-api.ecb.europa.eu/service/data/EXR/"
        f"D.{numerator}.EUR.SP00.A?lastNObservations=1",
        headers={
            "Accept": "application/json",
        } 
    )

    if verbose: print(f"status: {resp.status_code}")

    if not os.path.exists("data"):
        os.makedirs("data")
    name = f"{numerator}divEUR"
    with open(f"data/.{name}.json", 'w') as file:
        file.write(resp.text)

    with open(f"data/.{name}.json", 'r') as file:
        data = json.load(file)

    return data['dataSets'][0]['series']['0:0:0:0:0']['observations']['0'][0]


def exchange_rate(numerator: str, denominator: str = 'EUR', 
                  verbose: bool = True) -> float | None:
    """
    Calculates the exchange rate between two currencies.

    Parameters
    ----------
    numerator : str
        The starting currency indicated with 3 uppercase characters 
        according to ISO 4217.
    denominator : str
        The target currency indicated with 3 uppercase characters 
        according to ISO 4217.
    verbose : bool
        If True, adds additional information. Default is True.

    Returns
    -------
    float
        The exchage rate numerator/denominator.
    """

    numerator = numerator.upper()
    denominator = denominator.upper()

    try:      
        if numerator not in CURRENCIES or denominator not in CURRENCIES:
            if verbose: print('Currency not found.\nConversion not possible.')
            return 0

        if numerator == denominator:
            return 1
        
        if denominator == 'EUR':
            return retrieve_data(numerator, verbose)
        
        if numerator == 'EUR':
            return 1/exchange_rate(denominator, numerator, verbose)

        return(
                retrieve_data(numerator, verbose)/
                retrieve_data(denominator, verbose)
            )
    
    except ZeroDivisionError as error:
        print('Conversion not possible.')
    except TypeError as error:
        print('Conversion not possible.')
    except KeyError as error:
        print('Retrieval error. Likely one or both of the currencies are not in the dataset.')
    except IndexError as error:
        print('Retrieval error. Likely one or both of the currencies are not in the dataset.')
    except RequestException as error:
        print(error)
    except json.decoder.JSONDecodeError as error:
        print(error)
 

if __name__ == '__main__':
    print('US Dollars to Euros', exchange_rate('USD', 'EUR'))
    print('Euros to Swiss Francs', exchange_rate('EUR', 'CHF'))
    print('US Dollars to Swiss Francs', exchange_rate('USD', 'CHF'))
    print('Solaris to Galleons', exchange_rate('SOL', 'GAL'))

