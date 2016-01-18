all: help
.PHONY : all

VER=3
PACKAGE_NAME='sublime-yasi.sublime-package'
PACKAGE_FOLDER = '$(APPDATA)\Sublime Text $(VER)\Installed Packages'
OS = $(shell uname)
ifeq ($(OS),Darwin)
	PACKAGE_FOLDER='~/Library/Application Support/Sublime Text $(VER)/Installed Packages'
else ifeq ($(OS),Linux)
	PACKAGE_FOLDER='~/.config/sublime-text-$(VER)/Installed Packages'
endif

dist:zip
	@echo Copying package $(PACKAGE_NAME) to $(PACKAGE_FOLDER)
	@cp $(PACKAGE_NAME) $(PACKAGE_FOLDER)
.PHONY : dist

DEPS=*.sublime-keymap *.sublime-menu *.py

sublime-yasi.sublime-package: $(DEPS)
	@echo Zipping package $(PACKAGE_NAME)
	@7z a -tzip $(PACKAGE_NAME) $(DEPS) > /dev/null

zip: sublime-yasi.sublime-package
.PHONY : zip

help:
	@echo "Targets:"
	@echo " -> zip"
	@echo " -> dist"
.PHONY : help
