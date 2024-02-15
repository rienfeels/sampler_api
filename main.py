from fastapi import FastAPI, HTTPException
from databases import Database
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import SampledSongCreate

DATABASE_URL = "postgresql://postgres:@localhost/sampler_api"

Base = declarative_base()
metadata = MetaData()

class SampledSongs(Base):
    __tablename__ = "sampled_songs"

    id = Column(Integer, primary_key=True, index=True)
    song_name = Column(String, index=True)
    artist = Column(String)
    sampled_song_name = Column(String)
    sampled_artist = Column(String)

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()



@app.post("/sampled-songs/", response_model=SampledSongCreate)
def create_sampled_song(sampled_song: SampledSongCreate):
    db_sampled_song = SampledSongs(**sampled_song.model_dump())
    with SessionLocal() as db:
        try:
            db.add(db_sampled_song)
            db.commit()
            db.refresh(db_sampled_song)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating sampled song: {str(e)}")

    return sampled_song

@app.get("/sampled-songs/{song_name}")
def get_sampled_songs(song_name: str):
    with SessionLocal() as db:
        sampled_songs = db.query(SampledSongs).filter(SampledSongs.song_name == song_name).all()

    if not sampled_songs:
        raise HTTPException(status_code=404, detail="Song not found")

    return sampled_songs