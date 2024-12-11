CC = gcc-13
LD = ld
NASM = nasm

# Flags for building the kernel (C files)
CFLAGS = -ffreestanding -m64 -Wall -Wextra -nostdlib -I include
LDFLAGS = -T linker.ld

# NASM Flags for bootloader
ASMFLAGS = -f elf64 -g -F dwarf

# Directories
BUILD_DIR=build
SRC_DIR=src
ISO_DIR=$(BUILD_DIR)/iso
GRUB_DIR=$(ISO_DIR)/boot/grub
BOOTLOADER_DIR=$(SRC_DIR)/bootloader
KERNEL_DIR=$(SRC_DIR)/kernel
INCLUDE_DIR=include

# Kernel and bootloader files
KERNEL_SRC=$(KERNEL_DIR)/kernel.c
KERNEL_OBJ=$(BUILD_DIR)/kernel.o
KERNEL_BIN=$(BUILD_DIR)/kernel.bin

# Bootloader files
BOOTLOADER_SRC=$(BOOTLOADER_DIR)/bootloader.asm
BOOTLOADER_OBJ=$(BUILD_DIR)/bootloader.o
BOOTLOADER_BIN=$(BUILD_DIR)/bootloader.bin

# Output ISO file
ISO_FILE=$(BUILD_DIR)/os.iso

# GRUB Config
GRUB_CFG=$(GRUB_DIR)/grub.cfg

# Create directories if they don't exist
$(ISO_DIR)/boot/grub:
	mkdir -p $(ISO_DIR)/boot/grub

# Build Bootloader
$(BOOTLOADER_OBJ): $(BOOTLOADER_SRC)
	@echo "Assembling bootloader..."
	$(NASM) $(ASMFLAGS) $(BOOTLOADER_SRC) -o $(BOOTLOADER_OBJ)

$(BOOTLOADER_BIN): $(BOOTLOADER_OBJ)
	@echo "Linking bootloader..."
	$(LD) -m elf_i386 -Ttext 0x7C00 -o $(BOOTLOADER_BIN) $(BOOTLOADER_OBJ)

# Build Kernel
$(KERNEL_OBJ): $(KERNEL_SRC)
	@echo "Compiling kernel..."
	$(CC) $(CFLAGS) -c $(KERNEL_SRC) -o $(KERNEL_OBJ)

$(KERNEL_BIN): $(KERNEL_OBJ)
	$(LD) $(LDFlAGS) -o $(KERNEL_BIN) $(KERNEL_OBJ)

# GRUB Configuration File
$(GRUB_CFG):
	mkdir -p $(GRUB_DIR)
	@echo "Creating GRUB configuration..."
	echo "set timeout=0" > $(GRUB_CFG)
	echo "set default=0" >> $(GRUB_CFG)
	echo 'menuentry "Rishis Operating System" {' >> $(GRUB_CFG)
	echo "    multiboot /boot/kernel.bin" >> $(GRUB_CFG)
	echo "    boot" >> $(GRUB_CFG)
	echo "}" >> $(GRUB_CFG)

# Build ISO
$(ISO_FILE): $(KERNEL_BIN) $(BOOTLOADER_BIN) $(GRUB_CFG)
	# Create bootable ISO structure
	@echo "Copying kernel and bootloader to ISO directory..."
	mkdir -p $(ISO_DIR)/boot/grub
	cp $(KERNEL_BIN) $(ISO_DIR)/boot/
	cp $(BOOTLOADER_BIN) $(ISO_DIR)/boot/
	cp $(GRUB_CFG) $(ISO_DIR)/boot/grub/
	
	@echo "Generating bootable ISO..."
	grub-mkrescue -o $(ISO_FILE) $(ISO_DIR)

# Run the OS in QEMU
run: $(ISO_FILE)
	@echo "Running in QEMU..."
	qemu-system-x86_64 -cdrom $(ISO_FILE)

# Clean and Build artifacts
clean:
	@echo "Cleaning build..."
	rm -rf $(BUILD_DIR)/*
