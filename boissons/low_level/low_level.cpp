#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>
using namespace std;
class Localisation {
private:
  string nom;
  double taxes;
  double prix_m2;

public:
  Localisation(string n, double t, double p) {
    nom = n;
    taxes = t;
    prix_m2 = p;
  }
  void affichage() {
    cout << "Nom: " << nom << ", Taxes: " << taxes << ", Prix_m2: " << prix_m2
         << endl;
  }
};
using json = nlohmann::json;
int main() {

  Localisation loc("seddouk", 19.6, 200);
  loc.affichage();
  cpr::Response r =
      cpr::Get(cpr::Url{"http://localhost:8000/api/debit-energie/1/"},
               cpr::Authentication{"user", "pass", cpr::AuthMode::BASIC},
               cpr::Parameters{{"anon", "true"}, {"key", "value"}});

  cout << "Status: " << r.status_code << endl;
  cout << "Content-Type: " << r.header["content-type"] << endl;
  cout << "Body: " << r.text << endl;
  json data = json::parse(r.text);
  return 0;
}
