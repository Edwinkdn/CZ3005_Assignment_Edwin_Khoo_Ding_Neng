:-dynamic like/1.
:-dynamic dislike/1.
:-dynamic history/1.

ask(slides, 0).
/* Ask for an item that is related to the liked item first before going to a random
 	 item, but make sure you don't ask a previously asked question. */
ask(X,Y):-
	like(Y), related(X,Y), \+ history(X).
ask(X,Y):-
	random(X), \+ related(X,Y), \+ history(X).
ask(X,Y):-
	random(X), \+ history(X).

/* Determines if X is part of a list */
member(X,[X|_]).
member(X,[_|R]) :- member(X,R).

/* Adds element to a list */
append([A | B], C, [A | D]) :- append(B, C, D).
append([], A, A).

/* Define relationships of two different items */
related(X,Y) :-
	play(L), member(X, L), member(Y, L);
	eat(L), member(X, L), member(Y, L);
	do(L), member(X, L), member(Y, L);
	see(L), member(X, L), member(Y, L);
	learn(L), member(X, L), member(Y, L).

/* Define the relationship between a member of each list and their followup question */
followup(X, Y) :-
	play(L), member(X, L), play_followup(H), member(Y,H);
	eat(L), member(X, L), eat_followup(H), member(Y,H);
	do(L), member(X, L), do_followup(H), member(Y,H);
	see(L), member(X, L), see_followup(H), member(Y,H);
	learn(L), member(X, L), learn_followup(H), member(Y,H).

/* Create the random list */

random(X) :-
	play(L), member(X, L);
	eat(L), member(X, L);
	do(L), member(X, L);
	see(L), member(X, L);
	learn(L), member(X, L).

/* Create the list of items for each category */
play([basketball, slides, toys, legos, soccer, playdoh, trains, catching, sandbox, computer]).
eat([candy, choclate, cake, toffee, sandwich, pizza, veggies, fries, burger,soup]).
do([building, cooking, painting, singing, drawing]).
see([cartoons, spiders, alphabet, artwork, cat, dog]).
learn([math, science, instruments, shapes, colours]).

/* Keep a list of standard followup questions for each category */
play_followup([have_fun, enjoy_yourself, play_with_friends]).
eat_followup([find_it_yummy, eat_alot, wash_your_hands_before_you_eat]).
do_followup([enjoy_yourself, think_you_could_do_more, do_it_with_your_friends]).
see_followup([find_it_cool, share_with_the_class]).
learn_followup([learn_as_much_as_you_can, think_you_want_to_learn_more]).


/* Initialize the like, dislike, and history */
like(nothing).
dislike(nothing).
history(nothing).
a.
