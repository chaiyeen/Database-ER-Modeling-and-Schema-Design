drop table if exists Category;

create table Category(
    ItemID int,
    subCategory varchar(256),
    Primary Key(ItemID, subCategory)
);
