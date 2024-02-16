from sqlalchemy import *
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Wagon(Base):  # wagon
    __tablename__ = 'wagons'

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    train = relationship("Train", back_populates="wagons")

    current_station_id = Column(Integer, ForeignKey("stations.id"))
    target_station_id = Column(Integer, ForeignKey("stations.id"))
    ts = Column(DateTime, nullable=False)

    current_station = relationship("Station", back_populates="wagons", foreign_keys=[current_station_id])
    target_station = relationship("Station", back_populates="wagons", foreign_keys=[target_station_id])


class Train(Base):
    __tablename__ = 'trains'

    id = Column(Integer, primary_key=True)

    start_station_id = Column(Integer, ForeignKey("stations.id"))
    current_station_id = Column(Integer, ForeignKey("stations.id"))
    end_station_id = Column(Integer, ForeignKey("stations.id"))

    start_station = relationship("Station", back_populates="trains", foreign_keys=[start_station_id])
    current_station = relationship("Station", back_populates="trains", foreign_keys=[current_station_id])
    end_station = relationship("Station", back_populates="trains", foreign_keys=[end_station_id])

    ts = Column(DateTime, nullable=False)

    wagons = relationship("Wagon", back_populates="train")


class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    trains = relationship("Train", back_populates="current_station", foreign_keys="[Train.current_station_id]")
    wagons = relationship("Wagon", back_populates="current_station", foreign_keys="[Wagon.current_station_id]")


class StationConnection(Base):
    __tablename__ = 'station_connections'

    id = Column(Integer, primary_key=True)

    from_station = Column(Integer, ForeignKey("stations.id"))
    to_station = Column(Integer, ForeignKey("stations.id"))

    length = Column(Integer, nullable=False)
