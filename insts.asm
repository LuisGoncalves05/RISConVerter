add x5, x6, x7
sub x8, x9, x10
xor x11, x12, x13



or x14, x15, x16 
and x17, x18, x19
sll x20, x21, x4
srl x22, x23, x3
sra x24, x25, x2
slt x26, x27, x28
addi x5, x6, 100
xori x8, x9,    255
        ori x11, x12, 10
andi x14, x15, 255
slli x17, x18, 5
srli x20, x21, 6
srli    x23, x24, 7
slti x26, x27, 50
sltiu x29, x30, 30
lbu x4, 100(x6)
lh x8, 200(x9)
lw x12, 300(x12)
lbu x16, 400(x15)
lhu x20, 500(x18)
sb x20,    600(x21)
sh x23, 700(x24)
sw x26, 800(x27)
beq x5, x8, 100

bne x11, x14, 200
blt x17, x20, 300
bge x23, x26, 400
bltu x5, x11,   0x500
jal x4,  0x700
jalr x8, x11, 800
lui x14, 155648
auipc x17, 155648
ebreak
ecall
        mul x5, x8, x11
mulh x14,        x17, x20
mulsu x23, x26, x29


mulu x8, x11, x14
div x17,                x20, x23
divu x26   , x29, x5
rem x8,                 x11, x14
remu   x17, x20, x23
