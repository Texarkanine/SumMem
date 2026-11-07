# Zoom and Recall

`wake` shows a nap's caption in place of the memories under it. Two commands read past the caption: `zoom` opens one nap, and `recall` searches every remembered line. Neither writes a file, takes the lock, or waits on a writer. Both print rows as [memory lines](wake.md#memory-lines), the same format as `wake`.

## Zoom

`zoom <id>` prints the two children of one nap, one level down. The id may be a row of the view or a nap nested inside one, so repeated zooms walk down to the notes.

Zoom reads only children files in the current checkout. Every sentence a zoom can still owe is in a file at the tip, so squash-merges and shallow clones lose nothing, and an older commit is never consulted.

## Recall

`recall <pattern>` searches with a regular expression. It matches the text of notes and the captions of naps, including notes and captions nested inside children files. It does not match a row's grain, id, or date.

So the view answers everyday questions with captions standing in for their children, and `recall` reaches the original sentences when a caption is not enough.

## Unreadable children files

When `zoom` or `recall` cannot read a children file, it prints `skipped a pack` once on standard error and still prints whatever other naps answered. `wake` stays silent about it.

## Cost

`zoom` and `recall` parse each children file in the view at most once per command. They work out unique prefixes once per command: they sort the distinct ids and compare each with its neighbors, so printing a line is a lookup. Uniqueness is among distinct ids, so two rows that share an id still share one prefix.
