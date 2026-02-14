import random
import os
import unicodedata



# ======================
# OUTILS TEXTE
# ======================

def enlever_accents(texte):
    texte = unicodedata.normalize("NFD", texte)
    resultat = ""
    for c in texte:
        if unicodedata.category(c) != "Mn":
            resultat += c
    return resultat


# ======================
# DICTIONNAIRE
# ======================

def charger_dictionnaire(nom_fichier):
    mots = set()
    with open(nom_fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            mot = ligne.strip().lower()
            mot = enlever_accents(mot)
            mots.add(mot)
    return mots


base_dir = os.path.dirname(__file__)
chemin_dico = os.path.join(base_dir, "dico.txt")
dico_fr = charger_dictionnaire(chemin_dico)

# ======================
# ALPHABETS
# ======================

Alphabet_voyelles = ['a', 'e', 'i', 'o', 'u', 'y']
Alphabet_consonnes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x',
                      'z']


# ======================
# SAISIES
# ======================

def demander_nom_joueur(numero):
    while True:
        nom = input("Nom du joueur " + str(numero) + " : ").strip()
        if nom != "":
            return nom
        else:
            print("Le nom du joueur",numero,"ne peut pas être vide.")


def demander_nb_manches():
    while True:
        try:
            nb = int(input("Combien de manches ? (minimum 2) : "))
            if nb >= 2:
                return nb
            else:
                print("Il faut au moins 2 manches.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")


def demander_nb_lettres(joueur):
    while True:
        try:
            nb = int(input(joueur + ", choisis le nombre de lettres (2 à 10) : "))
            if nb >= 2 and nb <= 10:
                return nb
            else:
                print("Nombre invalide.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")


def demander_nb_voyelles(joueur, nb_lettres):
    while True:
        try:
            nb = int(input(joueur + ", choisis le nombre de voyelles (6 maximum) : "))
            if nb >= 0 and nb <= nb_lettres and nb <= 6:
                return nb
            else:
                print("Nombre invalide.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")


# ======================
# TIRAGE DES LETTRES
# ======================

def choix_voyelles(nb):
    voyelles = []
    for i in range(nb):
        voyelles.append(random.choice(Alphabet_voyelles))
    return voyelles


def choix_consonnes(nb):
    consonnes = []
    for i in range(nb):
        consonnes.append(random.choice(Alphabet_consonnes))
    return consonnes


def choix_lettres(nb_lettres, nb_voyelles):
    nb_consonnes = nb_lettres - nb_voyelles
    lettres = choix_voyelles(nb_voyelles) + choix_consonnes(nb_consonnes)
    random.shuffle(lettres)
    return lettres


# ======================
# CHOIX DU MOT
# ======================

def choix_mot(joueur, lettres, autre_joueur ,mot_interdit=""):
    lettres_str = ""
    for l in lettres:
        lettres_str += l

    while True:
        reponse = input(joueur + ", crée un mot avec : " + lettres_str + " ").lower().strip()

        if reponse == "":
            print()
            print("Mot vide?",joueur, "passe son tour.")
            return ""

        lettres_disponibles = lettres.copy()
        valide = True

        for lettre in reponse:
            if lettre in lettres_disponibles:
                lettres_disponibles.remove(lettre)
            else:
                valide = False
                break

        if not valide:
            print("Lettre absente ou utilisée trop de fois.")
            continue

        if reponse == mot_interdit:
            print("Mot déjà utilisé par :", autre_joueur)
            continue

        if reponse not in dico_fr:
            print("Mot non français.")
            continue

        print("Mot valide !", joueur)
        return reponse



# ======================
# POINTS
# ======================

def calcul_points(mot, lettres):

    if mot == "" :
        return 0

    score = 0
    for lettre in mot:
        if lettre in Alphabet_voyelles:
            score += 2
        else:
            score += 1

    if len(mot) == len(lettres):
        score += 5

    return score

# ======================
#SAUVEGARDE PARTIE
# ======================
def sauvegarder_partie(joueur1,joueur2,score1,score2) :
    with open("sauvegarde_partie.txt","w", encoding="UTF-8") as f:
        f.write(joueur1 + ";"+ str(score1) + "\n")
        f.write(joueur2 + ";"+ str(score2) + "\n")

# ======================
#CHARGER UNE PARTIE
# ======================
def charger_partie() :
    if not os.path.exists("sauvegarde_partie.txt"):
        return None
    with open("sauvegarde_partie.txt","r", encoding="UTF-8") as f:
        lignes = f.read().splitlines()
        joueur1 , score1 = lignes[0].split(";")
        joueur2 , score2 = lignes[1].split(";")
        return joueur1, int(score1), joueur2, int(score2)

# ======================
# UNE MANCHE
# ======================

def jouer_une_manche(joueur_qui_commence, autre_joueur, numero_manche):
    print("\n====================")
    print("MANCHE", numero_manche)
    print(joueur_qui_commence, "commence")
    print("====================\n")

    nb_lettres = demander_nb_lettres(joueur_qui_commence)
    nb_voyelles = demander_nb_voyelles(joueur_qui_commence, nb_lettres)

    lettres = choix_lettres(nb_lettres, nb_voyelles)

    mot1 = choix_mot(joueur_qui_commence, lettres,autre_joueur)

    print("À", autre_joueur, "de jouer maintenant.\n")

    mot2 = choix_mot(autre_joueur, lettres,joueur_qui_commence, mot1)

    print("\nLes deux mots sont acceptés.")
    print("Calcul des scores...\n")

    score1 = calcul_points(mot1, lettres)
    score2 = calcul_points(mot2, lettres)

    print("Mot proposé par ", joueur_qui_commence, ' : ', mot1, '', sep="")
    print("Mot proposé par ", autre_joueur, ' : ', mot2, '', sep="")

    print("\nScore de la manche :")
    print(joueur_qui_commence, ":", score1, "points")
    print(autre_joueur, ":", score2, "points")

    print("\nRésultat de la manche :")
    if score1 > score2:
        print("→", joueur_qui_commence, "gagne la manche")
    elif score2 > score1:
        print("→", autre_joueur, "gagne la manche")
    else:
        print("→ Égalité")

    return score1, score2


# ======================
# PARTIE
# ======================

def main():

    print("\n===================================")
    print("🎮 Bienvenue dans le jeu mot le plus long !")
    print("===================================")
    print("Ce jeu se joue à DEUX joueurs.")
    print("Les parties se joue sur un minimum de 2 manches.")
    print("\nRègles du jeu :")
    print("- Le mot proposé doit être français !")
    print("- Chaque lettre ne peut être utilisée qu'une seule fois")
    print("\nLes points :")
    print("- Les voyelles valent 2 points")
    print("- Les consonnes valent 1 point")
    print("- Bonus de 5 points si toutes les lettres sont utilisées")
    print("===================================")
    print("DEBUT DE LA PARTIE")
    print("***********************************\n")

    print("Veuillez entrer les noms des deux joueurs.\n")

    joueur1 = ""
    joueur2 = ""
    score_total_1 = 0
    score_total_2 = 0
    partie_chargee = False

    # ======================
    # CHARGEMENT
    # ======================

    if os.path.exists("sauvegarde_partie.txt"):
        rep = input("Une partie sauvegardée existe. Voulez-vous la charger (o/n) ? ").lower().strip()

        if rep == "o":
            donnees = charger_partie()
            if donnees:
                joueur1, score_total_1, joueur2, score_total_2 = donnees
                partie_chargee = True

                print("\nPartie chargée :")
                print(joueur1, ":", score_total_1, "points")
                print(joueur2, ":", score_total_2, "points\n")

    # ======================
    # NOUVELLE PARTIE
    # ======================

    if not partie_chargee:
        print("\nNouvelle partie\n")
        joueur1 = demander_nom_joueur(1)
        joueur2 = demander_nom_joueur(2)
        score_total_1 = 0
        score_total_2 = 0

    joueurs = [joueur1, joueur2]
    joueur_depart = random.choice(joueurs)

    if joueur_depart == joueur1:
        autre_joueur = joueur2
    else:
        autre_joueur = joueur1

    # ======================
    # MANCHES
    # ======================

    nb_manches = demander_nb_manches()

    for i in range(nb_manches):

        if i % 2 == 0:
            s1, s2 = jouer_une_manche(joueur_depart, autre_joueur, i + 1)
        else:
            s2, s1 = jouer_une_manche(autre_joueur, joueur_depart, i + 1)

        if joueur_depart == joueur1:
            score_total_1 += s1
            score_total_2 += s2
        else:
            score_total_1 += s2
            score_total_2 += s1

    print("\n====================")
    print("FIN DE LA PARTIE")
    print("====================")
    print(joueur1, ":", score_total_1, "points")
    print(joueur2, ":", score_total_2, "points")

    if score_total_1 > score_total_2:
        print(joueur1, "gagne la partie")
    elif score_total_2 > score_total_1:
        print(joueur2, "gagne la partie")
    else:
        print("Égalité !")

    # ======================
    # SAUVEGARDE PARTIE
    # ======================


    while True:
        rep = input("\nVoulez-vous sauvegarder cette partie (o/n) ? ").lower().strip()

        if rep == "o":
            sauvegarder_partie(joueur1, joueur2, score_total_1, score_total_2)
            print("Partie sauvegardée.")
            break
        elif rep == "n":
            print("Partie non sauvegardée.")
            break
        else:
            print("Veuillez répondre par o ou n.")

    # ======================
    # SAUVEGARDE DES SCORES
    # ======================

    with open("scores_utilisateurs.txt", "a", encoding="utf-8") as f:
        f.write(joueur1 + ";" + str(score_total_1) + "\n")
        f.write(joueur2 + ";" + str(score_total_2) + "\n")

    classement = []

    if os.path.exists("scores_utilisateurs.txt"):
        with open("scores_utilisateurs.txt", "r", encoding="utf-8") as f:
            for ligne in f:
                nom, score = ligne.strip().split(";")
                classement.append((nom, int(score)))

    scores_j1 = []
    scores_j2 = []

    for nom, score in classement:
        if nom == joueur1:
            scores_j1.append(score)
        elif nom == joueur2:
            scores_j2.append(score)

    scores_j1.sort(reverse=True)
    scores_j2.sort(reverse=True)

    top_3_j1 = scores_j1[:3]
    top_3_j2 = scores_j2[:3]

    print("\nTOP 3 des meilleurs scores de", joueur1)
    position = 1
    for score in top_3_j1:
        print(position, ".", score, "points")
        position += 1

    print("\nTOP 3 des meilleurs scores de", joueur2)
    position = 1
    for score in top_3_j2:
        print(position, ".", score, "points")
        position += 1

    classement.sort(key=lambda x: x[1], reverse=True)
    top_5 = classement[:5]

    print("\n🏆 TOP 5 DES MEILLEURS SCORES (TOUS JOUEURS)")
    position = 1
    for element in top_5:
        print(position, ".", element[0], "-", element[1], "points")
        position += 1
    print()


def demander_rejouer():
    while True:
        reponse = input(
            "Voulez-vous jouer une autre partie (o/n) ? "
        ).lower().strip()

        if reponse == "o":
            return True
        elif reponse == "n":
            return False
        else:
            print("Veuillez répondre par o ou n.")


# ======================
# LANCEMENT
# ======================

if __name__ == "__main__":
    while True:
        main()
        if not demander_rejouer():
            print("Merci d'avoir joué !")
            break

