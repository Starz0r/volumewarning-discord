import tempfile
import os
from pathlib import Path

from pydub import AudioSegment
import discord


class VolumeWarning(discord.Client):
    async def on_ready(self):
        print("Logged In.")

    async def on_message(self, msg):
        for attachment in msg.attachments:
            # if the attachment has no type just return immediately as it won't be embedded
            if attachment.content_type is None:
                return

            # get the mimetype and check if it's a video or audio media
            mimetype = attachment.content_type.split("/")
            if arr_contains(mimetype, "video") or arr_contains(mimetype, "audio"):

                # create a temporary directory and store the file
                tempdir = tempfile.mkdtemp()
                await attachment.save(tempdir / Path(attachment.filename), use_cached=True)

                # check if the max dB of the audio is too high
                audseg = AudioSegment.from_file(tempdir / Path(attachment.filename))
                if audseg.max_dBFS >= -6.0:
                    await msg.reply("ATTENTION: The attached media to the linked message contains audio that goes way above normal hearing, and it is recommended you turn down the volume or don't watch at all!", mention_author=False)
                elif audseg.max_dBFS >= -9.0:
                    await msg.reply("Warning: The attached media to the linked message contains audio that may be harmful to ones hearing, and it is recommended you turn down the volume before watching", mention_author=False)
                elif audseg.max_dBFS >= -12.0:
                    await msg.reply("Caution: The attached media to the linked message contains audio that goes above the normal hearing ranges and might be harsh on the ears.", mention_author=False)


def arr_contains(arr, match):
    for string in arr:
        if string == match:
            return True
    return False


def main():
    client = VolumeWarning()
    client.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
