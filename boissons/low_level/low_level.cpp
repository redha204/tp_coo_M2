#include <iostream>
#include <string>
using namespace std ;

class Localisation
{ 
    private : 

    char nom; 
    float taxes; 
    float prix_m2;
    
    public :
Localisation(float tax ,float prixm2,char ismis)
{
    this.nom=ismis;
    this.taxes=prix_m2;
    this.prix_m2=prixm2;
}

}