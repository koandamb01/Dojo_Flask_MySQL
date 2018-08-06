1045. pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: YES/NO)")

1046. Something went wrong (1046, 'No database selected') # No database was select when connecting to the mySQL

1049. pymysql.err.InternalError: (1049, "Unknown database 'sakilamed'") # the database name was incorrect

1064. Running Query: SELECTE * FROM users;
Something went wrong (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'SELECTE * FROM users' at line 1")

1146. Running Query: SELECT * FROM user;
Something went wrong (1146, "Table 'sakila.user' doesn't exist")




-- 
self.encoding = charset_by_name(self.charset).encoding
AttributeError: 'NoneType' object has no attribute 'encoding'



