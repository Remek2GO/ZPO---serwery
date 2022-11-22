

produkty = ["dw12", "nt672", "DJ909", "dwr664", "dbl2311", "WWA515", "Q4", "gsc432"]

def search_products (n_letters: int):
    outcome = []
    for x in produkty:
        if len(x) <= n_letters+3:
            try:
                if (ord(x[n_letters-1]) >= 65 and ord(x[n_letters-1]) <= 90) or (ord(x[n_letters-1]) >= 97 and ord(x[n_letters-1]) <= 122):  
                    outcome.append(x)
            except: 
                pass
    return (outcome)
        
    




print(search_products(3))
