[![Latest tag][tag]][tag~]

## sublime-yasi - yasi indenter meets Sublime Text

Enables correct lisp code indentation from within Sublime Text 3.

### Installation
It's not in [Package Control][pkg] yet, so you'll have to install it the repo way:

  + Hit `Ctrl+Shift+P`
  + Launch `Add Repository`
  + Paste `https://github.com/nkmathew/sublime-yasi`
  + `Ctrl+Shift+P` again
  + Click `Install Package`, lookup **yasi** and install it


### Key bindings
Hit `Ctrl+r` to indent the selection or alternatively navigate to the **Selection**
menu then **Format** then **Indent S-expression**.

Hitting `Ctrl-r` without an existing selection will result in the current line being
reindented.

As usual the bindings can be changed from the **Preferences** menu

### Screencast
![Demo](http://imgur.com/TlQgSFb.png)

[tag]: https://img.shields.io/github/tag/nkmathew/sublime-yasi.svg
[tag~]: https://github.com/nkmathew/sublime-yasi/releases
[pkg]: https://packagecontrol.io/
