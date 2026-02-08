


-- Script que agregue un usuario nuevo
INSERT INTO lyfter_car_rental."Users" (name, email, username, password, birthday) values ('sebas', 'sebas@gmail.com', 'sebas_s', 'password123', '1993-01-30');

-- Un script que agregue un automovil nuevo
INSERT INTO lyfter_car_rental."Vehicles" (model_id, year, status_id) values (28, 2025, 1)

-- Un script que cambie el estado de un usuario
UPDATE lyfter_car_rental."Users" SET status_id=2 WHERE id =51;

-- Un script que cambie el estado de un automovil
UPDATE lyfter_car_rental."Vehicles" SET status_id=2 WHERE id = 1;

-- Un script que genere un alquiler nuevo con los datos de un usuario y un automovil
INSERT INTO lyfter_car_rental."Rents" (vehicle_id, user_id, status_id) values (52, 51, 1)

-- Un script que confirme la devolución del auto al completar el alquiler, colocando el auto como disponible y completando el estado del alquiler
UPDATE lyfter_car_rental."Rents" SET status_id=5 WHERE id=7;
UPDATE lyfter_car_rental."Vehicles" SET status_id=1 WHERE id=37;

-- Un script que deshabilite un automovil del alquiler
UPDATE lyfter_car_rental."Rents" SET status_id=5 WHERE id= 44;
UPDATE lyfter_car_rental."Vehicles" SET status_id=4 WHERE id =38;

-- Un script que obtenga todos los automoviles alquilados, y otro que obtenga todos los disponibles.
SELECT * FROM lyfter_car_rental."Vehicles" WHERE status_id = 2;
SELECT * FROM lyfter_car_rental."Vehicles" WHERE status_id = 1;