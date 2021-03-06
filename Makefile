all: help
.PHONY : all

VER=3
PACKAGE_NAME=yasi-indenter.sublime-package
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

DEPS=*.sublime-keymap *.sublime-menu *.py *.sublime-settings

$(PACKAGE_NAME): $(DEPS)
	@echo Zipping package $(PACKAGE_NAME)
	@rm -f $(PACKAGE_NAME)
	@7z a -tzip $(PACKAGE_NAME) $(DEPS) > /dev/null

zip: $(PACKAGE_NAME)
.PHONY : zip

check:
	pep8 indent.py
	@printf "\n-------------------\n"
	pylint indent.py
.PHONY : check

help:
	@echo "Targets:"
	@echo " -> zip"
	@echo " -> dist"
	@echo " -> check"
.PHONY : help
