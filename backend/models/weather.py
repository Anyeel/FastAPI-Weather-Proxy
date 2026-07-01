from datetime import datetime, timezone

from sqlalchemy import String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class City(Base):
    """
    Represents a city in our database.
    We use lat and lon to uniquely identify the location.
    """
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)

    # One-to-many relationship with automatic lifecycle management of related weather records.
    weather_data: Mapped[list["WeatherInformation"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan"
    )


class WeatherInformation(Base):
    __tablename__ = "weather_information"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign key linking to the city, ondelete to ensure cascade
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))

    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Timestamp tracking when the weather data was fetched from the API.
    # This acts as a cache 'packaging date', allowing the service layer to implement
    # a 3-hour TTL (Time To Live) logic to decide when to refresh the data.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Many-to-one relationship back
    city: Mapped["City"] = relationship(back_populates="weather_data")
