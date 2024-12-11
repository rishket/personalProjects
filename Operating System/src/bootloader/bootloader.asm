; Bootloader
[bits 16]	; BIOS runs in 16-bit assembly
		; BIOS loads the bootloader at this address

_start:
			; Print "Hello, from Rishi's Kernel" on screen
	mov ah, 0x0E	; BIOS teletype function
	mov al, 'H'	
	int 0x10
	mov al, 'e'
	int 0x10
	mov al, 'l'
	int 0x10
	mov al, 'l'
	int 0x10
	mov al, 'o'
	int 0x10
        mov al, ' '
	int 0x10
        mov al, 'W'
	int 0x10
        mov al, 'o'
	int 0x10
        mov al, 'r'
	int 0x10
        mov al, 'l'
	int 0x10
        mov al, 'd'
	int 0x10
        mov al, '!'

	; Infinite Loop to prevent system crash
	jmp $

times 510 - ($ - $$) db 0	; Pad to 512 bytes (standard boot sector size)
dw 0xAA55

