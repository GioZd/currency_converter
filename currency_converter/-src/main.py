'''
CURRENCY CONVERTER v.0.0
Author: Giovanni Zedda
Last Change: 27th June 2024
Description: Convert a numerical value from
    a currency to another one. By using an EBC data API
'''

import tkinter as tk
from tkinter import ttk

from exr import CURRENCIES, exchange_rate

def main():
    def compute_result():      
        try:
            value = float(value1.get())
            orig = currency1.get()
            dest = currency2.get()   
            result = round(value/exchange_rate(orig, dest), 3)   
            value2.delete(0, tk.END)
            value2.insert(0, str(result))

        except ZeroDivisionError as err:
            print(f"Conversion not possible. Likely one or both " 
                  f"of the currencies are not in the dataset.")
            value2.delete(0, tk.END)
            value2.insert(0, '???')
        except TypeError as err:
            print(f"Conversion not possible. Likely one or both " 
                  f"of the currencies are not in the dataset.")
            value2.delete(0, tk.END)
            value2.insert(0, '???')
        except ValueError as err:
            value1.delete(0, tk.END)
            value1.insert(0, 'Numeric input only')

    root = tk.Tk()
    root.title('Exchange money')
    root.configure(
        background='#0033A0'
    )

    value1 = tk.Entry(root, width=20)
    currency1 = ttk.Combobox(root, values=sorted(list(CURRENCIES)), 
                             width=16, height=2)
    value2 = tk.Entry(root, width=20)

    currency2 = ttk.Combobox(root, values=sorted(list(CURRENCIES)), 
                             width=16, height=2)
    
    value1.grid(row=0, column=0, padx=(12, 5), pady=(15,5))
    currency1.grid(row=0, column=1, padx=(5, 12), pady=(15,5))
    value2.grid(row=2, column=0, padx=(12, 5), pady=5)
    currency2.grid(row=2, column=1, padx=(5, 12), pady=5)

    value1.delete(0, tk.END)
    value1.insert(0, 'Input here...')
    value2.delete(0, tk.END)
    value2.insert(0, '...Output here!')
    currency1.delete(0, tk.END)
    currency1.insert(0, 'USD')
    currency2.delete(0, tk.END)
    currency2.insert(0, 'EUR')

    compute_button = tk.Button(root, text="Compute", command=compute_result)
    compute_button.grid(row=4, columnspan=2, pady=12)

    root.mainloop()


if __name__ == '__main__':
    main()