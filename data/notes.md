# Download Image

- Chrome Plugin:
https://chrome.google.com/webstore/detail/image-downloader-imageye/agionbommeaifngbhincahgmoflcikhm/related?hl=en

- Source: Google Images

- Image Format JPEG

- Cutting image:
    - Showing only the leafs (e.g., using gThumb)
    - Removing the fruits when possible

- Rename files: 
```console
$ ls -v | cat -n | while read n f; do mv -n "$f" "$n.jpg"; done
``` 
