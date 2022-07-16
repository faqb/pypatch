# pypatch

<p> Python steganography tool with which you can hide files inside audio. </p>

## Installation
    git clone https://github.com/faqb/pypatch.git
    cd pypatch
    python3 -m env venv
    source env/bin/activate
    chmod +x pypatch.py
    python3 install -r requirements.txt

## IMPORTANT
To get the size of hidden file `pypatch` set file attribute `user.key`. Deleting this attribute will make impossible revealing source file.
Change `FILE_ATTRIBUTE` in `config.py` to set your own attribute name.

## Usage examples

### Help menu
Use `-h` after any option to get help menu.

    ./pypatch.py -h
    ./pypatch.py info -h
    ./pypatch.py hide -h
    ./pypatch.py reveal -h

### File info
Use `info` option to get information about MP3 or WAV file.
Shows size that can be hidden inside audio.

    ./pypatch.py info -t audio.mp3

### Hide file
Use `hide` to patch audio file and hide file inside.
Result file must be only in WAV format.

    ./pypatch.py hide -i audio.mp3 -o result_audio.wav -t image.png

### Reveal file
Use `reveal` to get hidden file from audio file.

    ./pypatch.py reveal -i audio.wav -o image.png
