import datetime
from flask import Flask, render_template, request, redirect, g, session
from flask_session import Session
from traitement import nb_vote,calculpola, tri_fusion_paire
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"]="jesuisunclrtrissicrtekarpafransaise"
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filsystem"
Session()

### VARIABLE GLOBALE ###

TAGS = ["Tag" + str(k) for k in range(1,6)]


DATABASE = 'donnees.db'

ERROR_DICT = {
    "0":" Vos informations sont erronées. Veuillez réessayer",
    "1":" Le nom de votre projet est vide. Veuillez réessayer.",
    "2":" La description de votre projet est vide. Veuillez réessayer.",
    "3":" Deux tags ne peuvent pas être identiques. Veuillez réessayer.",
    "4":" Vous devez rentrer un nom pour vous connecter. Veuillez réessayer.",
    "5":" Vous devez rentrer un prénom pour vous connecter. Veuillez réessayer.",
    "6":" Vous devez rentrer un courriel pour vous connecter. Veuillez réessayer.",
    "7":" Vous devez rentrer un mot de passe pour vous connecter. Veuillez réessayer.",
    "8":" Vous êtes déjà déconnecté.",
    "9":" Le projet que vous cherchez n'existe pas. Veuillez réessayer.",
    "10":" Vous ne pouvez pas voter sans écrire un commentaire ! Veuillez réessayer.",
    "666": "Vous nous pouvez pas aller sur une page d'erreur qui n'existe pas. Veuillez ne pas réessayer !"
}

### FONCTIONS BASE DE DONNÉES

def get_db():
    """
    Connexion à la base de données
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    déconnexion propre de la base de données
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def table_note():
    """
    Insère toutes les valeurs possibles dans la table note.
    A ne jamais utiliser sauf si vous supprimer le fichier donnees.db
    """
    db = get_db()
    c = db.cursor()
    val = -799 #valeur de départ car on a déjà créer la valeur -8 dans la table
    for i in range(2, 1602):
        c.execute("INSERT INTO NOTE VALUES ("+str(i)+", "+str(val/100)+")") #insertion de la valeur
        val += 1
    db.commit()
    return None


### FONCTIONS AUTRES ###

def max_id(table):
    """
    renvoie l'identifiant max d'une table donnée en entrée
    """
    db = get_db()
    c = db.cursor()
    c.execute("SELECT MAX("+str(table)+"_id) FROM "+str(table)) 
    res = c.fetchall()
    if type(res[0][0]) != int: #si la table est vide l'id max est 0
        return 0
    else: #cas d'une table non vide
        return res[0][0]



### ROUTES POUR L'APPLICATION WEB ###

@app.route("/", methods=["GET","POST"]) #route qui mène à la page d'acceuil
def index():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/connexion")
    return render_template("index.html")


@app.route("/proposition", methods=['GET']) # on propose un projet
def proposition():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/connexion")
    db = get_db()
    c = db.cursor()
    c.execute("SELECT nom FROM tag") # récupère les nom des tags
    res = c.fetchall()
    return render_template("proposition.html", TAGS = res)

@app.route("/verification", methods=['POST']) # une review du projet proposé, pour être sur avant de valider
def projet():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/connexion")
    if not request.form.get("titre"): #vérifie qu'un nom de projet est proposé
        return redirect("/error/1")
    if not request.form.get("desc"): #vérifie qu'une description de projet est proposée
        return redirect("/error/2")  
          
    else: # erreur si aucun tag n'a été mis lors de la publication du projet
        for i in range(1, 6):
            for j in range(1, 6):
                if request.form.get("Tag "+str(i)) != "Aucun" and request.form.get("Tag "+str(j)) != "Aucun" and i != j and request.form.get("Tag "+str(i)) == request.form.get("Tag "+str(j)):
                    return redirect("/error/3")
                else:
                    continue
        
        ptags = []
        session["pname"] = request.form['titre']
        session["ptag1"] = request.form['Tag 1']
        session["ptag2"] = request.form['Tag 2']
        session["ptag3"] = request.form['Tag 3']
        session["ptag4"] = request.form['Tag 4']
        session["ptag5"] = request.form['Tag 5']
        session["pdesc"] = request.form['desc'] # récupération des informations du projet
        for k in range(1,6):
            t = session["ptag"+str(k)]
            if t != "Aucun":
                ptags.append(t)
        session["ptags"] = ptags #récupération des tags
        return render_template('verification.html', titre = session["pname"], description = session["pdesc"], tags = ptags)


@app.route("/modification", methods=['GET', 'POST'])  # modification d'un projet proposé (avant validation)
def modification():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/connexion")
    session["pname"] = request.form['titre']
    session["pdesc"] = request.form['desc'] # on récupềre ce qui a été proposé pour pouvoir le modifier ensuite
    db = get_db()
    c = db.cursor()
    c.execute("SELECT nom FROM tag") #on récupère les noms des tags
    res = c.fetchall()
    return render_template('modification.html', titre = session["pname"], description = session["pdesc"], TAGS = res)


@app.route("/sauvegarde", methods=['GET', 'POST'])  # ajout d'un projet à la base de donnée lorsqu'on le propose
def sauvegarde():
    db = get_db()
    c = db.cursor()
    name = session["pname"]
    desc = session["pdesc"] # on récupềre ce qui a été proposé pour pouvoir le sauvegarder ensuite
    ptags = session["ptags"]
    k = len(session["ptags"])
    for i in range(1,k+1):
        indice = c.execute("SELECT tag_id FROM tag where nom = '"+ptags[i-1]+"'").fetchone()
        session["ptag"+str(i)] = indice[0]
           
    while k < 5:
        session["ptag"+str(k+1)] = None #complète la liste des tags avec des valeur None pour obtenir une liste de longueur 5
        k += 1
    
    maximum_id = max_id("projet")+1
    datede = str(datetime.date.today())
    #on récupère le maximum_id des projets, on rajoute un pour avoir un nouvel id pas utilisé

    c.execute("INSERT INTO projet VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (maximum_id,name,desc,session["ptag1"],session["ptag2"],session["ptag3"],session["ptag4"],session["ptag5"], session["id"], datede, 0, 801))
    db.commit()
    session["pname"]=None
    session["pdesc"]=None #reset des valeurs pour une possible futur proposition de projet
    session["ptags"]=None
    session["ptag1"]=None
    session["ptag2"]=None
    session["ptag3"]=None
    session["ptag4"]=None
    session["ptag5"]=None

    return redirect("/mes_projets")


@app.route("/mes_projets", methods = ['GET']) # la liste de nos projets
def own_project():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/connexion")
    db = get_db()
    c = db.cursor()

    projet = c.execute("SELECT * FROM projet WHERE createur_id = "+str(session["id"])).fetchall()
    notation = c.execute("SELECT valeur FROM note JOIN projet ON projet.note_id = note.note_id WHERE createur_id = "+str(session["id"])).fetchall()
    nmb_Vote = c.execute("SELECT COUNT(*),projet.projet_id FROM vote JOIN projet ON vote.projet_id = projet.projet_id WHERE projet.createur_id = "+str(session["id"])+" GROUP BY projet.projet_id ").fetchall()
    p_id = c.execute("SELECT projet_id FROM projet WHERE createur_id = "+str(session["id"])).fetchall() # récupération des informations sur les projets
    nb_vote_totaux = nb_vote(nmb_Vote,p_id)
    tmp = []
    for element in nb_vote_totaux: # on garde uniquement les notes des projets, pas les indices
        note, id = element
        tmp.append(note)
    nb_vote_totaux = tmp

    tags = []
    statut = []
    taille = [k for k in range (0,len(projet))]
    for proj in projet:
        tag = []
        if proj[10] == 0: 
        # définit si un projet est traité par la mairie ou non
            statut.append("En cours de traitement")
        else:
            statut.append("Votre projet a été étudié par la mairie")
        for k in range (3,8): #on récupère les tags
            pas = proj[k]
            if pas != None:
                t = c.execute("SELECT tag.nom FROM tag JOIN projet ON tag.tag_id =" + str(pas)).fetchall()
                tag.append(t[0][0])
        tags.append(tag)

    return render_template('mes_projets.html', projet = projet,N = taille, tags = tags, statut = statut, note = notation, nmb_vote = nb_vote_totaux)


@app.route("/delete", methods = ["POST"])
def deregister():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/connexion")
    db = sqlite3.connect('donnees.db', check_same_thread=False)
    cur = db.cursor()

    id_eliminer = request.form.get("id") # élimine un projet de la base de donnée lorsque son auteur décide de le supprimer
    
    cur.execute("DELETE FROM projet WHERE projet_id = ?", (id_eliminer, ))
    cur.execute("DELETE FROM vote WHERE projet_id = ?", (id_eliminer,))
    db.commit()

    return redirect("/mes_projets")


@app.route("/connexion", methods=["GET", "POST"]) # la page de connexion
def connexion():
    if request.method == "POST":
        db = get_db()
        c = db.cursor()
        #gestion des erreurs
        if not request.form.get("nom"):
            return redirect("/error/4")
        if not request.form.get("prenom"):
            return redirect("/error/5")
        if not request.form.get("mail"):
            return redirect("/error/6")
        if not request.form.get("mdp"):
            return redirect("/error/7")
        #récupération des informations du form
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        courriel = request.form.get("mail")
        mdp = request.form.get("mdp")
        c.execute("SELECT utilisateur_id FROM utilisateur WHERE nom LIKE '"+str(nom)+ "' AND prenom LIKE '"+str(prenom)+"' AND courriel LIKE '"+str(courriel)+"' AND mdp LIKE '"+str(mdp)+"'")
        res = c.fetchall()
        #vérification des informations
        if res == []:
            return redirect("error/0")
        else:
            session["id"] = res[0][0]
            session["nom"] = nom
            session["prenom"] = prenom
            session["courriel"] = courriel
            return redirect("/connexion")
    else:
        return render_template("connexion.html")


@app.route("/deconnexion")
def deconnexion():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/error/8")
    
    session["id"] = None
    return redirect("/connexion")


@app.route("/error/<f>")
def error_page(f):
    if f not in ERROR_DICT: #vérifie que l'erreur demandée existe
        return redirect("/error/666")

    return render_template("error_page.html", error_number = f, error_message=ERROR_DICT[f])


@app.route("/projets", methods = ["GET", "POST"])
def projets():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/connexion")
    db = get_db()
    c = db.cursor()
    p_id = c.execute("SELECT projet_id FROM projet WHERE statut = 0").fetchall()

    if not request.form.get("type_tri"): # si aucun tri n'est mis, on affiche dans l'ordre d'indice de projet
        liste_tri =[]
        for element in p_id:
            liste_tri.append(element[0])

    else:        

        if request.form.get("type_tri") == "1": # tri par ordre alphabétique
            projet_alphabet = c.execute("SELECT nom, projet_id FROM projet WHERE statut = 0").fetchall()
            liste_tri = tri_fusion_paire(projet_alphabet)

        if request.form.get("type_tri") == "2": # tri par note décroissante
            projet_note = c.execute("SELECT valeur, projet.projet_id FROM note JOIN projet ON projet.note_id = note.note_id WHERE projet.statut = 0").fetchall()
            liste_tri = tri_fusion_paire(projet_note)[::-1]

        if request.form.get("type_tri") == "3": # tri par note croissante
            projet_note = c.execute("SELECT valeur, projet.projet_id FROM note JOIN projet ON projet.note_id = note.note_id WHERE projet.statut = 0").fetchall()
            liste_tri = tri_fusion_paire(projet_note)


        if request.form.get("type_tri") == "4": # tri par nombre de commentaire décroissant
            projet_nb_vote = c.execute("SELECT COUNT(*), projet.projet_id FROM vote JOIN projet ON vote.projet_id = projet.projet_id WHERE statut = 0 GROUP BY projet.projet_id").fetchall()
            tmp = []
            for element in projet_nb_vote:
                tmp.append(element[1])
            for element in p_id :
                if not element[0] in tmp:
                    projet_nb_vote.append((0, element[0]))
   
            liste_tri = tri_fusion_paire(projet_nb_vote)[::-1]

        if request.form.get("type_tri") == "5": # tri par nombre de commentaire croissant
            projet_nb_vote = c.execute("SELECT COUNT(*),projet.projet_id FROM vote JOIN projet ON vote.projet_id = projet.projet_id WHERE statut = 0 GROUP BY projet.projet_id").fetchall()
            tmp = []
            for element in projet_nb_vote:
                tmp.append(element[1])
            for element in p_id :
                if not element[0] in tmp:
                    projet_nb_vote.append((0, element[0]))
            
            
            liste_tri = tri_fusion_paire(projet_nb_vote)

        tmp = []
        for element in liste_tri:
            el1, id = element
            tmp.append(id)
        liste_tri = tmp

    projet = []
    note = []
    nb_vote_totaux = []
    for element in liste_tri: # affichage selon le tri choisis précédemment 
        c.execute("SELECT * FROM projet WHERE statut = 0 and projet_id = "+str(element))
        projet.append(c.fetchall()[0])
        c.execute("SELECT COUNT(*) FROM vote JOIN projet ON vote.projet_id = projet.projet_id WHERE projet.projet_id = "+str(element))
        nb_vote = c.fetchall()[0][0]
        if type(nb_vote) != int: #si le projet n'a pas de vote alors on lui assigne un compteur de 0
            nb_vote_totaux.append(0)
        else:
            nb_vote_totaux.append(nb_vote)
        c.execute("SELECT valeur FROM note JOIN projet ON projet.note_id = note.note_id WHERE projet.statut = 0 and projet.projet_id = "+str(element))
        note.append(c.fetchall()[0][0])
    
    tags = []
    taille = [k for k in range (0,len(projet))]
    
    for proj in projet: # récupération des tags 
        tag = []
        for k in range (3,8):
            pas = proj[k]
            if pas != None:
                t = c.execute("SELECT tag.nom FROM tag JOIN projet ON tag.tag_id =" + str(pas) + " where tag.tag_id is not null").fetchall()
                tag.append(t[0][0])
        tags.append(tag)
    return render_template("projets.html",projet = projet, N=taille, nom = session["nom"], prenom = session["prenom"], tags=tags, note = note, nmb_vote = nb_vote_totaux)


@app.route("/projet/<f>")
def projet_1(f): #f est l'identifiant du projet qui apparait dans l'url
    #ouverture de la base de données
    if not session.get("id"): #vérifie que le visiteur est connecté
            return redirect("/connexion")
    db = get_db()
    c = db.cursor()

    projet = c.execute("SELECT * FROM projet WHERE projet_id =" + str(f)).fetchall()
    if projet == []:
       return redirect("/error/9")
    #récupération des données à afficher
    commentaires = c.execute("SELECT commentaire,vote_id,votant_id FROM vote WHERE projet_id = " + str(f)).fetchall()

    tag = []
    nom_projet = projet[0][1]
    note = c.execute("SELECT valeur FROM note n JOIN projet p ON n.note_id = p.note_id WHERE projet_id = " + str(f)).fetchall()
    note = note[0][0]
    if projet[0][10] == 0: # définit si un projet à été traité par la mairie
        statut = "En cours de traitement"
    else:
        statut = "Votre projet a été étudié par la mairie"
    for k in range (3,8):
        pas = projet[0][k]
        if pas != None:
            t = c.execute("SELECT tag.nom FROM tag JOIN projet ON tag.tag_id =" + str(pas) + " where tag.tag_id is not null").fetchall()
            tag.append(t[0][0])

    c.execute("SELECT COUNT(*) FROM VOTE WHERE projet_id = "+str(f) + " AND votant_id = "+str(session["id"]))
    dv = c.fetchall()
    if dv[0][0] == 0: #vérifie si l'utilisateur à déjà voté et si oui alors il ne peut plus voter
        return render_template("projet.html",projet = projet, nom = session["nom"], prenom = session["prenom"],id_connexion = session["id"], tags=tag, commentaires = commentaires, nom_projet = nom_projet, note = note, statut = statut, dv = 0)
    else:
        return render_template("projet.html",projet = projet, nom = session["nom"], prenom = session["prenom"],id_connexion = session["id"], tags=tag, commentaires = commentaires, nom_projet = nom_projet, note = note, statut = statut, dv = 1)


@app.route("/comment", methods=["GET", "POST"])
def commentaire():
    if not session.get("id"): #vérifie que le visiteur est connecté
            return redirect("/connexion")

    db = get_db()
    c = db.cursor()
    if request.form.get("com")=="": # renvoie d'erreur "pas de commentaire"
        return redirect("/error/10")

    new_com = request.form.get("com")    

    note = calculpola(new_com) # calcul de la polarité du commentaire 
    note = round(note,2)

    id = request.form.get("id_projet")
    c.execute("SELECT note_id FROM note WHERE valeur = " + str(note))
    note_id = c.fetchall()[0][0]

    c.execute("SELECT COUNT(*) FROM vote WHERE projet_id = " + str(id))
    nb_vote = c.fetchall()[0][0]

    c.execute("INSERT INTO vote VALUES (?,?,?,?,?)", (max_id("vote")+1 , id , session["id"] , new_com , note_id))
    db.commit()

    c.execute("SELECT valeur FROM note JOIN projet ON note.note_id = projet.note_id WHERE projet_id = "+str(id))
    ancienne_moyenne = c.fetchall()[0][0] # calcul de la nouvelle moyenne du projet
    moyenne = (nb_vote * ancienne_moyenne + note) / (nb_vote + 1)
    moyenne = round(moyenne, 2)

    c.execute("SELECT note_id FROM note WHERE valeur = "+str(moyenne))
    moyenne_id = c.fetchall()[0][0]

    c.execute("UPDATE projet SET note_id = "+str(moyenne_id)+" WHERE projet_id = " +str(id))
    db.commit()
  
    return redirect("/projet/"+str(id))


@app.route("/meaculpa", methods = ["POST"])
def annule_com():
    if not session.get("id"): #vérifie que le visiteur est connecté
        return redirect("/connexion")
    db = sqlite3.connect('donnees.db', check_same_thread=False)
    cur = db.cursor()

    elimine = request.form.get("avis") # récupére l'avis a éliminer

    note = calculpola(elimine)
    note = round(note,2)

    id = request.form.get("id_proj")
    vote = request.form.get("id_v")

    cur.execute("SELECT COUNT(*) FROM vote WHERE projet_id = " + str(id))
    nb_vote = cur.fetchall()[0][0]
    cur.execute("SELECT valeur FROM note JOIN projet ON note.note_id = projet.note_id WHERE projet_id = "+str(id))
    if nb_vote == 0 or nb_vote == 1:
        moyenne = 0
    else:
        ancienne_moyenne = cur.fetchall()[0][0] #calcul de la nouvelle moyenne avec le commentaire en moins
        moyenne = (nb_vote * ancienne_moyenne - note) / (nb_vote - 1)
        moyenne = round(moyenne, 2)

    cur.execute("SELECT note_id FROM note WHERE valeur = "+str(moyenne))
    moyenne_id = cur.fetchall()[0][0]

    cur.execute("UPDATE projet SET note_id = "+str(moyenne_id)+" WHERE projet_id = " +str(id))
    db.commit()

    cur.execute("DELETE FROM vote WHERE vote_id=" + str(vote) +" AND commentaire = ?", (elimine,))
    db.commit() 

    return redirect("/projet/"+str(id))
