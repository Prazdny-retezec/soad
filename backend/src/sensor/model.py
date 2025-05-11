from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Interval
from sqlalchemy.orm import relationship

from common.enum import ImageFormat
from database import Base


class SensorSettings(Base):
    __tablename__ = "sensor_settings"

    # primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # rgb camera
    rgb_image_quality = Column(Integer)
    rgb_image_count = Column(Integer)
    rgb_image_width = Column(Integer)
    rgb_image_height = Column(Integer)
    rgb_sampling_delay = Column(Integer)
    rgb_image_format = Column(Enum(ImageFormat))

    # multi-spectral camera
    ms_image_count = Column(Integer)
    ms_image_width = Column(Integer)
    ms_image_height = Column(Integer)
    ms_sampling_delay = Column(Integer)
    ms_image_format = Column(Enum(ImageFormat))

    # acoustic emission
    ae_voltage_format = Column(Integer) # AE voltage in Volts: 0=not exported, 1=(int)nV, 2=(int)uV, 3=(float)uV, 4=(float)mV, 5=(float)V. Default=5.
    ae_voltage_dbae = Column(Integer) # AE voltage in dBAE: 0=not exported, 1=exported. Default=0.
    ae_counts_log = Column(Integer)  # AE counts in logarithmic units: 0=not exported, 1=exported. Default=1.
    ae_counts_lin = Column(Integer) # AE counts in linear units: 0=not exported, 1=exported. Default=0.
    ae_energy_format = Column(Integer) # AE energy units: 0=V^2/Hz, 1=uV^2/Hz. Default=1.

    # FK
    measurement_id = Column(Integer, ForeignKey("measurement.id"))

    # relationships
    measurement = relationship("Measurement", back_populates="sensor_settings")
