# Rover Map Generator

Randomly generates maps for Assignment 1, CSCI 561. **This doesn't solve the problem, it just creates one (or multiple)**.

## How does it work?

The auspices of `numpy.random` and PNG libraries

## How do I make it work?

* Clone the repository
* Install the required dependencies `numpy` `Pillow` `pypng`
* Run `testcasegen.py` and follow the instructions
* `input_gen` is the appropriate input file.

## I want MOAR test cases

This will automate the entire stack, including execution and require some work from your end. Do the following:

* Interface your work so that it works with `tcgen.py` and `executeAlgorithm` works. Please remember not to use your original homework file for this. You will be making (almost) irreversible changes that will bite you in the end.
* Run `tcgen.py` and follow the instructions.
* Grab a coffee or go for a walk.

## Is this enabling plagiarism?

* This code does NOTHING that is a part of the assignment. This is simply a wrapper that allows you to visualize your inputs and outputs.
* No test cases are shared/stored in a common location! Please don't show off your amazing solve to anybody.

## But how does it run the agorithm?

* It doesn't. It acts like a SBI employee and only defers execution to whatever monstrosity you might have built. The code is yours, the execution is yours, and this only acts as a display mechanism.