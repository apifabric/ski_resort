# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 30, 2024 14:25:04
# Database: sqlite:////tmp/tmp.BohZ6pbRUE/ski_resort/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class EquipmentRental(SAFRSBaseX, Base):
    """
    description: Represents rental records for ski equipment.
    """
    __tablename__ = 'equipment_rental'
    _s_collection_name = 'EquipmentRental'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)
    rental_date = Column(DateTime)
    return_date = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)



class SkiInstructor(SAFRSBaseX, Base):
    """
    description: Details about ski instructors employed at the resort.
    """
    __tablename__ = 'ski_instructor'
    _s_collection_name = 'SkiInstructor'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    expertise_level = Column(String, nullable=False)
    hired_date = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    PerformanceReviewList : Mapped[List["PerformanceReview"]] = relationship(back_populates="instructor")
    SkiLessonList : Mapped[List["SkiLesson"]] = relationship(back_populates="instructor")



class SkiResort(SAFRSBaseX, Base):
    """
    description: Represents a ski resort with basic details and operational status.
    """
    __tablename__ = 'ski_resort'
    _s_collection_name = 'SkiResort'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    operational = Column(Boolean)

    # parent relationships (access parent)

    # child relationships (access children)
    CustomerFeedbackList : Mapped[List["CustomerFeedback"]] = relationship(back_populates="resort")
    LiftList : Mapped[List["Lift"]] = relationship(back_populates="resort")
    ResortFacilityList : Mapped[List["ResortFacility"]] = relationship(back_populates="resort")
    SkiEventList : Mapped[List["SkiEvent"]] = relationship(back_populates="resort")
    SkiTrailList : Mapped[List["SkiTrail"]] = relationship(back_populates="resort")
    TicketList : Mapped[List["Ticket"]] = relationship(back_populates="resort")



class CustomerFeedback(SAFRSBaseX, Base):
    """
    description: Collects feedback from customers about their experiences.
    """
    __tablename__ = 'customer_feedback'
    _s_collection_name = 'CustomerFeedback'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    resort_id = Column(ForeignKey('ski_resort.id'), nullable=False)
    feedback = Column(String, nullable=False)
    customer_name = Column(String)

    # parent relationships (access parent)
    resort : Mapped["SkiResort"] = relationship(back_populates=("CustomerFeedbackList"))

    # child relationships (access children)



class Lift(SAFRSBaseX, Base):
    """
    description: Represents lifts within a ski resort.
    """
    __tablename__ = 'lift'
    _s_collection_name = 'Lift'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    resort_id = Column(ForeignKey('ski_resort.id'), nullable=False)

    # parent relationships (access parent)
    resort : Mapped["SkiResort"] = relationship(back_populates=("LiftList"))

    # child relationships (access children)
    MaintenanceLogList : Mapped[List["MaintenanceLog"]] = relationship(back_populates="lift")



class PerformanceReview(SAFRSBaseX, Base):
    """
    description: Details performance reviews of ski instructors.
    """
    __tablename__ = 'performance_review'
    _s_collection_name = 'PerformanceReview'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    review_date = Column(DateTime)
    instructor_id = Column(ForeignKey('ski_instructor.id'), nullable=False)
    comments = Column(String)

    # parent relationships (access parent)
    instructor : Mapped["SkiInstructor"] = relationship(back_populates=("PerformanceReviewList"))

    # child relationships (access children)



class ResortFacility(SAFRSBaseX, Base):
    """
    description: Describes additional facilities available at the resort.
    """
    __tablename__ = 'resort_facility'
    _s_collection_name = 'ResortFacility'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    facility_name = Column(String, nullable=False)
    resort_id = Column(ForeignKey('ski_resort.id'), nullable=False)

    # parent relationships (access parent)
    resort : Mapped["SkiResort"] = relationship(back_populates=("ResortFacilityList"))

    # child relationships (access children)



class SkiEvent(SAFRSBaseX, Base):
    """
    description: Lists events and competitions hosted by the resort.
    """
    __tablename__ = 'ski_event'
    _s_collection_name = 'SkiEvent'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    event_name = Column(String, nullable=False)
    event_date = Column(DateTime, nullable=False)
    resort_id = Column(ForeignKey('ski_resort.id'), nullable=False)

    # parent relationships (access parent)
    resort : Mapped["SkiResort"] = relationship(back_populates=("SkiEventList"))

    # child relationships (access children)



class SkiLesson(SAFRSBaseX, Base):
    """
    description: Catalog of ski lessons provided by the resort.
    """
    __tablename__ = 'ski_lesson'
    _s_collection_name = 'SkiLesson'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    lesson_name = Column(String, nullable=False)
    instructor_id = Column(ForeignKey('ski_instructor.id'), nullable=False)
    difficulty = Column(String)

    # parent relationships (access parent)
    instructor : Mapped["SkiInstructor"] = relationship(back_populates=("SkiLessonList"))

    # child relationships (access children)



class SkiTrail(SAFRSBaseX, Base):
    """
    description: Contains information on each ski trail, including difficulty level.
    """
    __tablename__ = 'ski_trail'
    _s_collection_name = 'SkiTrail'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    resort_id = Column(ForeignKey('ski_resort.id'), nullable=False)

    # parent relationships (access parent)
    resort : Mapped["SkiResort"] = relationship(back_populates=("SkiTrailList"))

    # child relationships (access children)



class Ticket(SAFRSBaseX, Base):
    """
    description: Manages lift tickets sold to customers.
    """
    __tablename__ = 'ticket'
    _s_collection_name = 'Ticket'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    ticket_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    purchase_date = Column(DateTime)
    resort_id = Column(ForeignKey('ski_resort.id'), nullable=False)

    # parent relationships (access parent)
    resort : Mapped["SkiResort"] = relationship(back_populates=("TicketList"))

    # child relationships (access children)



class MaintenanceLog(SAFRSBaseX, Base):
    """
    description: Logs maintenance activities performed on lifts.
    """
    __tablename__ = 'maintenance_log'
    _s_collection_name = 'MaintenanceLog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    maintenance_date = Column(DateTime, nullable=False)
    lift_id = Column(ForeignKey('lift.id'), nullable=False)
    details = Column(String, nullable=False)

    # parent relationships (access parent)
    lift : Mapped["Lift"] = relationship(back_populates=("MaintenanceLogList"))

    # child relationships (access children)
