CREATE SCHEMA EMPLOYEE;

CREATE COLUMN TABLE employee.photo(
	pid INT NOT NULL GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
	folder CHAR(10) NOT NULL,
	imgfile CHAR(30) NOT NULL
);
