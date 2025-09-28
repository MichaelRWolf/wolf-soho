SOURCE_BIN_DIR := bin
BIN_FILES := bin/network_location
INSTALL_BIN_DIR := $(HOME)/bin

# Uplink commands configuration
UPLINK_COMMANDS := uplink-describe uplink-org uplink-monitor
UPLINK_LIB := uplink-lib.sh

.PHONY: all symlink_bin install_uplink uninstall_uplink clean todo help

all: symlink_bin install_uplink

symlink_bin:
	@mkdir -p $(INSTALL_BIN_DIR)
	@for bin_file in $(BIN_FILES); do \
		ln -sfv $(PWD)/$$bin_file $(INSTALL_BIN_DIR); \
	done

# Install uplink commands and library
install_uplink: $(INSTALL_BIN_DIR)
	@echo "Installing uplink commands to $(INSTALL_BIN_DIR)/"
	@# Install library
	@cp bin/$(UPLINK_LIB) $(INSTALL_BIN_DIR)/
	@echo "  $(UPLINK_LIB) -> $(INSTALL_BIN_DIR)/$(UPLINK_LIB)"
	@# Install commands
	@for cmd in $(UPLINK_COMMANDS); do \
		if [ -f bin/$$cmd ]; then \
			cp bin/$$cmd $(INSTALL_BIN_DIR)/$$cmd; \
			chmod +x $(INSTALL_BIN_DIR)/$$cmd; \
			echo "  $$cmd -> $(INSTALL_BIN_DIR)/$$cmd"; \
		else \
			echo "  ERROR: bin/$$cmd not found!"; \
			exit 1; \
		fi; \
	done
	@echo ""
	@echo "Uplink installation complete!"
	@echo "Commands installed to: $(INSTALL_BIN_DIR)"
	@echo "Library installed to: $(INSTALL_BIN_DIR)/$(UPLINK_LIB)"

# Create ~/bin directory if it doesn't exist
$(INSTALL_BIN_DIR):
	@mkdir -p $(INSTALL_BIN_DIR)

# Uninstall uplink commands and library
uninstall_uplink:
	@echo "Removing uplink commands from $(INSTALL_BIN_DIR)/"
	@for cmd in $(UPLINK_COMMANDS); do \
		if [ -f $(INSTALL_BIN_DIR)/$$cmd ]; then \
			rm $(INSTALL_BIN_DIR)/$$cmd; \
			echo "  Removed $(INSTALL_BIN_DIR)/$$cmd"; \
		fi; \
	done
	@if [ -f $(INSTALL_BIN_DIR)/$(UPLINK_LIB) ]; then \
		rm $(INSTALL_BIN_DIR)/$(UPLINK_LIB); \
		echo "  Removed $(INSTALL_BIN_DIR)/$(UPLINK_LIB)"; \
	fi
	@echo "Uplink uninstallation complete!"

clean:
	@echo "Nothing to clean."

help:
	@echo "Wolf-SOHO Project Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all            - Install all project tools (symlinks + uplink commands)"
	@echo "  symlink_bin    - Create symlinks for project binaries"
	@echo "  install_uplink - Install uplink monitoring commands"
	@echo "  uninstall_uplink - Remove uplink monitoring commands"
	@echo "  clean          - Clean project files"
	@echo "  todo           - Show project todos"
	@echo "  help           - Show this help message"

todo:
	@echo 1. Incorporate '~/repos/wolf-soho' into 'Portable-Profile'
	@echo 2. Incorporate '~/repos/apple-photos' into 'Portable-Profile' and/or wolf-soho
