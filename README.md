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
pip install pharmacokinetics
```
## Usage

The models are called `iv_one_compartment`, `iv_two_compartments`, and `subcutaneous`.
(Section here to be added when main usage established)

## See also
For further discussion of the mathematics behind this model, see [here](https://sabs-r3.github.io/software-engineering-projects/01-introduction/index.html).

## Authors and acknowledgment
The authors are Kallista Angeloff, Shirin Ermis, and Justin Leung. Particular thanks also to Simon Marchant for debugging.
## License
[MIT](https://choosealicense.com/licenses/mit/)
