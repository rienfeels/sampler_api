from pydantic import BaseModel

class SampledSongCreate(BaseModel):
    song_name: str
    artist: str
    sampled_song_name: str
    sampled_artist: str

class OpenAIQuery(BaseModel):
    user_input: str
    chat_memory: list

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str