import numpy as np
from scipy.linalg import eigh


def frecs_and_dmod(G_FREE, K_EQ, M_EQ, BOUNDRIES = ['firm', 'firm']):

    '''
    Return the natural frecuencies and the modal shape of a coupled mass-spring sistem where
        G_FREE: Degrees of freedom of the system
        K_EQ: The equivalent stiffnes in N/m
        M_EQ: The equivalent mass in Kg
        BOUNDRIES: Change between firm or free border condition
    '''
    
    NUM_SPRINGS = G_FREE + 1
    NUM_NODES = NUM_SPRINGS + 1

    #Create the mass and stiffnes matrix
    mass_equivalent = np.ones(NUM_NODES) * M_EQ
    matriz_Mglobal = np.diag(mass_equivalent)

    k_equivalent = np.ones(NUM_NODES) * K_EQ
    matriz_Kglobal = np.diag(k_equivalent * 2) + np.diag(-k_equivalent[:-1] , 1) + np.diag(-k_equivalent[:-1] ,-1)
    matriz_Kglobal[0,0] = K_EQ
    matriz_Kglobal[-1,-1] = K_EQ

    #Check boundrie condition
    r = np.arange(NUM_NODES)
    s = []

    if BOUNDRIES[0] == 'firm':
     	matriz_Kglobal[0][0] += K_EQ
     	s.append(0)
    if BOUNDRIES[1] == 'firm':
     	matriz_Kglobal[-1][-1] += K_EQ
     	s.append(NUM_NODES - 1)

    r = np.delete(r,s)

    #Resize matrix if border is firm
    matriz_Mred = matriz_Mglobal[np.ix_(r,r)]
    matriz_Kred = matriz_Kglobal[np.ix_(r,r)]

    w_2, dmod = eigh(matriz_Kred, matriz_Mred)
    w = np.sqrt(w_2)

    dmod = np.transpose(dmod/dmod[-1,:])  #Normalize

    #Add border condition
    if len(s) > 1:
        s[1] -= 1

    u_n = np.zeros(NUM_NODES)
    dmod = np.insert(dmod, (s), u_n[s].reshape(1,-1),  axis = 1 )

    return w, dmod
