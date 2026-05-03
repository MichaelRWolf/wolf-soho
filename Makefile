SOURCE_BIN_DIR := bin
BIN_FILES := bin/network_location bin/beryl_sqm bin/networkCurl \
             bin/gitnas-repo-create bin/gitnas-remote-add \
             bin/gitnas-repo-setup bin/gitnas-repo-sync \
             bin/fleet-status bin/git-status-summary \
             bin/fleet-nas-sync
INSTALL_BIN_DIR := $(HOME)/bin
LAUNCHD_DIR := $(HOME)/Library/LaunchAgents
LAUNCHD_PLISTS := launchd/com.wolfenterprises.fleet-nas-sync.plist

# Uplink commands configuration
UPLINK_COMMANDS := uplink-describe uplink-org uplink-monitor
UPLINK_LIB := uplink-lib.sh

.PHONY: setup-hooks all symlink_bin install uninstall install_uplink uninstall_uplink install_launchd uninstall_launchd clean todo help verify_TM_exclusions

setup-hooks:
	pre-commit install



# Default target - show help
all: help

# Install all project tools
install: symlink_bin install_uplink

# Uninstall all project tools
uninstall: uninstall_uplink
	@echo "Removing symlinks from $(INSTALL_BIN_DIR)/"
	@for bin_file in $(BIN_FILES); do \
		if [ -L $(INSTALL_BIN_DIR)/$$(basename $$bin_file) ]; then \
			rm $(INSTALL_BIN_DIR)/$$(basename $$bin_file); \
			echo "  Removed $(INSTALL_BIN_DIR)/$$(basename $$bin_file)"; \
		fi; \
	done
	@echo "Uninstall complete!"

symlink_bin:
	@mkdir -p $(INSTALL_BIN_DIR)
	@for bin_file in $(BIN_FILES); do \
		ln -sfv $(PWD)/$$bin_file $(INSTALL_BIN_DIR); \
	done

# Install uplink commands and library
install_uplink: $(INSTALL_BIN_DIR)
	@echo "Installing uplink commands to $(INSTALL_BIN_DIR)/"
	@# Install library
	@ln -sfv $(PWD)/bin/$(UPLINK_LIB) $(INSTALL_BIN_DIR)/$(UPLINK_LIB)
	@# Install commands
	@for cmd in $(UPLINK_COMMANDS); do \
		if [ -f bin/$$cmd ]; then \
			ln -sfv $(PWD)/bin/$$cmd $(INSTALL_BIN_DIR)/$$cmd; \
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
		if [ -L $(INSTALL_BIN_DIR)/$$cmd ]; then \
			rm $(INSTALL_BIN_DIR)/$$cmd; \
			echo "  Removed $(INSTALL_BIN_DIR)/$$cmd"; \
		fi; \
	done
	@if [ -L $(INSTALL_BIN_DIR)/$(UPLINK_LIB) ]; then \
		rm $(INSTALL_BIN_DIR)/$(UPLINK_LIB); \
		echo "  Removed $(INSTALL_BIN_DIR)/$(UPLINK_LIB)"; \
	fi
	@echo "Uplink uninstallation complete!"

install_launchd:
	@mkdir -p $(LAUNCHD_DIR)
	@for plist in $(LAUNCHD_PLISTS); do \
		cp $$plist $(LAUNCHD_DIR)/; \
		launchctl load $(LAUNCHD_DIR)/$$(basename $$plist); \
		echo "Loaded: $$(basename $$plist)"; \
	done

uninstall_launchd:
	@for plist in $(LAUNCHD_PLISTS); do \
		launchctl unload $(LAUNCHD_DIR)/$$(basename $$plist) 2>/dev/null || true; \
		rm -f $(LAUNCHD_DIR)/$$(basename $$plist); \
		echo "Unloaded: $$(basename $$plist)"; \
	done

clean:
	@echo "Nothing to clean."

verify_TM_exclusions:
	cd TimeMachine && prove -v ./verify-tm-isexcluded

help:
	@echo "Wolf-SOHO Project Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  install       - Install all project tools (symlinks + uplink + gitnas commands)"
	@echo "  uninstall     - Remove all project tools (symlinks + uplink + gitnas commands)"
	@echo "  symlink_bin   - Create symlinks for project binaries"
	@echo "  install_uplink - Install uplink monitoring commands"
	@echo "  uninstall_uplink - Remove uplink monitoring commands"
	@echo "  clean         - Clean project files"
	@echo "  verify_TM_exclusions - Run Time Machine exclusion verification tests"
	@echo "  todo          - Show project todos"
	@echo "  help          - Show this help message"
	@echo ""
	@echo "gitnas commands (installed to ~/bin/ via make install):"
	@echo "  gitnas-repo-create  - Create bare repo on NAS (gh-derivative)"
	@echo "  gitnas-remote-add   - Add 'nas' remote to local repo (git-derivative)"
	@echo "  gitnas-repo-setup   - Create + add remote in one step (gh+git)"
	@echo "  gitnas-repo-sync    - Push to nas remote; --all for fleet push (gh-derivative)"
	@echo ""
	@echo "fleet commands (installed to ~/bin/ via make install):"
	@echo "  fleet-status        - Summarize git status across ~/repos/*; --with-nas adds nas column"
	@echo "  fleet-nas-sync      - Push all nas-remote repos; connectivity guard + staleness warn"
	@echo "  git-status-summary  - Alias for fleet-status (legacy name)"
	@echo ""
	@echo "launchd agents (install via make install_launchd):"
	@echo "  fleet-nas-sync      - Daily 16:00 NAS sync; logs to ~/Library/Logs/fleet-nas-sync.log"
	@echo ""
	@echo "Usage:"
	@echo "  make           - Show this help (default)"
	@echo "  make install   - Install all project tools"
	@echo "  make uninstall - Remove all project tools"
	@echo "  make help      - Show this help message"

todo:
	@echo 1. Incorporate '~/repos/wolf-soho' into 'Portable-Profile'
	@echo 2. Incorporate '~/repos/apple-photos' into 'Portable-Profile' and/or wolf-soho
