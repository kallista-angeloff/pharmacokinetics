# Pharmacokinetics
Pharmacokinetics is a Python package for visualising simplified drug delivery methods 
and protocols.
## Overview
This package contains representations of three models:
### Single-compartment intravenous model
This model represents the body as a single compartment into which the drug is delivered 
and from which it is cleared.
### Multi-compartment intravenous model
This model represents the body as a main compartment into which the drug is delivered
and a number of peripheral compartments which exchange diffusively with the main compartment.
Clearance is represented as occurring only from the main compartment.
### Multi-component subcutaneous model
This model represents the body as a dosing compartment into which the drug is initially delivered
before reaching a main compartment, and a number of peripheral compartments which exchange 
diffusively with the main compartment. Clearance is represented as occurring only from the main 
compartment.

Each model can be run with a custom dosing protocol.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Pharmacokinetics.

```bash
pip install pkmodel
```
If this does not work, download the source folder into the desired directory and run:

```bash
pip install -e .
```

## Usage

Open and run `main.py`. The following prompts will occur:
```
How many models do you want to run?
Enter a whole number: 
```
After selecting the number of models:
```
Should a continous dosis be used? 
y/n? 
```
After selecting the dosing protocol:
```
What should the amount of dosis be in ng? 
Type a number larger than 0. 
```
After selecting the size of the dose:
```
How many spikes should there be in the dosis? 
Enter an integer between 1 and 10.
```
(This refers to the number of discrete doses of the original amount entered.)
After selecting the number of discrete doses:
```
How many compartments including the central one should there be? 
Enter an integer between 1 and 3.
```
After selecting the total number of compartments:
```
Should a dosing compartment be used? 
y/n?
```
(This refers to the initial dosing compartment used in a subcutaneous model.)

The model will attempt to run with these parameters and notify if successful:

```
The solver successfully reached the end of the integration interval.
```
A plot of the output will be available in a folder called `data`, created one level up from
`pkmodel`. Each run will be identified by its timestamp.

## See also
Sphinx auto-generated documentation is available one directory up in the `docs` folder. For further discussion of the mathematics behind this model, see [here](https://sabs-r3.github.io/software-engineering-projects/01-introduction/index.html).

## Authors and acknowledgment
The authors are Kallista Angeloff, Shirin Ermis, and Justin Leung. Particular thanks also to Simon Marchant for debugging.
## License
[MIT](https://choosealicense.com/licenses/mit/)
