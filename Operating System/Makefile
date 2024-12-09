# Compiler Settings:
CC = i386-elf-gcc
CFLAGS = -ffresstanding -O2 -Wall -Wextra -nostdlib -fno-builtin -m32
LDFLAGS = -T linker.ld -ffresstanding -O2 nostdlib -m32

# Source and object files
ASM_SRC = boot.asm
SRC = kernel.c
OBJ = $(SRC:.c=.o)
KERNEL_BIN = kernel.builtin
# Default target
all: $(KERNEL_BIN)

# Link kernel object to binary
$(KERNEL_BIN): $(OBJ)
	$(CC) $(LDFLAGS) $(OBJ) -o $(KERNEL_BIN)

# Compile C source to object
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

GRUB_BIN = /usr/local/bin/grub-mkrescue
ISO_NAME = os.iso
ISO_DIR = iso

all: $(KERNEL_BIN) $(ISO_NAME)

$(ISO_NAME): $(KERNEL_BIN)
	mkdir -p $(ISO_DIR)/boot/grub
	cp $(KERNEL_BIN) $(ISO_DIR)/boot/
	cp grub.cfg $(ISO_DIR)/boot/grub/
	grub-mkrescue -o $(ISO_NAME) $(ISO_DIR)

clean:
	rm -rf $(ISO_DIR) $(KERNEL_BIN) $(ISO_NAME)