from time import *


def carte_to_chaine(dico):
    var = ""
    char = ""
    if dico["couleur"] == "P":
        char = chr ( 9824 )
    elif dico["couleur"] == "K":
        char = chr ( 9826 )
    elif dico["couleur"] == "C":
        char = chr ( 9825 )
    elif dico["couleur"] == "T":
        char = chr ( 9827 )
    if dico["valeur"] == 10:
        var = "10" + char
    else:
        var = " " + str ( dico["valeur"] ) + char
    return var


def afficher_reussite(liste):
    for e in liste:
        print ( carte_to_chaine ( e ), end=" " )
    print ( "\n" )


def init_pioche_fichier(nom_fich):
    # ouverture fichier
    f = open ( nom_fich )
    pioche = f.read ()
    liste_pioche = pioche.split ( " " )
    for i in range ( len ( liste_pioche ) ):
        if (liste_pioche[i][0] == '1'):
            liste_pioche[i] = {"valeur": int ( liste_pioche[i][0] + liste_pioche[i][1] ), "couleur": liste_pioche[i][3]}
        elif (liste_pioche[i][0] in {'V', 'A', 'D', 'R'}):
            liste_pioche[i] = {"valeur": liste_pioche[i][0], "couleur": liste_pioche[i][2]}
        else:
            liste_pioche[i] = {"valeur": int ( liste_pioche[i][0] ), "couleur": liste_pioche[i][2]}
    # fermeture fichier
    f.close ()
    return liste_pioche


def ecrire_fichier_reussite(nom_fich, pioche):
    # ecrire pioche dans nom_fichier

    with open ( nom_fich, "w" ) as f:
        for elem in pioche:
            a = str ( elem["valeur"] ) + "-" + elem["couleur"] + ' '
            f.write ( a )


# Melange et creation des cartes #

from random import shuffle


def init_pioche_alea(nb_cartes=32):
    couleur = ['T', 'C', 'K', 'P']
    if nb_cartes == 32:
        valeur = [7, 8, 9, 10, 'V', 'D', 'R', 'A']
    if nb_cartes == 52:
        valeur = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'V', 'D', 'R', 'A']
    liste = []

    # creation des cartes

    for x in valeur:
        for y in couleur:
            elem = {'valeur': x, 'couleur': y}
            liste.append ( elem )

    # melange des cartes

    shuffle ( liste )
    return liste

def alliance(carte1, carte2):
    egal = True
    if (carte1["valeur"] == carte2["valeur"]) ^(carte1["couleur"] == carte2["couleur"]):
        return egal
    else:
        return not (egal)


def saut_si_possible(liste_tas, num_tas):
    ok = True
    if num_tas not in [0, len ( liste_tas ) - 1]:
        if alliance ( {"valeur": liste_tas[num_tas - 1]['valeur'], "couleur": liste_tas[num_tas - 1]['couleur']},
                      {"valeur": liste_tas[num_tas + 1]['valeur'], "couleur": liste_tas[num_tas + 1]['couleur']} ):
            liste_tas.pop ( num_tas - 1 )
            return ok
        else:
            return not (ok)
    else:
        return not (ok)


def une_etape_reussite(liste_tas, pioche, affiche=False, affiche_Turtle=False):
    if (len ( pioche ) > 0):
        if affiche:
            print ( "pioche:", end=" " )
            afficher_reussite ( pioche )

            print ( "liste_tas:", end=" " )
            afficher_reussite ( liste_tas )
        if affiche_Turtle:

            affiche_reussite_turtle ( liste_tas,"liste_tas" )
        liste_tas.append ( pioche[0] )
        pioche.pop ( 0 )
        i = 1
        while i < len ( liste_tas ) - 1:

            if saut_si_possible ( liste_tas, i ):

                i = 1
                if affiche:
                    print ( "pioche:", end=" " )
                    if len ( pioche ) > 0:
                        afficher_reussite ( pioche )
                    else:
                        print ( "vide" )
                    print ( "liste_tas:", end=" " )
                    afficher_reussite ( liste_tas )

                if affiche_Turtle:
                    affiche_reussite_turtle(liste_tas,"liste_tas")

            else:
                i = i + 1




# une_etape_reussite([{'valeur':9,'couleur':'T'},{'valeur':'V','couleur':'K'},{'valeur':10,'couleur':'C'},{'valeur':3,'couleur':'P'},{'valeur':'V','couleur':'T'},{'valeur':'D','couleur':'T'},{'valeur':'D','couleur':'P'}],[{'valeur':7,'couleur':'T'}],True)

def reussite_mode_auto(pioche, affiche=False, afficheTurtle=False,nb_pour_gagner=2):
    if afficheTurtle:
        interface (nb_pour_gagner)
        affiche_reussite_turtle(pioche,"pioche")
    liste_tas = [pioche.pop ( 0 ), pioche.pop ( 0 ), pioche.pop ( 0 )]

    while len ( pioche ) != 0:
        une_etape_reussite ( liste_tas, pioche, affiche, afficheTurtle )
    if afficheTurtle:
        #puisque c est le dernier affichage on met True
        affiche_reussite_turtle ( liste_tas,"liste_tas", True )
    if len(liste_tas)<=nb_pour_gagner:
        print("gagner")
    else:
        print("perdu")

    return liste_tas
#reussite_mode_auto(init_pioche_alea(),True,False,8)


def reussite_mode_manuel(pioche, nb_tas_max=2):
    liste_tas = []
    quitter = False
    for i in range ( 3 ):
        liste_tas.append ( pioche.pop ( i ) )
    afficher_reussite ( pioche )
    afficher_reussite ( liste_tas )

    while len ( pioche ) > 0 and not quitter:
        print ( "le menu:\n 1)Découvrir une carte de la pioche\n 2)Faire un saut\n 3)Quitter le jeu\n " )
        while True:
            try:
                reponse = int ( input ( "Répondez par 1,2 ou 3" ) )
                if reponse in [1, 2, 3]: break
            except:
                continue
        if reponse == 1:
            liste_tas.append ( pioche.pop ( 0 ) )
            afficher_reussite ( pioche )
            afficher_reussite ( liste_tas )

        elif reponse == 2:
            while True:
                try:
                    reponse2 = int ( input ( "quelle carte vous voulez sauter" ) )
                    if reponse2 < len ( liste_tas ): break
                except:
                    continue
            possible = saut_si_possible ( liste_tas, reponse2 )
            if not (possible):
                print ( "Saut non autorisé!!" )
            else:
                afficher_reussite ( pioche )
                afficher_reussite ( liste_tas )
        else:
            print ( "Vous avez quitté le jeu" )
            for i in pioche:
                liste_tas.append ( i )
            afficher_reussite ( liste_tas )
            quitter = True

    if len ( liste_tas ) <= nb_tas_max:
        print ( "gagner" )
        return True
    else:
        print ( "perdu" )
        return False


def lance_reussite(mode, nb_cartes=32, affiche=False, nb_tas_max=2):
    if mode == 'auto':
        liste = reussite_mode_auto ( init_pioche_alea ( nb_cartes ), affiche )
    elif mode == 'manuel':
        liste = reussite_mode_manuel ( init_pioche_alea ( nb_cartes ), nb_tas_max )
    return liste


# extensions:

def verifier_pioche(pioche, nb_cartes=32):
    test = True
    cartes_adequates = True
    for i in range ( len ( pioche ) - 1 ):
        if pioche.count ( pioche[i] ) != 1:
            test = False
    for i in range ( len ( pioche ) - 1 ):
        if nb_cartes == 32:
            if (pioche[i]["valeur"] not in [7, 8, 9, 10, 'V', 'D', 'R', 'A']) or (
                    pioche[i]["couleur"] not in ['T', 'C', 'K', 'P']):
                cartes_adequates = False
        elif nb_cartes == 52:
            if (pioche[i]["valeur"] not in [2, 3, 4, 5, 6, 7, 8, 9, 10, 'V', 'D', 'R', 'A']) or (
                    pioche[i]["couleur"] not in ['T', 'C', 'K', 'P']):
                cartes_adequates = False
    return len ( pioche ) == nb_cartes and test and cartes_adequates


def res_multi_simulation(nb_sim,nb_cartes=32):
    nb_tas=[]
    for i in range(nb_sim):
        pioche=init_pioche_alea(nb_cartes)
        nb_tas.append(len(reussite_mode_auto(pioche)))
    return nb_tas





def statistiques_nb_tas(nb_sim, nb_cartes=32):
    liste_nb_tas = res_multi_simulation ( nb_sim, nb_cartes )
    print ( "liste_nb_tas:", liste_nb_tas )
    max_nb_tas = max ( liste_nb_tas )
    min_nb_tas = min ( liste_nb_tas )
    moyenne_nb_tas = sum ( liste_nb_tas ) / len ( liste_nb_tas )
    return max_nb_tas, min_nb_tas, moyenne_nb_tas


import matplotlib.pyplot as plt


def estimation_graphique(nb_carte=32):
    # creation d une liste contenant les différent nb de tas pour 1000 essaie
    liste_nb_tas = res_multi_simulation ( 1000, nb_carte )
    print ( liste_nb_tas )
    # on tri la liste
    liste_nb_tas.sort ()
    liste_estimation = []
    # pour chaque valeur appartenant a la liste_nb_tas on récupére la moyenne pour gagner et on la place dans une liste estimation
    for e in liste_nb_tas:
        i = 0
        for j in liste_nb_tas:
            if j <= e:
                i = i + 1
        liste_estimation.append ( i / len ( liste_nb_tas ) )
    print(liste_estimation)


    # partie graphique avec matplotlib
    plt.title ( "Estimation en fonction des nb de tas" )
    # On trace la figure les nb_tas en abscisse et les estimations en ordonnées
    plt.plot ( liste_nb_tas, liste_estimation )

    plt.xlabel ( 'nb tas pour gagner' )
    plt.ylabel ( 'estimation' )
    plt.show ()  # On montre le graph

estimation_graphique()




def meilleur_echange_consecutif(pioche):
    copy_pioche = pioche.copy ()
    print ( "la pioche initial:", end=" " )
    afficher_reussite ( pioche )
    #recupérer le nombre de tas pour la pioche a l état initial
    nb_tas_initial = len ( reussite_mode_auto ( copy_pioche ) )
    #generer une liste qui contiendra le nombre de tas pour chaque cas(pour chaque echange)
    tous_nb_tas_possible = [nb_tas_initial]
    #on va parcourir la pioche et pour chaque position :
    for i in range ( len ( pioche ) - 1 ):
        copy_pioche = pioche.copy ()
        #on fait l echange
        copy_pioche[i], copy_pioche[i + 1] = copy_pioche[i + 1], copy_pioche[i]
        #on ajoute a la liste tous_nb_tas_possible le nombre de tas si on fait cet echange
        tous_nb_tas_possible.append ( len ( reussite_mode_auto ( copy_pioche ) ) )
    #on recupére la position de la plus petite valeur de la liste tous_nb_tas_possible
    min = tous_nb_tas_possible[0]
    indice_min = 0
    for k in range ( 1, len ( tous_nb_tas_possible ) ):
        if min >= tous_nb_tas_possible[k]:
            min = tous_nb_tas_possible[k]
            indice_min = k
    print ( "l echange est fait au position: ", indice_min - 1 )

    #si l état initial c est le meilleur cas on fais rien
    if indice_min == 0:
        afficher_reussite ( pioche )
        return pioche, nb_tas_initial
    # on fait l échange sur la pioche a la position indice_min-1:
    else:
        pioche[indice_min - 1], pioche[indice_min] = pioche[indice_min], pioche[indice_min - 1]
        print ( "la pioche au final:", end=" " )
        afficher_reussite ( pioche )

        n = nb_tas_initial - min
        return pioche, n

def meilleur_echange_posible(pioche):
    copy_pioche = pioche.copy ()
    print ( "la pioche initial:", end=" " )
    afficher_reussite ( pioche )
    #recupérer le nombre de tas pour la pioche a l état initial
    nb_tas_initial = len ( reussite_mode_auto ( copy_pioche ) )
    #generer une liste qui contiendra le nombre de tas pour chaque cas(pour chaque echange)
    tous_nb_tas_possible = [nb_tas_initial]
    l=[(0,0)]
    #on va parcourir la pioche et pour chaque position :
    for j in range (len(pioche)-1):
        for i in range ( len ( pioche ) - 1 ):
            if j!=i:
                copy_pioche = pioche.copy ()
                #on fait l echange
                copy_pioche[j], copy_pioche[j + 1] = copy_pioche[j + 1], copy_pioche[j]
                #on ajoute a la liste tous_nb_tas_possible le nombre de tas si on fait cet echange
                tous_nb_tas_possible.append ( len ( reussite_mode_auto ( copy_pioche ) ) )
                l.append((j,i))
    #on recupére la position de la plus petite valeur de la liste tous_nb_tas_possible
    min = tous_nb_tas_possible[0]
    indice_min = 0
    for k in range ( 1, len ( tous_nb_tas_possible ) ):
        if min >= tous_nb_tas_possible[k]:
            min = tous_nb_tas_possible[k]
            indice_min = k
    print ( "l echange est fait au position: ", l[indice_min][0],l[indice_min][1] )

    #si l état initial c est le meilleur cas on fais rien
    if indice_min == 0:
        afficher_reussite ( pioche )
        return pioche, nb_tas_initial
    # on fait l échange sur la pioche a la position indice_min-1:
    else:
        pioche[l[indice_min][0]], pioche[l[indice_min][1]] = pioche[l[indice_min][1]], pioche[l[indice_min][0]]
        print ( "la pioche au final:", end=" " )
        afficher_reussite ( pioche )

        n = nb_tas_initial - min
        return pioche, n

#p,n=meilleur_echange_possible(init_pioche_alea())
#print(n)

from turtle import *


def charge_image():
    fenetre = Screen ()
    valeurs = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R']
    couleurs = ['P', 'C', 'K', 'T']
    carte = {}
    for c in couleurs:
        for v in valeurs:
            fichier = "imgs/carte-" + v + '-' + c + '.gif'
            carte[c, v] = fichier
            fenetre.register_shape ( fichier )

    return carte, fenetre

# afficher les cartes de la liste l_carte passer on parametre
def affiche_reussite_turtle(l_cartes,etat,derniere=False):
    # on charge les images dans le dictionnaire carte grace a la fonction charge_image
    carte, fenetre = charge_image ()
    dos = "imgs/carte-dos.gif"
    fenetre.register_shape ( dos )#on charge l image de dos
    largeur_carte = 44
    hauteur_carte = 64
    separation_x = 5
    separation_y = 10
    xinit = -300
    yinit = 200
    up ()
    tampons = {}

    y = yinit

    x = xinit
    goto(-300,250)
    pencolor ( "red" )
    write(etat,font=("Arial", 16, "normal"))

    for j in range ( 0, len ( l_cartes ) + 1,8):
        #on va afficher 8 cartes pour chaque ligne
        for e in l_cartes[j:j + 8]:
            shape ( dos )  # pour faire joli: on affiche le dos des cartes pendant
            # le déplacement de la tortue
            goto ( x, y )  # on déplace la tortue à l'endroit voulu
            shape ( carte[e['couleur'], str ( (e['valeur']) )] )  # on change la "forme" de la tortue pour
            # l'image de la carte correspondante
            tampons[e['couleur'], e['valeur']] = stamp ()  # on "tamponne" la forme et on sauvegarde le
            # numéro du tampon

            x = x + largeur_carte + separation_x
        x = xinit
        y = y - hauteur_carte - separation_y

    hideturtle ()  # on cache la tortue
    sleep (5) #attendre 5s

    #si derniere== True on clique sur l écran pour fermer la fenetre
    if derniere:
        write ( "Cliquez dans la fenêtre pour terminer.", align='center' )
        exitonclick ()  # on attend un clic et on ferme la fenetre
    clear ()




def interface(nb_pour_gagner=2):
    fenetre = Screen ()
    bgpic("imgs/jeux_de_carte.gif")
    up ()
    goto(-350,140)
    pencolor("red")
    write ( "Bienvenue dans notre jeux ", font=("Arial", 26, "normal") )
    goto(-350,50)
    pencolor("blue")
    write ( "il faut avoir "+str(nb_pour_gagner)+" tas a la fin pour gagner" , font=("Arial", 16, "normal") )
    hideturtle ()
    sleep(3)
    clear()


#reussite_mode_auto(init_pioche_alea(),True,True)
