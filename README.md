# autotranscode

Automatically transcode video (and audio) files in a directory. This is my automated fix to DaVinci Resolve only supporting a very specific set of video formats with the free version on Linux.

This is a Python script that watches a folder for file changes. Once it sees a new (or changed) media file, it starts transcoding it, using the previously supplied ffmpeg settings.

## License

`autotranscode` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
