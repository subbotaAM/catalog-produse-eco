from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["EcoCatalogRM"]
produse = db["produse"]


def afiseaza_produse():
    print("\n--- Lista tuturor produselor ECO ---")

    lista = list(produse.find())

    if len(lista) == 0:
        print("Nu există produse în colecție.")
        return

    for produs in lista:
        print(
            produs.get("numeProdus", "Fără nume"),
            "-",
            produs.get("categorie", "Fără categorie"),
            "-",
            produs.get("pret", 0),
            produs.get("moneda", "MDL")
        )


def cauta_produs():
    print("\n--- Căutare produs după nume ---")

    nume = input("Introdu numele produsului: ")

    rezultat = produse.find_one({"numeProdus": nume})

    if rezultat:
        print("\nProdus găsit:")
        print("Nume:", rezultat.get("numeProdus"))
        print("Categorie:", rezultat.get("categorie"))
        print("Preț:", rezultat.get("pret"), rezultat.get("moneda", "MDL"))
        print("Stoc:", rezultat.get("stoc"))
        print("Rating:", rezultat.get("ratingMediu"))

        producator = rezultat.get("producator", {})
        print("Producător:", producator.get("denumire", "Necunoscut"))
        print("Localitate:", producator.get("localitate", "Necunoscută"))
    else:
        print("Produsul nu a fost găsit.")


def filtreaza_dupa_categorie():
    print("\n--- Filtrare produse după categorie ---")

    categorie = input("Introdu categoria: ")

    rezultate = list(produse.find({"categorie": categorie}))

    if len(rezultate) == 0:
        print("Nu există produse în această categorie.")
        return

    for produs in rezultate:
        print(
            produs.get("numeProdus"),
            "-",
            produs.get("pret"),
            produs.get("moneda", "MDL")
        )


def adauga_produs():
    print("\n--- Adăugare produs nou ---")

    nume = input("Nume produs: ")
    categorie = input("Categorie: ")
    pret = float(input("Preț: "))
    stoc = int(input("Stoc: "))
    producator = input("Denumire producător: ")
    localitate = input("Localitate producător: ")

    produs_nou = {
        "numeProdus": nume,
        "categorie": categorie,
        "pret": pret,
        "moneda": "MDL",
        "stoc": stoc,
        "producator": {
            "denumire": producator,
            "localitate": localitate
        },
        "ecoTags": ["eco", "local"],
        "ratingMediu": 0
    }

    produse.insert_one(produs_nou)

    print("Produsul a fost adăugat cu succes.")


def actualizeaza_pret():
    print("\n--- Actualizare preț produs ---")

    nume = input("Introdu numele produsului: ")
    pret_nou = float(input("Introdu prețul nou: "))

    rezultat = produse.update_one(
        {"numeProdus": nume},
        {"$set": {"pret": pret_nou}}
    )

    if rezultat.modified_count > 0:
        print("Prețul produsului a fost actualizat.")
    else:
        print("Produsul nu a fost găsit sau prețul este deja același.")


def sterge_produs():
    print("\n--- Ștergere produs ---")

    nume = input("Introdu numele produsului de șters: ")

    confirmare = input("Ești sigur că vrei să ștergi acest produs? da/nu: ")

    if confirmare.lower() != "da":
        print("Ștergerea a fost anulată.")
        return

    rezultat = produse.delete_one({"numeProdus": nume})

    if rezultat.deleted_count > 0:
        print("Produsul a fost șters.")
    else:
        print("Produsul nu a fost găsit.")


def sorteaza_dupa_pret():
    print("\n--- Produse sortate după preț crescător ---")

    for produs in produse.find().sort("pret", 1):
        print(
            produs.get("numeProdus"),
            "-",
            produs.get("pret"),
            produs.get("moneda", "MDL")
        )


def produse_pret_sub_100():
    print("\n--- Produse cu preț mai mic sau egal cu 100 MDL ---")

    rezultate = list(produse.find({"pret": {"$lte": 100}}))

    if len(rezultate) == 0:
        print("Nu există produse cu preț mai mic sau egal cu 100 MDL.")
        return

    for produs in rezultate:
        print(
            produs.get("numeProdus"),
            "-",
            produs.get("pret"),
            produs.get("moneda", "MDL")
        )


def statistica_pe_categorii():
    print("\n--- Statistică pe categorii ---")

    pipeline = [
        {
            "$group": {
                "_id": "$categorie",
                "numarProduse": {"$sum": 1},
                "pretMediu": {"$avg": "$pret"},
                "ratingMediuCategorie": {"$avg": "$ratingMediu"}
            }
        },
        {
            "$sort": {"numarProduse": -1}
        }
    ]

    rezultate = list(produse.aggregate(pipeline))

    if len(rezultate) == 0:
        print("Nu există date pentru statistică.")
        return

    for rezultat in rezultate:
        print("Categorie:", rezultat["_id"])
        print("Număr produse:", rezultat["numarProduse"])
        print("Preț mediu:", round(rezultat["pretMediu"], 2), "MDL")
        print("Rating mediu:", round(rezultat["ratingMediuCategorie"], 2))
        print("-----------------------------")


def meniu():
    while True:
        print("\n========== EcoCatalog RM ==========")
        print("1. Afișează toate produsele")
        print("2. Caută produs după nume")
        print("3. Filtrează produse după categorie")
        print("4. Adaugă produs nou")
        print("5. Actualizează prețul unui produs")
        print("6. Șterge produs")
        print("7. Sortează produsele după preț")
        print("8. Afișează produse cu preț <= 100 MDL")
        print("9. Statistică pe categorii")
        print("0. Ieșire")

        optiune = input("Alege opțiunea: ")

        if optiune == "1":
            afiseaza_produse()
        elif optiune == "2":
            cauta_produs()
        elif optiune == "3":
            filtreaza_dupa_categorie()
        elif optiune == "4":
            adauga_produs()
        elif optiune == "5":
            actualizeaza_pret()
        elif optiune == "6":
            sterge_produs()
        elif optiune == "7":
            sorteaza_dupa_pret()
        elif optiune == "8":
            produse_pret_sub_100()
        elif optiune == "9":
            statistica_pe_categorii()
        elif optiune == "0":
            print("Programul s-a închis.")
            break
        else:
            print("Opțiune invalidă. Încearcă din nou.")

meniu()