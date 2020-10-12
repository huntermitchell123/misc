/**************************************
Programmer: Hunter Mitchell
Section and Class: 5 and CptS 121
Date: 2/22/17
Amount of Swag: not enough i guess
Program Description: Does the game craps
***************************************/

#include "header.h"

int main(void) {

	double bank_balance = 0, wager; //declaring doubles
	int answer = 0, answer2 = 1, roll1, roll2, sum, outcome, outcome2, point_value = 0; //declaring integers

	srand((unsigned int)time(NULL)); //time

	print_game_rules();
	printf("\n");
	
	while (answer != 2) { //will stop once the player doesnt want to play

		printf("Would you like to play craps?\n");
		printf("1. Yes\n");
		printf("2. No\n");
		scanf("%d", &answer);
		printf("\n");

		if (answer == 1) { //player wants to play

			answer2 = 1; //setting this in case they already backed out
			bank_balance = get_bank_balance(); //getting bank balance
			printf("Your bank balance is: %lf\n", bank_balance); 

			while (bank_balance != 0.0 && answer2 == 1) { //continue again if not broke and still wants to play

				if (point_value != 0 && answer2 == 1) { //if player already has a point

					roll1 = roll_die();
					roll2 = roll_die();
					printf("The dice roll: %d %d\n", roll1, roll2); //dice rolls
					sum = calculate_sum_dice(roll1, roll2);
					printf("The sum is: %d\n\n", sum);
					outcome2 = is_point_loss_or_neither(sum, point_value); //determining outcome
					bank_balance = adjust_bank_balance(bank_balance, wager, outcome2);//changing bank balance

					if (outcome2 == 1) { //rolled point

						printf("You made your point!\n");

					} else if (outcome2 == 0) { //rolled a 7

						printf("You lost!\n");

					} else {

						printf("Roll again!\n");

					}
					
					if (outcome2 != -1) { //if rolled point or 7

						point_value = 0;
						printf("Your bank balance is now: %lf\n\n", bank_balance);

						if (bank_balance != 0.0) { //making sure player isnt broke

							printf("Would you like to keep playing?\n");
							printf("1. Yes\n");
							printf("2. No\n");
							scanf("%d", &answer2);
							printf("\n");

						} else {

							printf("You are all out of money!\n\n");

						}
					}
				}

				if (point_value == 0 && answer2 == 1 && bank_balance != 0.0) { //if player doesnt have a point value and wants to play

					wager = get_wager_amount(); //asking for wager for the round
					printf("You are wagering %lf\n\n", wager);

					if (check_wager_amount(wager, bank_balance) == 1) { //making sure wager is less than balance

						roll1 = roll_die();
						roll2 = roll_die();
						printf("The dice roll: %d %d\n", roll1, roll2); //rolling dice
						sum = calculate_sum_dice(roll1, roll2);
						printf("The sum is: %d\n\n", sum);
						outcome = is_win_loss_or_point(sum); //figuring outcome
						bank_balance = adjust_bank_balance(bank_balance, wager, outcome); //changing balance

						if (outcome == 1) { //win

							printf("You won!\n");

						} else if (outcome == 0) { //lose

							printf("You lost!\n");

						} else { //point!

							point_value = sum;
							printf("Your point value is now %d\n\n", point_value);

						}

						if (outcome != -1) { //if its not a point

							printf("Your bank balance is now: %lf\n\n", bank_balance);

							if (bank_balance != 0.0) { //making sure player isnt broke

								printf("Would you like to keep playing?\n");
								printf("1. Yes\n");
								printf("2. No\n");
								scanf("%d", &answer2);
								printf("\n");

							} else {

								printf("You are all out of money!\n\n");

							}
						}

					} else if (check_wager_amount(wager, bank_balance) == 0) { //uh oh! wager is too high

						printf("Your wager is more than your bank you dumb idiot\n");

					}
				}
			}
		}
	} 
	printf("Goodbye then...\n"); //if player doesnt wanna play
	return 0;
}