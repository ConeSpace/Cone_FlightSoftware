#include <wiringPi.h>
#include <iostream>
#include <cstdio>
#include <stdio.h>
#include <wiringSerial.h>
#include <string.h>

/*
This Script is to provide a testing base for components. It may also be used for debugging.

28-12-2018
V0.2
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

		} else if (TestCode == 003) {
			//Test Script for Test Code 003
			//Name: Status Button
			//Desccription: Prints 1 if Button is pressed

			pinMode(7, INPUT);

			while (true) {

				

			}

		}
		else if (TestCode == 004) {
			//Test Script for Test Code 004
			//Name: Transmit
			//Desccription: Transmitts "Hello World" every second
			//
			//Pin Layout 
			//8-TXD
			//10-RXD
			//16-M0
			//18-M1

			printf("TestCode 004 initializing...\n");


			pinMode(4, OUTPUT);
			pinMode(5, OUTPUT);
			printf("Outputs set...");

			int fd;
			int count;
			if (wiringPiSetup() < 0)return 1;
			if ((fd = serialOpen("/dev/serial0", 9600)) < 0)return 1;
			printf("serial test start ...\n");
			serialPrintf(fd, "Hello World!");
			count++;
			printf("Sucessfull!");
			while (true) {
				serialPrintf(fd, "Hello World!");
				printf("Transmitting...\n");
				count++;
				delay(1000);

			}



		}
		else if (TestCode == 005) {
			//Test Script for Test Code 005
			//Name: Receive
			//Desccription: Receives Data and prints it
			//
			//Pin Layout 
			//8-TXD
			//10-RXD
			//16-M0
			//18-M1

			printf("TestCode 005 initializing...\n");


			pinMode(4, OUTPUT);
			pinMode(5, OUTPUT);
			printf("Outputs set...");

			
			int fd;
			if (wiringPiSetup() < 0)return 1;
			if ((fd = serialOpen("/dev/serial0", 9600)) < 0)return 1;
			printf("serial test start ...\n");
			serialPrintf(fd, "Hello World!");
			printf("Sucessfull!");
			while (true) {
				putchar(serialGetchar(fd));
				delay(1);
			}
			


		}
		else {
			//No matching Test Code found
			std::cout << "ERROR: Unknown Test-Code" << std::endl;
		}
	}
	return 0;
}