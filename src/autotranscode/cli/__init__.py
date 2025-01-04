# SPDX-FileCopyrightText: 2025-present kleines Filmröllchen <kleines@filmroellchen.eu>
#
# SPDX-License-Identifier: MIT
import asyncio
import click

from autotranscode.__about__ import __version__
from autotranscode.ffmpeg import FFmpegHandler
from autotranscode import handle_transcoding
from pathlib import Path
from click import Path as PathArgument


@click.command(
    help="Watch and transcode all video files in a directory tree automatically."
)
@click.version_option(version=__version__, prog_name="autotranscode")
@click.argument(
    "directory",
    type=PathArgument(exists=True, path_type=Path),
)
@click.option(
    "--suffix",
    "-s",
    "suffix",
    required=True,
    help="Suffix to add to the encoded files.",
)
@click.option(
    "--video-codec",
    "-cv",
    "video_codec",
    required=True,
    help="Video codec to encode into. Input files that are already supported or match this codec are never transcoded.",
)
@click.option(
    "--audio-codec",
    "-ca",
    "audio_codec",
    required=True,
    help="Audio codec to encode into. Input files that are already supported or match this codec are never transcoded.",
)
@click.option("--container", "container", default="mp4", help="Video container to use.")
@click.option(
    "--extra-output-args",
    "-o",
    "output_args",
    help="Extra ffmpeg arguments to add to each output file. This is useful for additional output format options, such as encoder-specific settings. Use the format 'option=value', and omit the leading dash. Take care: not all files will have video and/or audio streams.",
    type=str,
    multiple=True,
    default=tuple(),
)
@click.option(
    "--extra-input-args",
    "-i",
    "input_args",
    help="Extra ffmpeg arguments to add to each input file. These are usually global ffmpeg options, such as hardware acceleration. Use the format 'option=value', and omit the leading dash.",
    type=str,
    multiple=True,
    default=tuple(),
)
def autotranscode(
    directory: Path,
    suffix: str,
    video_codec: str,
    audio_codec: str,
    container: str,
    output_args: tuple[str],
    input_args: tuple[str],
):
    handler = FFmpegHandler(
        video_codec, audio_codec, container, suffix, list(input_args), list(output_args)
    )
    # asyncio.run(
    #     handler.transcode("/mnt/edit/sources/Community Showcase October 2022/C0591.MP4")
    # )
    handle_transcoding(directory, handler)
    # asyncio.run(handler.build_ffmpeg_invocation("pyproject.toml", "test.mkv"))
