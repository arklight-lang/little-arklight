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
