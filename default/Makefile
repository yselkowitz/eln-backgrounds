WP_BG_DIR=$(WP_BG_ROOT)/default
WP_BG_REL=$(WP_REL_PATH)/default

THEMES_PNG= \
	$(WP_NAME)-01-day.png \
	$(WP_NAME)-01-night.png

WP_PNG_DESTS=$(THEMES_PNG:%=$(WP_BG_DIR)/%)

INSTALL_RULES= \
	install-base \
	install-gnome

.PHONY: $(WP_PNG_DESTS) $(INSTALL_RULES) \
        all install

$(WP_PNG_DESTS): OUTNAME = $(shell $(BASENAME) $@)
$(WP_PNG_DESTS):
	$(MKDIR) $(WP_BG_DIR)
	#~ Convert to RGB-format file (no alpha) and fix timestamp
	$(MAGICK) $(OUTNAME) -alpha off $@ 
	$(TOUCH_R) $(OUTNAME) $@

all:

install: $(INSTALL_RULES)

install-base: $(WP_PNG_DESTS)
	$(MKDIR) $(WP_BG_DIR)
	$(INSTALL) $(WP_NAME).xml	$(WP_BG_DIR)/$(WP_NAME).xml
	#~ Base background images done by WP_PNG_DESTS rules

install-gnome:	
	#~ GNOME background
	$(MKDIR) $(GNOME_BG_DIR)
	$(INSTALL) gnome-backgrounds-$(WP_NAME).xml	$(GNOME_BG_DIR)/$(WP_NAME).xml
