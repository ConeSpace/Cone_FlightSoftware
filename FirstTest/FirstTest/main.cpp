#include <wiringPi.h>
#include <iostream>
#include <cstdio>
#include <stdio.h>

/*
This Script is to provide a testing base for components. It may also be used for debugging.

22-12-2018
V0.1
Sebastian Dohnal
*/

int main(void)
{

	//Setup
	wiringPiSetup();

	//Enter testing loop
	while (true) {
		//Ask for Test Code
		std::cout << "Enter the Test-Code:" << std::endl;
		int TestCode = 000;
		std::cin >> TestCode;
		//Test Code saved as int TestCode


		//Check if Testcode matches test script and if yes run this script

		if (TestCode == 001) {
			//Test Script for Test Code 001
			//Name: Hello World
			//Desccription: Prints "Hello World" every second

			while (true) {
				std::cout << "Hello World!" << std::endl;
				delayMicroseconds(1000000);
			}
		}
		else if (TestCode == 002) {
			//Test Script for Test Code 002
			//Name: Status LED Blink
			//Desccription: Makes LED Blink every second

			pinMode(7, OUTPUT);

			while (true) {

				printf("LED ON\n");
				digitalWrite(7, 1);
				delay(1000);
				printf("LED OFF\n");
				digitalWrite(7, 0);
				delay(1000);

			}

		} else {
			//No matching Test Code found
			std::cout << "ERROR: Unknown Test-Code" << std::endl;
		}
	}
	return 0;
}