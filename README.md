# autotranscode

Automatically transcode video (and audio) files in a directory. This is my automated fix to DaVinci Resolve only supporting a very specific set of video formats with the free version on Linux.

This is a Python script that watches a folder for file changes. Once it sees a new (or changed) media file, it starts transcoding it, using the previously supplied ffmpeg settings.

## Installation & Usage

From source: install `hatch`, then use `hatch run autotranscode` and take a look at the available options.

Alternatively, for a global release installation, download the tarball from the release (not the sources!) and run `pipx install <tarball>`. You can now use `autotranscode`.

```
Usage: autotranscode [OPTIONS] DIRECTORY

  Watch and transcode all video files in a directory tree automatically.

Options:
  --version                     Show the version and exit.
  -s, --suffix TEXT             Suffix to add to the encoded files.
                                [required]
  -cv, --video-codec TEXT       Video codec to encode into. Input files that
                                are already supported or match this codec are
                                never transcoded.  [required]
  -ca, --audio-codec TEXT       Audio codec to encode into. Input files that
                                are already supported or match this codec are
                                never transcoded.  [required]
  --container TEXT              Video container to use.
  -o, --extra-output-args TEXT  Extra ffmpeg arguments to add to each output
                                file. This is useful for additional output
                                format options, such as encoder-specific
                                settings. Use the format 'option=value', and
                                omit the leading dash. Take care: not all
                                files will have video and/or audio streams.
  -i, --extra-input-args TEXT   Extra ffmpeg arguments to add to each input
                                file. These are usually global ffmpeg options,
                                such as hardware acceleration. Use the format
                                'option=value', and omit the leading dash.
  --help                        Show this message and exit.
```

## License

`autotranscode` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
