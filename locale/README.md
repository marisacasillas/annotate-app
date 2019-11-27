We use Python's builtin `gettext()` facilities to localize messages in templates. You can set a prioritized list of languages in which to display messages in the user interface in `annotate/config.py`; you can specify any language for which translations have been created by its code (i.e., the name of an immediate subdirectory of this directory).

Presently, we expect all translatable messages to occur in `views/*.tpl` files.  Our tooling will only be able to reliably extract messages on pure-python lines (ones that begin with `%` and contain only Python code).

The `localize` script in the application's root directory helps automate the process of extracting messages to be translated and compiling them.  Translations are placed under this directory, following the usual GNU gettext structure. `localize` expects you to have the `gettext` utilities available in your PATH. In particular, it currently uses the `xgettext`, `msgmerge`, and `msgfmt` utilities.

## Adding/editing translations

Once you've added or changed messages in views, you'll need to run `localize` to extract them; this will automatically update `messages.pot` and the `.po` files for each language, keeping any existing translations that still apply.  Then you can edit the `.po` files for each language to add translations for the new messages.

Once you've added translations, run `localize` again to compile them into `.mo` files and make them available to the application. If the application is currently running, you may need to restart it to see the new translations.

## Adding a language

To add, e.g., French translations:

```
./localize init fr
```

Now edit `locale/fr/LC_MESSAGES/messages.po`. Start by removing any superfluous comments that `msginit` adds (use another language's `.po` file as an example) and fill in the language name on the `Language:` comment (in this case, "French"). Next, start adding French translations of the English `msgid`s. At this point, the process is the same as adding/editing translations for existing languages (see above).
