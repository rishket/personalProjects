ENTRY(kernel_main)

SECTIONS {	
	. = 1M;			/* Start at 1MB (BIOS limitation) */

	.multiboot : {
		*(.multiboot)
	}

	.text : {
		*(.text)	/* Code section */
	}
	
	.data : {
		*(.data)	/* Data section */
	}

	.bss : {
		*(.bss)		/* Uninitialized data section */
	}

	/DISCARD/ : {
		*(.comment)
		*(.note.GNU-stack)
	}
}
