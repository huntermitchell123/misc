#include "header.h"

void print_game_rules(void) {
	printf("A player rolls two dice. Each die has six faces. These faces contain 1, 2, 3, 4, 5, and 6 spots. After the dice have come to rest, the sum of the spots on the two upward faces is calculated. If the sum is 7 or 11 on the first throw, the player wins. If the sum is 2, 3, or 12 on the first throw (called \"craps\"), the player loses(i.e.the \"house\" wins). If the sum is 4, 5, 6, 8, 9, or 10 on the first throw, then the sum becomes the player's \"point.\" To win, you must continue rolling the dice until you \"make your point.\" The player loses by rolling a 7 before making the point.\n");
}

double get_bank_balance(void) {
	double balance = 0;
	printf("What is your starting bank balance?\n");
	scanf("%lf", &balance);
	return balance;
}

double get_wager_amount(void) {
	double wager;
	printf("How much would you like to wager this round?\n");
	scanf("%lf", &wager);
	return wager;
}

int check_wager_amount(double wager, double balance) {
	if (wager <= balance) {
		return 1;
	}
	else {
		return 0;
	}
}

int roll_die(void) { 
	return (rand() % 6) + 1;
}

int calculate_sum_dice(int die1_value, int die2_value) {
	return die1_value + die2_value;
}

int is_win_loss_or_point(int sum_dice) {
	if (sum_dice == 7 || sum_dice == 11) {
		return 1;
	}
	else if (sum_dice == 2 || sum_dice == 3 || sum_dice == 12) {
		return 0;
	}
	else {
		return -1;
	}
}

int is_point_loss_or_neither(int sum_dice, int point_value) {
	if (sum_dice == point_value) {
		return 1;
	}
	else if (sum_dice == 7) {
		return 0;
	}
	else {
		return -1;
	}
}

double adjust_bank_balance(double bank_balance, double wager_amount, int add_or_subtract) {
	if (add_or_subtract == 1) {
		bank_balance = bank_balance + wager_amount;
	}
	else if (add_or_subtract == 0) {
		bank_balance = bank_balance - wager_amount;
	}
	else {

	}
	return bank_balance;
}

void chatter_messages(int number_rolls, int win_loss_neither, double initial_bank_balance, double current_bank_balance) {
	if (win_loss_neither == 1) {
		printf("You won this roll!\n");
	}
	else if (win_loss_neither == 0) {
		printf("Aw shit you lost cuh!\n");
	}
	else if (win_loss_neither == -1) {
		printf("The sum became your \"point\"!\n");
	}
	else {

	}
}