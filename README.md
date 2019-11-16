# Annotate (Anotar)

## Install

```sh
# Install pipenv, which we use for dependency management, globaly.
pip3 install pipenv # may need sudo
# Clone the application.
git clone https://github.com/marisacasillas/annotate-app.git
cd annotate-app
# Install dependencies.
pipenv install
# Copy some sound files to annotate into static/snippets.
cp YOUR_FILES_HERE static/snippets/
# Create the database for the snippets.
pipenv run ./make-database.py
# Run the application (starts a local web server).
pipenv run ./app.py
```

Point your browser at `http://localhost:8080/login`.
