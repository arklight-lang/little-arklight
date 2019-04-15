# Little Arklight - a circuit based programming language

[![License](https://img.shields.io/badge/LICENSE-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Unitary Fund](https://img.shields.io/badge/Supported%20by-Unitary%20Fund-brightgreen.svg?style=for-the-badge)](http://unitary.fund)

Quantum computing heralds a new era of computing and promises algorithms that will help solve problems that classical computing is not able to handle currently.
But teaching quantum computing has proven a challenge for multiple reasons least of which is the unfamiliarity of classical developers with circuits and linear algebra.

Little Arklight is a project that aims to help developers transition from classical programming into quantum computing in a somewhat smooth manner.
This is achieved by demonstrating how one can write classical algorithms in terms of circuits as this formalism is extensively used in quantum computing.

The project is under active development so please do watch it for updates.

## Why Little Arklight

After [Avalon](https://github.com/avalon-lang) reached a respectable milestone where simple quantum algorithms could be written,
my attempts to introduce students and developers to quantum programming using Avalon were not successful.

It turns out that when learners read about quantum programs online, they see a lot of linear algebra which is rarely used
for simple classical algorithms and a lot of circuits which do not look like electronic circuits they are used to.

To bridge that gap, (Little) Arklight allows the programmer to configure the virtual machine by writing gates as matrices
and programs that use those gates as circuits. This remains true for both classical computing and quantum computing.

## What makes it little

In the full blown version of Arklight, performance will be taken into consideration. Performance of the VM and performance of your program through optimizations.
Moreover, it will include new future enabled by a configurable random access memory for both the classical VM and the quantum VM.

Though the "big" Arklight is not a priority at this moment ([Avalon](https//github.com/avalon-lang) is), it is definitely something I have in mind so please stay tuned.

## How it works

The programmer begins by configuring the virtual machine(s) by specifying the number of registers they want and the "primitive" gates they want to support.
This is done through the use of directives in JSON format. An example can be found at [directives sample file](examples/directives.json).

Then the user writes the program as a series of circuit that will be compiled to bytecode for the VM. The assembler checks the program for correctness as well before bytecode generation.
Once the bytecode is generated, it is packaged into a ZIP file with the directives file for potential distribution and execution.

Finally to run the program, the VM is invoked, passing the packaged ZIP which it reads, configures itself using the directives file then executes the bytecode displaying results if instructed to do so.

This system is quite primitive compared to the power of a full-fledged programming language but it is powerful enough to perform even non-trivial computations.

## State of the project

The assembler is nearing completion. The checker is almost fully finished after which code generation and packaging will be done.
The skeleton of the VM is in place and only the execution code remains to be filled. This is simply a giant switch that runs each instruction and it is coming soon.

## Show me the code

Using the directives in the examples folder, we configure the VM to accept two gates as native gates, meaning everything will be written in terms of those two.
The program below (also found in ``examples/program.al``) shows the implementation of the NAND gate in terms of AND and NOT then the OR gate is written in terms of NANDs.

```
// Sample program that shows a couple of circuits built from the basic gates configured for the VM.
circuit nand(pr1, pr2) {
    %pr1 = and(%pr1, %pr2);
    return not(%pr1);
}

circuit or(pr1, pr2) {
    %pr1 = %nand(%pr1, %pr1);
    %pr2 = %nand(%pr2, %pr2);
    return %nand(%pr1, %pr2);
}

circuit main() {
    // Initialize classical registers
    cr0 = 0b;
    cr1 = 1b;

    cr1 = %or(cr0, cr1);

    // Display the content of classical register cr0
    print(cr1);
}

```

## Running a preview

If you wish to track progress and want to check things out, please download this repository into the directory of your choice and install the requirements.
Once you have the requirements installed, you can run the assembler as follows (assuming ``src/as/kas.py`` has execute permissions):

```
$ ./kas.py examples/program.al --directives=examples/directives.json
```

At the moment, it will just display the main circuit with all circuits rewritten in terms of native gates.

Instructions for running the VM in development mode coming soon.

## Installation

Once the project is completed, you will be able to download the package directly from either PyPy and/or Conda or as independent executables. Stay tuned!

## Documentation

Documentation is in the works as well so watch this space for the same.

## Contributing

Thanks for considering it. Shoot me an email if you wish to contribute so I can help with directions.
Tests are currently missing to that's a good place to start if you are so inclined.

## Contact

You can reach me at <a href="mailto:nbashige@gmail.com">nbashige@gmail.com</a>

## License

This code is licensed under the MIT license. Please see the LICENSE file for the terms.

## Acknowledgement

Development of Arklight is being supported by the [Unitary Fund](https://unitary.fund) grant.
Thanks to [Will J. Zeng](http://willzeng.com) for running the program.

## Copyright

Copyright (c) 2018 Ntwali Bashige Toussaint
