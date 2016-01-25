[![Latest tag][tag]][tag~]
[![Package Control Downloads][pkg-downloads]][pkg-downloads~]

## sublime-yasi - yasi indenter meets Sublime Text

Enables correct lisp code indentation from within Sublime Text 3.

### Installation
+ The repo way:

  + Hit `Ctrl+Shift+P`
  + Launch `Add Repository`
  + Paste `https://github.com/nkmathew/sublime-yasi`
  + `Ctrl+Shift+P` again
  + Click `Install Package`, lookup **yasi** and install it

+ Standard way(via [Package Control][pkg]):
  + Hit `Ctrl+Shift+P` > `Install Package` search for **yasi** and install it

+ Manually:
  + Clone repo or download [master.zip][zip]
  + Run `make VER=2` to install for Sublime 2 or `make VER=3` for Sublime 3

### Features
+ Indenting selections:

  Hit `Ctrl+r` to indent the selection or alternatively navigate to the **Selection**
  menu then **Format** then **Indent S-expression**.

+ Indenting the current line:

  Hitting `Ctrl-r` without an existing selection will result in the current line
  being reindented.

+ Auto-indentation:

  Auto-indents the next line when the enter key is pressed

+ Indenting file on save(opt-out feature, see [preferences](#preferences))

### Preferences
To turn off file auto-indentation on save go to the user settings in,
![Prefences > Package Settings > yasi-indenter > Settings - User][img]

and change the value to `false` like so:

```js
{
    "indent_sexp_on_save": false
}
```


### Screencast
![Demo](http://imgur.com/TlQgSFb.png)

[tag]: https://img.shields.io/github/tag/nkmathew/sublime-yasi.svg
[tag~]: https://github.com/nkmathew/sublime-yasi/releases
[pkg-downloads]: https://packagecontrol.herokuapp.com/downloads/yasi-indenter.svg
[pkg-downloads~]: https://packagecontrol.io/packages/yasi-indenter
[pkg]: https://packagecontrol.io/
[zip]: https://github.com/nkmathew/sublime-yasi/archive/master.zip
[img]: http://i.imgur.com/yazls5v.png
