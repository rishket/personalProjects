.section .multiboot
.align 4
.long 0x1BADB002		# Magic Number (multiboot header)
.long 0x00			# Flags (default value)
.long - (0x1BADB002 + 0x00) 	# Checksum
.long kernel_main		# Entry point (should be defined later in C or assembly)

# Your kernel's entry point (can be defined in C)
.global kernel_main
kernel_main:
	
	ret
