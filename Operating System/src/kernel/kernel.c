#include <stdint.h>
#define MULTIBOOT_HEADER_MAGIC 0x1BADB002
#define MULTIBOOT_HEADER_FLAGS 0x00010003
#define MULTIBOOT_HEADER_CHECKSUM -(MULTIBOOT_HEADER_MAGIC + MULTIBOOT_HEADER_FLAGS)

// Entry point to linker.ld
extern void kernel_main(void);

__attribute__((section(".multiboot")))
struct multiboot_header {
	uint32_t magic;
	uint32_t flags;
	uint32_t checksum;
}
__attribute__((packed)) multiboot_header = {
	MULTIBOOT_HEADER_MAGIC,
	MULTIBOOT_HEADER_FLAGS,
	MULTIBOOT_HEADER_CHECKSUM
};

void kernel_main(void){
	const char *message = "Hello, from Rishi's Kernel";
	char *video_memory = (char *) 0xB8000;	// VGA text buffer address

	// Write the string to the screen in video memory
	for (int i = 0; message[i] != '\0'; i++){
		video_memory[i * 2] = message[i];	// Character
		video_memory[i * 2 + 1] = 0x07;		// Attribute byte (light grey on black)
	}

	// Infinite loop to halt the CPU (useful for debugging)
	while(1){
		__asm__ volatile("hlt");
	}
}


