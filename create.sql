drop table if exists Item;
drop table if exists Category;
drop table if exists Person;
drop table if exists BidInfo;

create table Category(
  ItemID int,
  categoryName varchar(256)
);
