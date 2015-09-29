Module de recrutement
---------------------


Agent
  status
  FK(DSI_Individu, null=True)
  FK(Int_Individu, null=True)

CCOURS_Individu
    id = models.IntegerField(db_column='INDIV_ID', primary_key=True)
    numero = models.IntegerField(db_column='INDIV_NUMERO')
    civilite = models.CharField(max_length=20, db_column='INDIV_CIVILITE')
    nom_pat = models.CharField(max_length=2000, db_column='INDIV_NOM_PAT')
    nom_usuel = models.CharField(max_length=2000, db_column='INDIV_NOM_USUEL')
    prenom = models.CharField(max_length=2000, db_column='INDIV_PRENOM')
    dnaissance = models.DateField(db_column='INDIV_DNAISSANCE')
    dept_naissa = models.CharField(max_length=3, db_column='INDIV_DEPT_NAISSA')
    ville_naiss = models.CharField(max_length=2000, db_column='INDIV_VILLE_NAISS')
    pays_naiss = models.CharField(max_length=3, db_column='INDIV_PAYS_NAISS', )
    pays_nationalite = models.CharField(max_length=3, db_column='INDIV_PAYS_NATIONALITE', )
    sitfam = models.CharField(max_length=1, db_column='INDIV_SITFAM')
    no_insee = models.CharField(max_length=13, db_column='INDIV_NO_INSEE')
    cle_insee = models.IntegerField(db_column='INDIV_CLE_INSEE')
    mail = models.CharField(db_column='INDIV_MAIL', max_length=2000)
    login = models.CharField(db_column='INDIV_LOGIN', max_length=2000)
    password = models.CharField(db_column='INDIV_PASSWORD', max_length=2000)
    mangue_id = models.IntegerField(db_column='MANGUE_ID')
    etat_id = models.IntegerField(max_length=1, db_column='ETAT_ID')


Int_Individu (Pour les titulaires) bdd ied
  * nom
  * prenom1
  * prenom2
  * date de naissance
  * Adresse (FK)

Adresse
  Modele apogee ou dsi







##################################################
class Personne(models.Model):
    GENDER_CHOICES = (
        ('M', 'Homme'), ('F', 'Femme'),
    )
    last_name = models.CharField(u"Nom patronymique", max_length=30, null=True)
    common_name = models.CharField(u"Nom d'époux", max_length=30, null=True, blank=True)
    first_name1 = models.CharField(u"Prénom", max_length=30)
    first_name2 = models.CharField(u"Deuxième prénom", max_length=30, null=True, blank=True)
    first_name3 = models.CharField(u"Troisième prénom", max_length=30, null=True, blank=True)
    personal_email = models.EmailField("Email", unique=True, null=True)
    date_registration_current_year = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(u'sexe', max_length=1, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField('date de naissance', null=True)
    categorie = models.ForeignKey(CategoriePersonne, null=True, blank=True)  # ! IMPORTQNT
