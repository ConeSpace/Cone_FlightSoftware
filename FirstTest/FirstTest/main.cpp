#include <wiringPi.h>
#include <iostream>

using namespace std;
// LED-PIN - wiringPi-PIN 0 ist BCM_GPIO 17.
// Wir müssen bei der Initialisierung mit wiringPiSetupSys die BCM-Nummerierung verwenden.
// Wenn Sie eine andere PIN-Nummer wählen, verwenden Sie die BCM-Nummerierung, und
// aktualisieren Sie die Eigenschaftenseiten – Buildereignisse – Remote-Postbuildereignisbefehl 
// der den GPIO-Export für die Einrichtung für wiringPiSetupSys verwendet.
#define	LED	17

int main(void)
{
	//wiringPiSetupSys();

	//pinMode(LED, OUTPUT);

	cout << "Hello world\n";
	
	return 0;
}