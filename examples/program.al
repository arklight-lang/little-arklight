// Sample program that shows a couple of circuits built from the basic gates configured for the VM.
// Native gates and VM registers do not start with a PERCENT sign.
// Circuits and parameters to circuits begin with a PERCENT sign.
// In this particular case, we use the native gates AND and NOT along with two classical registers cr0 and cr1

// NAND gate implemented as a circuit in terms of AND and NOT native gates
circuit nand(pr1, pr2) {
    %pr1 = and(%pr1, %pr2);
    return not(%pr1);
}

// OR gate implemented as a circuit in terms of the NAND circuit above
circuit or(pr1, pr2) {
    %pr1 = %nand(%pr1, %pr1);
    %pr2 = %nand(%pr2, %pr2);
    return %nand(%pr1, %pr2);
}

// The main circuit serves as the entry point
circuit main() {
    // Initialize classical registers
    cr0 = 0b;
    cr1 = 1b;

    // apply the OR circuit to the cr0 and cr1 regsters
    cr1 = %or(cr0, cr1);

    // Display the content of classical register cr1
    print(cr1);
}
