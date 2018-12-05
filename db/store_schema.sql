DROP TABLE IF EXISTS product;

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TINYTEXT NOT NULL,
  brand TINYTEXT NOT NULL,
  model TINYTEXT NOT NULL,
  image TINYTEXT NOT NULL,
  lens_diameter FLOAT(5,5) NOT NULL,
  bridge_width FLOAT(5,5) NOT NULL,
  side_length FLOAT(5,5) NOT NULL,
  price FLOAT(5,5) NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO product (name, brand, model, image, lens_diameter, bridge_width, side_length, price)
VALUES ("Glasses 1", "Warby Parker", "Benson", "images/image1.jpg", 52, 18, 135, 25 );

INSERT INTO product (name, brand, model, image, lens_diameter, bridge_width, side_length, price)
VALUES ("Glasses 2", "Warby Parker", "Benson", "images/image1.jpg", 50, 17, 130, 20 );

