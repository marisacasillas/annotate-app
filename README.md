# Annotate (Anotar)

Annotate (Anotar) is an application for efficiently eliciting text-based annotations of short audio files. This application may be useful to those who have a collection of short audio files that need to be listened to and annotated by hand (e.g., transcription, speaker type, the topic at hand).

The application is run through local server, meaning that audio playback and text entry are done in your web browser, but using files that stored on your local machine. To do this the app relies on Python, your web browser (we recommend Chrome), and the Howler audio library. All file storage is local. Therefore, the Annotate application can be used for offline projects (e.g., in 'the field') and projects with strict data privacy policies.

Once a batch of annotation is initiated and the application is up and running (see [Getting started](#markdown-header-getting-started) below), annotators can log in, add annotations, track their progress, log out when ready for a break, and repeat when they're ready to begin again. Some features of the application include:

**Required user login:** Each annotation is time-stamped and associated with a particular user. This features is useful for tracking sources of between-annotator variability in their dataset and for checking that work is being divided as planned.

**Progress updates:** Users are reminded of how many annotations they've completed that day, how many they've completed overall for the current batch, and how many are left to do in the batch. This information can help motivate users to keep annotative and can also aid consistent annotation progress from one work session to the next.

**Keyboard input:** Most interaction with the application can be done purely from keyboard input. This feature significantly speeds up text entry and audio playback. See [Keyboard input](#markdown-header-keyboard-input) for a list of key commands.

**Required input for each clip:** Users must enter some value into the text box before proceeding to the next annotation. This feature prevents incomplete annotations, and can be combined with a default 'skip'/'unclear' annotation convention to ensure comprehensive annotation over the audio file batch.

**Backward navigation/re-annotation:** Users can re-visit and edit their entries for audio clips they have already annotated. This is useful when further context might clarify the content of an audio file recently heard.

_Note: This application was built for use with Spanish speakers, so the action labels and default user names are in Spanish (this can be easily changed; see [Language settings](#markdown-header-language-settings) below)._

_Figure 1._ Screen shot of an annotation being made by `usuario2`.

![Screen shot of an annotation being made by `usuario2`.](example-screenshot.png)

## Getting started

**Install the annotate-app**

```sh
# Install pipenv, which we use for dependency management, globally.
pip3 install pipenv # may need sudo
# Clone the application.
git clone https://github.com/marisacasillas/annotate-app.git
cd annotate-app
# Install dependencies.
pipenv install
```

**Copy the batch of audio clips you want to annotate into `annotate-app/static/snippets/`**

```sh
# Copy some sound files to annotate into static/snippets.
cp YOUR_FILES_HERE static/snippets/
```
Make sure the directory _only_ contains sound files that you want to annotate.

**Initialize the database of audio clip annotations**

```sh
# Create the database for the snippets.
pipenv run ./make-database.py
```
Note that, if you are preparing your second batch, you have to remove the old database file first.

**Start up the application**

```sh
# Run the application (starts a local web server).
pipenv run ./app.py
```
Note that this command needs to be run again if the host computer is rebooted.

**Begin annotating**

Point your browser at [`http://localhost:8080/login`](). The default user names are `usuario1` and `usuario2`. Log in, listen, and enter your responses.

**Inspect the annotations**

Annotations are stored in a database file in `annotate-app/var/`. Use the `db2csv.py` script to convert this file into a CSV and then inspect as you normally would (in R, Excel, etc.). We recommend using a file name that reflects the date and time of your file conversion.

```sh
# Convert the database file into a CSV
# arguments: [PATH_TO_DB] [PATH_FOR_NEW_CSV]
./db2csv.py var/database.db var/converted_dbs/annotate_database_TIMESTAMP.csv

```

## Key commands
[to be filled in!]

notes for now:

- playback should start right away, ready for text input
- to start/stop audio: unfocus from the text box w/ esc, then use `/` to pause/play or the left arrow to start the audio clip again
- once playback starts again, the application automatically focuses on the text box again, ready for input
- the text box can be refocused without starting audio playback again by hitting T
- submit the current annotation by escaping the text box and hitting shift + right arrow
- return to a previous annotation by escaping the text box and hitting shift + left arrow

## Language settings
[to be filled in!]

strings:

- users
- progress updates
- empezar anotaciones, salir, próximo, último

## Desktop use
[to be filled in!]


## Authorship and conditions of use
This application was authored and designed by Shawn Cameron Tice (author, creator) and Marisa Casillas (creator). We support the open re-use of code, and hereby distribute this project under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/), which requires that any work using modifications of this source code must be made available to the public using the same license (see `annotate-app/LICENSE.txt` for details).

If you would like to cite this project in your work, please refer to the project's home on GitHub ([https://github.com/marisacasillas/annotate-app]()). Please raise issues, contribute improvements, and leave other comments or suggestions regarding this project on its GitHub repository.
