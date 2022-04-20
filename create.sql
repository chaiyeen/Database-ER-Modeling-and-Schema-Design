drop table if exists Item;
drop table if exists Category;
drop table if exists Person;
drop table if exists BidInfo;

create table Category(
  catID INT,
  ItemID INT,
  categoryName varchar(256),
  
  Primary key(catID),
  Foreign key(ItemID) references Item(ItemID)
);

create table Person(
  UserID varchar(256),
  Rating INT,
  Location varchar(256),
  Country varchar(256),
  
  Primary key(UserID)
);

create table BidInfo(
  BidID INT,
  ItemID INT,
  Bidder varchar(256),
  Amount money,
  Time datetime,
  
  Primary key(BidID),
  Foreign Key (Bidder) references Person(UserID),
  Foreign key (ItemID) references Item(ItemID)
);

create table Item(
  ItemID INT,
  Name varchar(256),
  CurrPrice money,
  Buy_Price money,
  FirstBid money,
  Number_of_Bids INT,
  Started datetime,
  Ends datetime,
  SellerID varchar(256),
  Description varchar(256),
  
  Primary key (ItemID),
  Foreign key (SellerID) references Person(UserID)
);
