WITH temp AS (SELECT ItemID FROM Category GROUP BY ItemID HAVING COUNT(CategoryName)=4)
SELECT COUNT(*) FROM temp;