# Makefile for uplink commands
# Installs commands to ~/bin with library in same directory

BIN_DIR = $(HOME)/bin
LIB_DIR = $(BIN_DIR)
LIB_FILE = uplink-lib.sh
COMMANDS = uplink-describe uplink-org uplink-monitor

.PHONY: install uninstall clean help

# Default target
all: help

# Install all commands and library to ~/bin
install: $(BIN_DIR)
	@echo "Installing uplink commands to $(BIN_DIR)/"
	@# Install library
	@cp bin/$(LIB_FILE) $(LIB_DIR)/
	@echo "  $(LIB_FILE) -> $(LIB_DIR)/$(LIB_FILE)"
	@# Install commands as-is
	@for cmd in $(COMMANDS); do \
		if [ -f bin/$$cmd ]; then \
			cp bin/$$cmd $(BIN_DIR)/$$cmd; \
			chmod +x $(BIN_DIR)/$$cmd; \
			echo "  $$cmd -> $(BIN_DIR)/$$cmd"; \
		else \
			echo "  ERROR: bin/$$cmd not found!"; \
			exit 1; \
		fi; \
	done
	@echo ""
	@echo "Installation complete!"
	@echo "Commands installed to: $(BIN_DIR)"
	@echo "Library installed to: $(LIB_DIR)/$(LIB_FILE)"
	@echo ""
	@echo "Note: Make sure $(BIN_DIR) is in your PATH to use these commands."

# Create ~/bin directory if it doesn't exist
$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

# Uninstall commands and library
uninstall:
	@echo "Removing uplink commands from $(BIN_DIR)/"
	@for cmd in $(COMMANDS); do \
		if [ -f $(BIN_DIR)/$$cmd ]; then \
			rm $(BIN_DIR)/$$cmd; \
			echo "  Removed $(BIN_DIR)/$$cmd"; \
		fi; \
	done
	@if [ -f $(LIB_DIR)/$(LIB_FILE) ]; then \
		rm $(LIB_DIR)/$(LIB_FILE); \
		echo "  Removed $(LIB_DIR)/$(LIB_FILE)"; \
	fi
	@echo "Uninstallation complete!"

# Clean up any temporary files
clean:
	@echo "No temporary files to clean"

# Show help
help:
	@echo "Uplink Commands Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  install   - Install commands and library to ~/bin (default)"
	@echo "  uninstall - Remove installed commands and library"
	@echo "  clean     - Clean up temporary files"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Commands to be installed:"
	@for cmd in $(COMMANDS); do echo "  - $$cmd"; done
	@echo ""
	@echo "Installation directory: $(BIN_DIR)"
	@echo "Library file: $(LIB_FILE)"
