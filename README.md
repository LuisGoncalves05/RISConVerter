# RISConVerter
#### Video Demo:  <https://youtu.be/rPw1WD8SJ2s>
#### Description: 
Hello World! 

This is my python project for CS50P, an assembly-to-binary and binary-to-assembly converter designed for the RISC-V ISA.

Here's how it works:

- **File Initialization**: The process begins by prompting the user to input the desired file name for the converted output, ensuring its validity based on the file's extension. If an invalid entry is made, the user is prompted again. The conversion mode (assembly-to-binary or binary-to-assembly) is determined by the file extension.

- **File Retrieval**: A function is used to retrieve the file intended for conversion, validating its existence and correct extension. If validation fails, the user is prompted to provide the file again.

- **Conversion Process**: Two distinct functions handle the conversion process, one for converting assembly to binary and the other for converting binary to assembly.

    - If the assembly mode is selected (indicated by a .s or .asm extension), a file with the specified name is created. The content of the file is then read, with each 32-bit instruction extracted and parsed into its corresponding fields following the RISC-V reference card. Imm fields are converted to integers from two's complement strings, while register fields are formatted as 'x(integer)' from unsigned binary. Note that not all instructions are encoded the same and some of these fields may not have a meaning depending on the type of instruction. 
    
    - To identify instructions by their fields, a CSV file within the program is utilized. It contains all (non-pseudo) instructions alongside their corresponding type, opcode, funct3, and funct7. In instructions lacking funct7 or funct3 fields, these are represented as None. These instructions are parsed into a dictionary, containing opcodes as keys and their respective types as values, and a dictionary with identifiers and their corresponding instructions. These identifiers, derived from opcode, funct3, and funct7, allow for instruction identification from the binary. Different instruction types may require distinct formatting in assembly, hence specific formatting functions are employed accordingly.

    - The conversion process iterates until all instructions within the binary file have been processed.

    - For binary mode (indicated by a .bin extension), a similar process ensues. The CSV file is read in binary mode, providing a dictionary mapping instructions to a dictionary containing their respective type, opcode, funct3, and funct7 fields.

    - The assembly file to be converted is passed to a function to extract instructions, removing unnecessary white characters and comments while standardizing the format ('inst field1 field2 field3' for all appropriate fields). Each instruction is converted into a list of fields, separated into the instruction itself and additional components. The instruction is then used to retrieve the corresponding parameters dictionary, while the additional components provide imm values (converted to ints from decimal or hex strings) and/or register names. Instructions are subsequently encoded into binary strings based on their type-specific (and in some cases opcode-specific) encodings.

    - Finally, the instruction is converted from str to bytes and stored sequentially in the output file. This process is repeated for all instructions in the list.