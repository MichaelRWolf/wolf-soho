# TODO

## Makefile Integration Strategy

**Problem**: Integrate project root Makefile with Trails_End/Makefile

**Current State**:
- Root Makefile manages project-wide symlinks for `bin/network_location`
- Trails_End Makefile manages uplink monitoring commands with install/uninstall functionality

**Suggested Strategy**: Enhanced Integration Pattern
- Use delegation with `-C` flag to change directory
- Pass variables (BIN_DIR) to sub-makefile
- Provide unified `install`/`uninstall` targets
- Maintain separation of concerns

**Implementation**:
```makefile
# Add to root Makefile
.PHONY: uplink install_uplink uninstall_uplink clean_uplink help_uplink

# Delegate uplink-related targets to Trails_End Makefile
uplink install_uplink uninstall_uplink clean_uplink help_uplink:
	@$(MAKE) -C Trails_End $(MAKECMDGOALS:%=%)

# Update main targets
all: symlink_bin install_uplink
```

**Benefits**:
- Single entry point for all project tools
- Consistent interface using same BIN_DIR variable
- Modular design with independent Makefiles
- Extensible for future subdirectories

**Status**: Not implemented - deferred for later
