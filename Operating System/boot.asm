; boot.asm
[bits 32]           ; Set to 32-bit mode
[global _start]     ; Make _start the entry point
[extern kernel_main]    ; Declare kernel_main as an external symbol

_start:
    cli     ; Disable interrupts
    mov esp, 0x90000    ; Set stack pointer
    call kernel_main    ; Call the main C function
    hlt                 ; Halt the CPU