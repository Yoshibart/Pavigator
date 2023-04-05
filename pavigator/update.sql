LOAD DATA LOCAL INFILE './google_transit_dublinbus/stops.txt'
INTO TABLE main_stopmodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './google_transit_dublinbus/agency.txt'
INTO TABLE main_agencymodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './google_transit_dublinbus/routes.txt'
INTO TABLE main_routemodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@col1, @col2, @col3,@col4,@col5)
SET routeID = @col1,agencyID_id = @col2,routeShortName = @col3,routeLongName = @col4,routeType = @col5;

LOAD DATA LOCAL INFILE './google_transit_dublinbus/calendar.txt'
INTO TABLE main_calendermodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE './google_transit_dublinbus/shapes.txt'
INTO TABLE main_shapemodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@col1, @col2, @col3,@col4,@col5)
SET shapeID = @col1,shapePtLat = @col2,shapePtLon = @col3,shapePtSequence = @col4,shapeDistTravelled = @col5;

LOAD DATA LOCAL INFILE './google_transit_dublinbus/trips.txt'
INTO TABLE main_tripmodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@col1, @col2, @col3,@col4,@col5,@col6)
SET tripID = @col3,shapeID_id = @col4,tripHeadSign = @col5,directionID = @col6,routeID_id = @col1,
serviceID_id = @col2;

LOAD DATA LOCAL INFILE './google_transit_dublinbus/transfers.txt'
INTO TABLE main_transfersmodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@col1, @col2, @col3,@col4)
SET fromStopID_id = @col1, toStopID_id = @col2, transferType = @col3, minTransferTime = @col4;

LOAD DATA LOCAL INFILE './google_transit_dublinbus/stop_times.txt'
INTO TABLE main_stoptimemodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@col1, @col2, @col3,@col4,@col5,@col6,@col7,@col8,@col9)
SET arrivalTime = @col2, scheduledArrivalTime=@col2, departureTime = @col3,stopSequence = @col5,stopHeadSign = @col6,pickUpType = @col7,
dropOffType = @col8,shapeDistTravelled = @col9,stopID_id = @col4,tripID_id = @col1;

LOAD DATA LOCAL INFILE './google_transit_dublinbus/calendar_dates.txt'
INTO TABLE main_calendardatesmodel
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@col1, @col2, @col3)
SET date = @col2,exceptionType = @col3,serviceID_id = @col1;

