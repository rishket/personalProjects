**Rishi's 32-bit OS Kernel**

_________________________________________



This is an Operating System I made from scratch using an Ubuntu x86_64 14.04 VM and QEMU to emulate. As of right now, it prints a simple message to the bootloader, but I have not yet figured out how to link the kernel. So far, it seem the bootloader can't find the memory address at which the kernel is located (out of reach).



**Contents:**

*Bootloader - boot.asm/bootloader.asm*

*Kernel - kernel.c*

Binaries: kernel.bin/bootloader.bin

Makefile

ISO Disk Image
