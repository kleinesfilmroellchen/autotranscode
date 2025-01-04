# ffmpeg support tooling

import json
from pathlib import Path
from ffmpeg.asyncio import FFmpeg

UNSUPPORTED_CODECS = ["h264", "avc", "h265", "hevc", "aac"]


async def query_streams(input: Path) -> list[dict]:
    """Queries stream data in the ffprobe format."""
    ffprobe = FFmpeg(executable="ffprobe").input(
        input,
        print_format="json",
        show_streams=None,
    )
    metadata = json.loads(await ffprobe.execute())
    return metadata["streams"]


def get_stream_codecs(stream_data: list[dict]) -> tuple[str | None, str | None]:
    """Extracts the first video and audio codecs from the ffprobe stream data."""
    first_audio, first_video = None, None
    for stream in stream_data:
        if stream["codec_type"] == "video" and first_video is None:
            first_video = stream["codec_name"].strip().lower()
        if stream["codec_type"] == "audio" and first_audio is None:
            first_audio = stream["codec_name"].strip().lower()

    return (first_video, first_audio)


class FFmpegHandler:
    def __init__(
        self,
        video_codec: str,
        audio_codec: str,
        container: str,
        suffix: str,
        input_args: list[str],
        output_args: list[str],
    ):
        self.video_codec = video_codec
        self.audio_codec = audio_codec
        self.container = container
        self.suffix = suffix
        self.input = {}
        for arg in input_args:
            key, value = arg.split("=", maxsplit=1)
            self.input[key] = value
        self.output = {}
        for arg in output_args:
            key, value = arg.split("=", maxsplit=1)
            self.output[key] = value

    def associated_output_name(self, input: Path) -> Path:
        output = input.with_stem(input.stem + self.suffix).with_suffix(
            "." + self.container
        )
        return output

    def is_output_file(self, output: Path) -> bool:
        return output.suffix == '.' + self.container and output.stem.endswith(self.suffix)

    async def transcode(self, input: Path):
        input = Path(input)
        output = self.associated_output_name(input)
        ffmpeg = await self.build_ffmpeg_invocation(input, output)
        await ffmpeg.execute()

    async def build_ffmpeg_invocation(self, input: Path, output: Path) -> FFmpeg:
        streams = await query_streams(input)
        input_video_codec, input_audio_codec = get_stream_codecs(streams)

        if input_audio_codec is None and input_video_codec is None:
            raise Exception(f"{input} is probably not a video file")

        output_video_codec = (
            self.video_codec if input_video_codec in UNSUPPORTED_CODECS else "copy"
        )
        output_audio_codec = (
            self.audio_codec if input_audio_codec in UNSUPPORTED_CODECS else "copy"
        )

        ffmpeg = (
            FFmpeg()
            .option("y")
            .option("v", "warning")
            .input(input, **self.input)
            .output(
                output,
                {
                    "codec:v": output_video_codec,
                    "codec:a": output_audio_codec,
                },
                **self.output,
            )
        )
        print(ffmpeg.arguments)

        return ffmpeg
