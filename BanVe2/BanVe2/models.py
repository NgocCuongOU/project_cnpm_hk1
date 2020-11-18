from sqlalchemy import Column, Integer, Float, String,ForeignKey,Boolean,Date,Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin, current_user, logout_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect
from enum import Enum as UserEnum
from BanVe2 import db, admin


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class UserRole(UserEnum):
    USER = 1
    ADMIN = 2

class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_name = Column(String(50), nullable=False)
    user_password = Column(String(50), nullable=False)
    user_active = Column(Boolean, default=True)
    joined_date = Column(Date, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name

prod_flight = db.Table('prod_flight',
                       Column('airport_id', Integer, ForeignKey('air_port.id'), primary_key=True),
                       Column('flight_id', Integer, ForeignKey('flight_details.id'), primary_key=True))

class Airport(db.Model):

    __tablename__ = "air_port"

    id = Column(Integer, primary_key=True, autoincrement=True)
    air_name = Column(String(100), nullable=False)
    place = Column(String(100), nullable=False)
    stop_time = Column(Integer, default=0)

    air_flight = relationship('FlightDetails', secondary = 'prod_flight', lazy = 'subquery', backref = db.backref('airflight', lazy=True) )

    def __str__(self):
        return self.air_name



class PreOderTicket(db.Model):

    __tablename__ = "preoder_ticket"

    id = Column(Integer, primary_key=True, autoincrement=True)
    passenger_name = Column(String(50), nullable=False)
    identity_num = Column(Float, nullable=False)
    phone = Column(Integer, nullable=False)
    ticket_class = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    date_oder = Column(Date, nullable=False)
    flight = relationship ('FlightDetails', backref = 'flight', lazy = True)


    def __str__(self):
        return self.passenger_name

class FlightDetails(db.Model):

    __tablename__ = "flight_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_name = Column(String(100), nullable=False)
    from_name = Column(String(50), nullable=False)
    destination =  Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    time_to_arrived = Column(Integer, nullable=False)
    economy_class = Column(Integer, nullable=False)
    business_class = Column(Integer, nullable=False)
    empty_seat = Column(Integer, nullable=False)
    od_seat = Column(Integer, nullable=False)

    id_flight = Column(Integer, ForeignKey(PreOderTicket.id), nullable=True)

    def __str__(self):
        return self.flight_name



class TicketDetails(db.Model):

    __tablename__ = "ticket_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_preoder = Column(Integer, ForeignKey(PreOderTicket.id), nullable=False)


    def __str__(self):
        return self.id_preoder.__str__()

#========================================================
#===================Model Views==========================

class UserModelView(AuthenticatedView):
    column_display_pk = True
    can_create = True
    can_edit = True
    can_export = True
    pass

class FlightDetailsModelView(AuthenticatedView):
    column_display_pk = True
    can_create = True
    can_edit = True
    can_export = True
    pass

class TicketDetailsModelView(AuthenticatedView):
    column_display_pk = True
    can_create = True
    can_edit = True
    can_export = True
    pass

class PreOderTicketModelView(AuthenticatedView):
    column_display_pk = True
    can_create = True
    can_edit = True
    can_export = True
    pass

class AirportModelView(AuthenticatedView):
    column_display_pk = True
    can_create = True
    can_edit = True
    can_export = True
    pass

#========================================================
#========================================================

class AboutUsView(BaseView):
    @expose('/')
    def __index__(self):
        return self.render('admin/about-us.html')

    def is_accessible(self):
        return current_user.is_authenticated
    pass

class LogoutAdminView(BaseView):
    @expose("/")
    def __index__(self):
        logout_user()
        return redirect("/admin")
    def is_accessible(self):
        return current_user.is_authenticated

#========================================================
#========================================================
admin.add_view(UserModelView(User, db.session))
admin.add_view(FlightDetailsModelView(FlightDetails, db.session))
admin.add_view(TicketDetailsModelView(TicketDetails, db.session))
admin.add_view(PreOderTicketModelView(PreOderTicket, db.session))
admin.add_view(AirportModelView(Airport, db.session))

admin.add_view(AboutUsView(name="About Us"))
admin.add_view(LogoutAdminView(name="Logout"))

#========================================================
#========================================================

if __name__ == "__main__":
    db.create_all()
