# ChatGPT Stream Game

A text-based game in a twitch stream. ChatGPT outputs something, and then twitch chat sends messages to control what happens next (one chat message gets picked at random).

## Setup

Install dependencies: `python3 -m pip install -r requirements.txt`

Copy `.env.` to `.env.local`, and add fill it.

You'll need:

-   An openai api key https://platform.openai.com/account/api-keys
-   A twitch token (Bot Chat Token) https://twitchtokengenerator.com/
-   Obs password: in obs, select Tools -> WebSocket Server Settings -> Show Connect Info
    -   Also turn on `Enable WebSocket Server`, and change the port to `4455`.

### Obs setup

You'll also need to setup some elements in OBS.

-   A text element for the subtitles. See `app.py` for which names to use (either `Game Text` or `Game Text Raiden` by default).
-   For TTS audio: a media source named `Game TTS Audio`. The source should play from file, but the app will set that setting so no need to tweak any settings there.

## Usage

`python3 src/app.py`

You will likely need some basic python skills in order to make anything useful out of this: do not expect to turn it on and win at life.

## Example streams and their shortcomings

See the vods at https://twitch.tv/timeloopgame . There's two games: a zombie game and metal gear game.

The zombie game has better gameplay, but text based games are not easy to attract people to get into. Thus I also quickly tried a MG radio scene, but the gameplay of that was too boring for me.

## Further exploration

Mostly a good text based game will be about the prompt. I've included my prompts in the repo.

You'd want to use a good TTS and not the crappy google TTS that's currently being used. But that kind of TTS is expensive (at least elevenlabs is).
