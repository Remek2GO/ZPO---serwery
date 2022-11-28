Product = ["dw12", "nt672", "DJ909", "dwr664", "dbl2311", "WWA515", "Q4", "gsc432", "alan404"]

def get_entries (n_letters: int):
    outcome = []
    for x in Product:
        if len(x) <= n_letters+3:
            try:
                if (90 >= ord(x[n_letters-1]) >= 65) or ( 122 >= ord(x[n_letters-1]) >= 97)  and (57 >= ord(x[n_letters]) >= 48) :  
                    outcome.append(x)
            except: 
                pass
    return (outcome)

print(get_entries(2))