CREATE TABLE Veh_Inv
(VEHICLE VARCHAR(50),
NO_VEHICLES INT,
);

INSERT INTO Veh_Inv
VALUES('Bikes',2);

INSERT INTO Veh_Inv
VALUES('Cycles',3);

INSERT INTO Veh_Inv
VALUES('Car',1);

INSERT INTO Veh_Inv
VALUES('Boat',2);

select * from Veh_Inv

insert into Veh_Inv(VEHICLE, NO_VEHICLES) values ('abc', )
delete from Veh_Inv where VEHICLE = 'abc'

create table Customer_details
(
Cust_Name varchar(50),
Phone_no varchar(25),
Email nvarchar(30)
)

create table Rental_details
(
Customer_name varchar(50),
Rental_date date,
Return_date date,
Vehicle_type varchar(20)
)