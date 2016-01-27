### Unreleased
- Fixes:
  - Wrong auto-indent when a string is an argument to the current function call
    e.g.

    ```clojure
      (blablabla "that stuff: " []
                                (println "blablabla!"))
    ```
    Placing the cursor between the square brackets and hitting enter will place the
    closing square bracket below the word **that**

### v0.4.2 - 26th January 2016
- Update to yasi v2.0.1

### v0.4.1 - 25th January 2016

Fixes:
  - Forgot to remove logging function call used in debugging


### v0.4.0 - 25th January 2016

Fixes:
  - Made to work with the updated yasi version(v2.0.0)

### v0.3.0 - 25th January 2016

Fixes:
  - Enter key not being released when editing any other non lisp file

Features:
  - Context menu entry for launching indenter

### v0.2.0 - 24th January 2016

Features:
  - Auto-indentation on enter keypress

Fixes:
  - Dialect/language setting not being passed when indenting a selection

### v0.1.2 - 18th January 2016

Fixes:
  - Proper yasi module importation

### v0.1.1 - 18th January 2016

Fixes:

  - Malfunction in Sublime 2 due to lack of argparse library in Sublime's python
    installation(v2.6.5)
