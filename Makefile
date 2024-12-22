SOURCE_BIN_DIR := bin
BIN_FILES := bin/network_location
INSTALL_BIN_DIR := $(HOME)/bin

.PHONY: all clean symlink_bin

all: symlink_bin


symlink_bin:
	@mkdir -p $(INSTALL_BIN_DIR)
	@for bin_file in $(BIN_FILES); do \
		ln -sfv $(PWD)/$$bin_file $(INSTALL_BIN_DIR); \
	done

clean:
	@echo "Nothing to clean."
