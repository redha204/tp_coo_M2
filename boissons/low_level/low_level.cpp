#include <cpr/cpr.h>
#include <iostream>
#include <memory>
#include <optional>
#include <vector>
#include <nlohmann/json.hpp>

using namespace std;
using json = nlohmann::json;

// Forward declarations
class Localisation;
class Energie;
class DebitEnergie;
class Local;
class Produit;
class MatierePremiere;
class QuantiteMatierePremiere;
class UtilisationMatierePremiere;
class ApprovisionnementMatierePremiere;
class Metier;
class RessourceHumaine;
class Machine;
class Fabrication;

// Classes de base sans dépendances
class MatierePremiere {
protected:
    int id;
    string nom;
    int stock;
    int emprise;

public:
    MatierePremiere(int i, string n, int s, int e) 
        : id(i), nom(n), stock(s), emprise(e) {}
    
    MatierePremiere(const json& data)
        : id(data["id"]), nom(data["nom"]), 
          stock(data["stock"]), emprise(data["emprise"]) {}
    
    MatierePremiere(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/matiere-premiere/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->nom = data["nom"];
        this->stock = data["stock"];
        this->emprise = data["emprise"];
    }
    
    void affichage() const {
        cout << "MatierePremiere[" << id << "]: " << nom 
             << ", stock=" << stock << ", emprise=" << emprise << endl;
    }
    
    int getId() const { return id; }
    string getNom() const { return nom; }
};

class Metier {
protected:
    int id;
    string nom;
    int remuneration;

public:
    Metier(int i, string n, int r) 
        : id(i), nom(n), remuneration(r) {}
    
    Metier(const json& data)
        : id(data["id"]), nom(data["nom"]), 
          remuneration(data["remuneration"]) {}
    
    Metier(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/metier/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->nom = data["nom"];
        this->remuneration = data["remuneration"];
    }
    
    void affichage() const {
        cout << "Metier[" << id << "]: " << nom 
             << ", remuneration=" << remuneration << endl;
    }
    
    int getId() const { return id; }
};

class Localisation {
protected:
    int id;
    string nom;
    int taxes;
    int prix_m2;

public:
    Localisation(int i, string n, int t, int p) 
        : id(i), nom(n), taxes(t), prix_m2(p) {}
    
    Localisation(const json& data)
        : id(data["id"]), nom(data["nom"]), 
          taxes(data["taxes"]), prix_m2(data["prix_m2"]) {}
    
    Localisation(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/localisation/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->nom = data["nom"];
        this->taxes = data["taxes"];
        this->prix_m2 = data["prix_m2"];
    }
    
    void affichage() const {
        cout << "Localisation[" << id << "]: " << nom 
             << ", taxes=" << taxes << ", prix_m2=" << prix_m2 << endl;
    }
    
    int getId() const { return id; }
};

class Energie {
protected:
    int id;
    string nom;
    int prix;
    unique_ptr<Localisation> localisation;

public:
    Energie(int i, string n, int p, unique_ptr<Localisation> loc)
        : id(i), nom(n), prix(p), localisation(move(loc)) {}
    
    Energie(const json& data)
        : id(data["id"]), nom(data["nom"]), prix(data["prix"]),
          localisation(make_unique<Localisation>(data["localisation_id"])) {}
    
    Energie(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/energie/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->nom = data["nom"];
        this->prix = data["prix"];
        this->localisation = make_unique<Localisation>(data["localisation_id"]);
    }
    
    void affichage() const {
        cout << "Energie[" << id << "]: " << nom << ", prix=" << prix << endl;
        if (localisation) {
            cout << "  Localisation: ";
            localisation->affichage();
        }
    }
};

class DebitEnergie {
protected:
    int id;
    int debit;
    unique_ptr<Energie> energie;

public:
    DebitEnergie(int i, int d, unique_ptr<Energie> e)
        : id(i), debit(d), energie(move(e)) {}
    
    DebitEnergie(const json& data)
        : id(data["id"]), debit(data["debit"]),
          energie(make_unique<Energie>(data["energie_id"])) {}
    
    DebitEnergie(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/debit-energie/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->debit = data["debit"];
        this->energie = make_unique<Energie>(data["energie_id"]);
    }
    
    void affichage() const {
        cout << "DebitEnergie[" << id << "]: debit=" << debit << endl;
        if (energie) {
            cout << "  ";
            energie->affichage();
        }
    }
};

class Local {
protected:
    int id;
    string nom;
    unique_ptr<Localisation> localisation;
    int surface;

public:
    Local(int i, string n, unique_ptr<Localisation> loc, int s)
        : id(i), nom(n), localisation(move(loc)), surface(s) {}
    
    Local(const json& data)
        : id(data["id"]), nom(data["nom"]), surface(data["surface"]),
          localisation(make_unique<Localisation>(data["localisation_id"])) {}
    
    Local(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/local/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->nom = data["nom"];
        this->surface = data["surface"];
        this->localisation = make_unique<Localisation>(data["localisation_id"]);
    }
    
    void affichage() const {
        cout << "Local[" << id << "]: " << nom << ", surface=" << surface << endl;
        if (localisation) {
            cout << "  ";
            localisation->affichage();
        }
    }
    
    int getId() const { return id; }
};

class Produit {
protected:
    int id;
    string nom;
    int prix_de_vente;
    int quantite;
    int emprise;
    unique_ptr<Local> local;

public:
    Produit(int i, string n, int pdv, int q, int e, unique_ptr<Local> l)
        : id(i), nom(n), prix_de_vente(pdv), quantite(q), emprise(e), local(move(l)) {}
    
    Produit(const json& data)
        : id(data["id"]), nom(data["nom"]), prix_de_vente(data["prix_de_vente"]),
          quantite(data["quantite"]), emprise(data["emprise"]),
          local(make_unique<Local>(data["local_id"])) {}
    
    Produit(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/produit/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->nom = data["nom"];
        this->prix_de_vente = data["prix_de_vente"];
        this->quantite = data["quantite"];
        this->emprise = data["emprise"];
        this->local = make_unique<Local>(data["local_id"]);
    }
    
    void affichage() const {
        cout << "Produit[" << id << "]: " << nom << ", prix=" << prix_de_vente 
             << ", quantite=" << quantite << endl;
    }
    
    int getId() const { return id; }
};

class QuantiteMatierePremiere {
protected:
    int id;
    int quantite;
    unique_ptr<MatierePremiere> matiere_premiere;

public:
    QuantiteMatierePremiere(int i, int q, unique_ptr<MatierePremiere> mp)
        : id(i), quantite(q), matiere_premiere(move(mp)) {}
    
    virtual void affichage() const {
        cout << "QuantiteMatierePremiere[" << id << "]: quantite=" << quantite << endl;
        if (matiere_premiere) {
            cout << "  ";
            matiere_premiere->affichage();
        }
    }
    
    virtual ~QuantiteMatierePremiere() = default;
};

class UtilisationMatierePremiere : public QuantiteMatierePremiere {
public:
    using QuantiteMatierePremiere::QuantiteMatierePremiere;
    
    UtilisationMatierePremiere(const json& data)
        : QuantiteMatierePremiere(
            data["id"], 
            data["quantite"],
            make_unique<MatierePremiere>(data["matiere_premiere_id"])
        ) {}
    
    UtilisationMatierePremiere(int id) 
        : QuantiteMatierePremiere(0, 0, nullptr) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/utilisation-matiere-premiere/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->quantite = data["quantite"];
        this->matiere_premiere = make_unique<MatierePremiere>(data["matiere_premiere_id"]);
    }
};

class ApprovisionnementMatierePremiere : public QuantiteMatierePremiere {
protected:
    unique_ptr<Localisation> localisation;
    int prix_unitaire;
    int delais;

public:
    ApprovisionnementMatierePremiere(int i, int q, unique_ptr<MatierePremiere> mp,
                                      unique_ptr<Localisation> loc, int pu, int d)
        : QuantiteMatierePremiere(i, q, move(mp)),
          localisation(move(loc)), prix_unitaire(pu), delais(d) {}
    
    ApprovisionnementMatierePremiere(const json& data)
        : QuantiteMatierePremiere(
            data["id"], 
            data["quantite"],
            make_unique<MatierePremiere>(data["matiere_premiere_id"])
        ),
          localisation(make_unique<Localisation>(data["localisation_id"])),
          prix_unitaire(data["prix_unitaire"]),
          delais(data["delais"]) {}
    
    ApprovisionnementMatierePremiere(int id)
        : QuantiteMatierePremiere(0, 0, nullptr), localisation(nullptr), prix_unitaire(0), delais(0) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/approvisionnement-matiere-premiere/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->quantite = data["quantite"];
        this->matiere_premiere = make_unique<MatierePremiere>(data["matiere_premiere_id"]);
        this->localisation = make_unique<Localisation>(data["localisation_id"]);
        this->prix_unitaire = data["prix_unitaire"];
        this->delais = data["delais"];
    }
    
    void affichage() const override {
        cout << "ApprovisionnementMatierePremiere[" << id << "]: prix_unitaire=" 
             << prix_unitaire << ", delais=" << delais << endl;
    }
};

class RessourceHumaine {
protected:
    int id;
    unique_ptr<Metier> metier;
    int quantite;

public:
    RessourceHumaine(int i, unique_ptr<Metier> m, int q)
        : id(i), metier(move(m)), quantite(q) {}
    
    RessourceHumaine(const json& data)
        : id(data["id"]), quantite(data["quantite"]),
          metier(make_unique<Metier>(data["metier_id"])) {}
    
    RessourceHumaine(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/ressource-humaine/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->quantite = data["quantite"];
        this->metier = make_unique<Metier>(data["metier_id"]);
    }
    
    void affichage() const {
        cout << "RessourceHumaine[" << id << "]: quantite=" << quantite << endl;
        if (metier) {
            cout << "  ";
            metier->affichage();
        }
    }
};

class Machine {
protected:
    int id;
    string nom;
    int prix_achat;
    int cout_maintenance;
    vector<unique_ptr<Metier>> operateurs;
    int debit;
    int surface;
    int debit_energie;
    int taux_utilisation;
    unique_ptr<Local> local;

public:
    Machine(int i, string n, int pa, int cm, int d, int s, int de, int tu, unique_ptr<Local> l)
        : id(i), nom(n), prix_achat(pa), cout_maintenance(cm), 
          debit(d), surface(s), debit_energie(de), taux_utilisation(tu), local(move(l)) {}
    
    Machine(const json& data)
        : id(data["id"]), nom(data.value("nom", "")), prix_achat(data["prix_achat"]),
          cout_maintenance(data["cout_maintenance"]), debit(data.value("debit", 0)),
          surface(data["surface"]), debit_energie(data.value("debit_energie", 0)),
          taux_utilisation(data["taux_utilisation"]),
          local(make_unique<Local>(data["local_id"])) {
        if (data.contains("operateurs_details")) {
            for (const auto& op : data["operateurs_details"]) {
                operateurs.push_back(make_unique<Metier>(op));
            }
        }
    }
    
    Machine(int id) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/machine/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->nom = data.value("nom", "");
        this->prix_achat = data["prix_achat"];
        this->cout_maintenance = data["cout_maintenance"];
        this->debit = data.value("debit", 0);
        this->surface = data["surface"];
        this->debit_energie = data.value("debit_energie", 0);
        this->taux_utilisation = data["taux_utilisation"];
        this->local = make_unique<Local>(data["local_id"]);
    }
    
    void affichage() const {
        cout << "Machine[" << id << "]: " << nom << ", prix_achat=" << prix_achat 
             << ", cout_maintenance=" << cout_maintenance << endl;
    }
};

class Fabrication {
protected:
    int id;
    unique_ptr<Produit> produit;
    vector<unique_ptr<UtilisationMatierePremiere>> utilisations_matiere_premiere;
    vector<unique_ptr<Machine>> machines;
    vector<unique_ptr<RessourceHumaine>> ressources_humaines;

public:
    Fabrication(int i, unique_ptr<Produit> p)
        : id(i), produit(move(p)) {}
    
    Fabrication(const json& data)
        : id(data["id"]), produit(make_unique<Produit>(data["produit"])) {
        if (data.contains("utilisations_matiere_premiere")) {
            for (const auto& ump : data["utilisations_matiere_premiere"]) {
                utilisations_matiere_premiere.push_back(
                    make_unique<UtilisationMatierePremiere>(ump)
                );
            }
        }
        if (data.contains("machines")) {
            for (const auto& m : data["machines"]) {
                machines.push_back(make_unique<Machine>(m));
            }
        }
        if (data.contains("ressources_humaines")) {
            for (const auto& rh : data["ressources_humaines"]) {
                ressources_humaines.push_back(make_unique<RessourceHumaine>(rh));
            }
        }
    }
    
    Fabrication(int id) : id(id), produit(nullptr) {
        cpr::Response r = cpr::Get(
            cpr::Url{"http://localhost:8000/api/fabrication/" + to_string(id) + "/"}
        );
        json data = json::parse(r.text);
        this->id = data["id"];
        this->produit = make_unique<Produit>(data["produit"]);
    }
    
    void affichage() const {
        cout << "Fabrication[" << id << "]" << endl;
        if (produit) {
            cout << "  ";
            produit->affichage();
        }
    }
};
int main() {
    cout << "=== Test 1: Localisation ===" << endl;
    Localisation loc(1);
    loc.affichage();
    
    cout << "\n=== Test 2: DebitEnergie ===" << endl;
    DebitEnergie debit(1);
    debit.affichage();
    
    cout << "\n=== Test 3: Local ===" << endl;
    Local local(1);
    local.affichage();
    
    return 0;
}
