# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship
import datetime

# Define the database engine
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite', echo=False)

# Create a base class for the models
Base = declarative_base()

class SkiResort(Base):
    """
    description: Represents a ski resort with basic details and operational status.
    """
    __tablename__ = 'ski_resort'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    operational = Column(Boolean, default=True)

class SkiTrail(Base):
    """
    description: Contains information on each ski trail, including difficulty level.
    """
    __tablename__ = 'ski_trail'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    resort_id = Column(Integer, ForeignKey('ski_resort.id'), nullable=False)

class Lift(Base):
    """
    description: Represents lifts within a ski resort.
    """
    __tablename__ = 'lift'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    resort_id = Column(Integer, ForeignKey('ski_resort.id'), nullable=False)

class SkiInstructor(Base):
    """
    description: Details about ski instructors employed at the resort.
    """
    __tablename__ = 'ski_instructor'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    expertise_level = Column(String, nullable=False)
    hired_date = Column(DateTime, default=datetime.datetime.now)

class SkiLesson(Base):
    """
    description: Catalog of ski lessons provided by the resort.
    """
    __tablename__ = 'ski_lesson'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_name = Column(String, nullable=False)
    instructor_id = Column(Integer, ForeignKey('ski_instructor.id'), nullable=False)
    difficulty = Column(String)

class EquipmentRental(Base):
    """
    description: Represents rental records for ski equipment.
    """
    __tablename__ = 'equipment_rental'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    rental_date = Column(DateTime, default=datetime.datetime.now)
    return_date = Column(DateTime, nullable=True)

class SkiEvent(Base):
    """
    description: Lists events and competitions hosted by the resort.
    """
    __tablename__ = 'ski_event'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String, nullable=False)
    event_date = Column(DateTime, nullable=False)
    resort_id = Column(Integer, ForeignKey('ski_resort.id'), nullable=False)

class Ticket(Base):
    """
    description: Manages lift tickets sold to customers.
    """
    __tablename__ = 'ticket'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    purchase_date = Column(DateTime, default=datetime.datetime.now)
    resort_id = Column(Integer, ForeignKey('ski_resort.id'), nullable=False)

class PerformanceReview(Base):
    """
    description: Details performance reviews of ski instructors.
    """
    __tablename__ = 'performance_review'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_date = Column(DateTime, default=datetime.datetime.now)
    instructor_id = Column(Integer, ForeignKey('ski_instructor.id'), nullable=False)
    comments = Column(String)

class MaintenanceLog(Base):
    """
    description: Logs maintenance activities performed on lifts.
    """
    __tablename__ = 'maintenance_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    maintenance_date = Column(DateTime, nullable=False)
    lift_id = Column(Integer, ForeignKey('lift.id'), nullable=False)
    details = Column(String, nullable=False)

class ResortFacility(Base):
    """
    description: Describes additional facilities available at the resort.
    """
    __tablename__ = 'resort_facility'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    facility_name = Column(String, nullable=False)
    resort_id = Column(Integer, ForeignKey('ski_resort.id'), nullable=False)

class CustomerFeedback(Base):
    """
    description: Collects feedback from customers about their experiences.
    """
    __tablename__ = 'customer_feedback'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resort_id = Column(Integer, ForeignKey('ski_resort.id'), nullable=False)
    feedback = Column(String, nullable=False)
    customer_name = Column(String)

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a session for adding sample data
Session = sessionmaker(bind=engine)
session = Session()

# Sample data entries
resort1 = SkiResort(name='Alpine Haven', location='Colorado', operational=True)
resort2 = SkiResort(name='Winter Wonderland', location='Utah', operational=False)
session.add_all([resort1, resort2])

trail1 = SkiTrail(name='Black Diamond', difficulty='Expert', resort_id=1)
trail2 = SkiTrail(name='Bunny Slope', difficulty='Beginner', resort_id=1)
trail3 = SkiTrail(name='Sunny Path', difficulty='Intermediate', resort_id=2)
session.add_all([trail1, trail2, trail3])

lift1 = Lift(name='Summit Express', capacity=200, resort_id=1)
lift2 = Lift(name='Snowflake Lift', capacity=100, resort_id=2)
session.add_all([lift1, lift2])

instructor1 = SkiInstructor(name='John Smith', expertise_level='Advanced')
instructor2 = SkiInstructor(name='Jane Doe', expertise_level='Intermediate')
session.add_all([instructor1, instructor2])

lesson1 = SkiLesson(lesson_name='Intro to Skiing', instructor_id=1, difficulty='Beginner')
lesson2 = SkiLesson(lesson_name='Advanced Tricks', instructor_id=2, difficulty='Expert')
session.add_all([lesson1, lesson2])

rental1 = EquipmentRental(customer_name='Alice Brown', rental_date=datetime.datetime(2023, 12, 1))
rental2 = EquipmentRental(customer_name='Charlie White', rental_date=datetime.datetime(2023, 12, 2), return_date=datetime.datetime(2023, 12, 5))
session.add_all([rental1, rental2])

event1 = SkiEvent(event_name='Annual Downhill', event_date=datetime.datetime(2023, 2, 20), resort_id=1)
event2 = SkiEvent(event_name='Freestyle Showcase', event_date=datetime.datetime(2023, 3, 15), resort_id=2)
session.add_all([event1, event2])

ticket1 = Ticket(ticket_type='Full Day', price=120.00, resort_id=1)
ticket2 = Ticket(ticket_type='Half Day', price=80.00, resort_id=2)
session.add_all([ticket1, ticket2])

review1 = PerformanceReview(review_date=datetime.datetime(2023, 10, 10), instructor_id=1, comments='Exceeds expectations')
review2 = PerformanceReview(review_date=datetime.datetime(2023, 11, 12), instructor_id=2, comments='Good performance')
session.add_all([review1, review2])

log1 = MaintenanceLog(maintenance_date=datetime.datetime(2023, 9, 5), lift_id=1, details='Replaced cables')
log2 = MaintenanceLog(maintenance_date=datetime.datetime(2023, 10, 22), lift_id=2, details='Routine check-up')
session.add_all([log1, log2])

facility1 = ResortFacility(facility_name='Ice Skating Rink', resort_id=1)
facility2 = ResortFacility(facility_name='Spa', resort_id=2)
session.add_all([facility1, facility2])

feedback1 = CustomerFeedback(resort_id=1, feedback='Amazing experience, will return!', customer_name='Tom Green')
feedback2 = CustomerFeedback(resort_id=2, feedback='Not fully operational but great snow.', customer_name='Sue Blue')
session.add_all([feedback1, feedback2])

# Commit the session to the database
session.commit()
