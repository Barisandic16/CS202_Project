INSERT INTO User (user_id, username, password, name) VALUES
(1001, 'ahmet', '123', 'Ahmet Fırat'),
(1002, 'aden', '123', 'Aden Duru Çelik'),
(1003, 'baris', '123', 'Orgeneral Barış Andiç'),
(1004, 'berkin', '0000', 'Berkin Karakoç'),
(1005, 'musteri1', 'musteri1', 'musteri1'),
(1006, 'musteri', 'musteri', 'musteri'),
(1007, 'musteri99', 'musteri99', 'Müşteri Deneme'),
(1008, 'musteri0', 'musteri0', 'Müşteri Deneme 2'),
(1009, 'zeynep', '123', 'Zeynep'),
(1010, 'fatma', '123', 'Fatma');

INSERT INTO Customer (customer_id, user_id) VALUES
(2001, 1004), (2002, 1005), (2003, 1006), (2004, 1007), (2005, 1008);

INSERT INTO Manager (manager_id, user_id) VALUES
(3001, 1001), (3002, 1002), (3003, 1003), (3004,1009), (3005,1010);

INSERT INTO Phone_Number (number, country_code, user_id) VALUES
('5551231', '+90', 1001), ('5551232', '+90', 1002), ('5551233', '+90', 1003),
('5554561', '+90', 1004), ('5554562', '+90', 1005), ('5554563', '+90', 1006),
('5554564', '+90', 1007), ('5554565', '+90', 1008);

INSERT INTO Address (street, city, postal_code, user_id) VALUES
('Karaköprü Semt Lokantası', 'Şanlıurfa', '4001', 1001),
('Özyeğin Yurt 3', 'İstanbul', '4002', 1002),
('Bademli', 'Bursa', '4003', 1003),
('Artvin Merkez', 'Artvin', '4004', 1004),
('Bursa', 'Bursa', '4005', 1005);

INSERT INTO Restaurant (restaurant_id, name, adress, cuisine_type, manager_id) VALUES
(5001, 'Çiğköfteci Ahmet Usta', 'Karaköprü', 'Urfa', 3001),
(5002, 'İnari', 'Bebek', 'Japon', 3002),
(5003, 'BARIS-TA', 'Mustafa Kemal Atatürk Caddesi', 'Türk', 3003),
(5004, 'Lahmacuncu Ahmet Usta', 'Karaköprü', 'Urfa', 3004),
(5005, 'Emek Mantı', 'Bağdat Caddesi', 'Türk', 3005);

INSERT INTO Keyword (keyword_id, key_text, manager_id, restaurant_id) VALUES
(9001, 'cigkofte', 3001, 5001), (9002, 'urfa', 3001, 5001),
(9003, 'suşi', 3002, 5002), (9004, 'kahve', 3003, 5003),
(9005, 'lahmacun', 3004, 5004), (9006, 'manti', 3005, 5005);

INSERT INTO MenuItem (item_id, name, description, price, image, dis_percentage, dis_end_date, restaurant_id) VALUES
(6001, 'Etli Çiğköfte', 'Orijinal Çiğköfte', 13.40, 'cigkofte.jpg', 19.62, '2025-04-25', 5001),
(6002, 'Etsiz Çiğköfte', 'Adıyaman Çiğköftesi', 14.13, 'etsiz.jpg', 10.29, '2025-04-16', 5001),
(6003, 'Kaliforniya Roll', 'Yeni başlayanlar için', 9.90, 'kal.jpg', 19.04, '2025-05-02', 5002),
(6004, 'Tarabya Roll', 'Etli suşi', 14.31, 'tarabya.jpg', 15.38, '2025-05-04', 5002),
(6005, 'Yerba Mate', 'Güney Amerika Çayı', 15.58, 'mate.jpg', NULL, '2025-04-26', 5003),
(6006, 'Latte', 'Sütlü kahve', 10.31, 'latte.jpg', NULL, '2025-04-23', 5003),
(6007, 'Lahmacun', 'Urfa Lahmacunu', 12.94, 'lahmacun.jpg', NULL, '2025-05-10', 5004),
(6008, 'Urfa Kebap', 'Bulgur Pilavı ile birlikte', 11.32, 'kebap.jpg', NULL, '2025-05-05', 5004),
(6009, 'Sinop Mantı', 'İçi boş', 14.40, 'sinopmanti.jpg', 16.81, '2025-04-27', 5005),
(6010, 'Hangel', 'Terekeme Mantısı', 12.64, 'hangel.jpg', 18.11, '2025-04-16', 5005),
(6011, 'Bol Acılı', 'Favorimiz', 10.68, 'acılı.jpg', 10.37, '2025-04-23', 5001),
(6012, 'Onikiri', 'Aynısının üçgeni', 8.62, 'onikiri.jpg', NULL, '2025-04-20', 5002),
(6013, 'Ice White Chocolate Mocha', 'Ice White Chocolate Mocha', 15.86, 'iwcm.jpg', NULL, '2025-05-09', 5003),
(6014, 'Antep Lahmacun', 'Sarımsaklı', 12.55, 'antep.jpg', NULL, '2025-04-19', 5004),
(6015, 'Kayseri Mantısı', 'Kayseri Mantısı', 14.18, 'kayseri.jpg', 10.99, '2025-05-06', 5005);

INSERT INTO Cart (cart_id, customer_id, restaurant_id, quantity, status, timestamp, item_id) VALUES
(7001, 2001, 5001, 4, 'preparing', NOW(), 6001),
(7002, 2002, 5002, 5, 'accepted', NOW(), 6003),
(7003, 2003, 5003, 1, 'preparing', NOW(), 6005),
(7004, 2004, 5004, 2, 'sent', NOW(), 6007),
(7005, 2005, 5005, 1, 'delivered', NOW(), 6009),
(7006, 2001, 5001, 8, 'preparing', NOW(), 6011),
(7007, 2002, 5002, 5, 'accepted', NOW(), 6004),
(7008, 2003, 5003, 3, 'sent', NOW(), 6006),
(7009, 2004, 5004, 2, 'preparing', NOW(), 6008),
(7010, 2005, 5005, 2, 'delivered', NOW(), 6010);

INSERT INTO Rating (rating_id, rate, comment, customer_id, restaurant_id, cart_id) VALUES
(8001, 5, 'Çok güzeldi', 2001, 5001, 7001),
(8002, 4, 'Tuzu eksikti ama olsun', 2002, 5001, 7006),
(8003, 5, 'Çok güzel ancak çok pahalı', 2003, 5001, 7001),
(8004, 5, 'Fena', 2004, 5001, 7001),
(8005, 4, 'Harikaydı', 2005, 5001, 7006),
(8006, 5, 'Fiyat performans', 2001, 5001, 7001),
(8007, 4, 'Kalite', 2002, 5001, 7006),
(8008, 5, 'Çok sıcaktı ama güzeldi', 2003, 5001, 7001),
(8009, 5, 'Standart', 2004, 5001, 7001),
(8010, 4, 'Tuzu azdı', 2005, 5001, 7006),
(8011, 5, 'Mükemmel', 2001, 5002, 7002),
(8012, 5, 'Porsiyonları fazla', 2002, 5002, 7002),
(8013, 4, 'Başarılı', 2003, 5002, 7007),
(8014, 3, 'İdare eder ama promosyonla gidiyor', 2004, 5002, 7007),
(8015, 5, 'Süper', 2005, 5002, 7002),
(8016, 4, 'Başarılı', 2001, 5002, 7002),
(8017, 5, 'Çok güzeldi', 2002, 5002, 7007),
(8018, 5, 'Sevdim', 2003, 5002, 7002),
(8019,4,'Lezzetli',2002,5002,7002),
(8020,3,'Ortalama',2002,5002,7007),
(8021,5,'Mükemmel',2003,5003,7003),
(8022,4,'Güzel',2003,5003,7008),
(8023,5,'Harika',2003,5003,7003),
(8024,3,'İdare eder',2003,5003,7008),
(8025,4,'Beğendim',2003,5003,7003),
(8026,2,'Beklediğim gibi değil',2003,5003,7008),
(8027,5,'Tavsiye ederim',2003,5003,7003),
(8028,4,'Tat olarak iyi',2003,5003,7008),
(8029,5,'Sıcak ve taze',2003,5003,7003),
(8030,3,'Fiyat biraz yüksek',2003,5003,7008),
(8031,5,'Lezzet şahane',2004,5004,7004),
(8032,4,'Güzeldi',2004,5004,7009),
(8033,4,'Doyurucu',2004,5004,7004),
(8034,3,'Hafif baharatlı',2004,5004,7009),
(8035,5,'Favorim oldu',2004,5004,7004),
(8036,2,'Beklediğim gibi değil',2004,5004,7009),
(8037,5,'Tekrar alırım',2004,5004,7004),
(8038,4,'Lezzet dengesi iyiydi',2004,5004,7009),
(8039,5,'Sıcak geldi',2004,5004,7004),
(8040,3,'Sunum zayıftı',2004,5004,7009),
(8041,5,'Mükemmel',2005,5005,7005),
(8042,4,'Lezzetli',2005,5005,7010),
(8043,4,'Doyurucu',2005,5005,7005),
(8044,3,'Baharat oranı yüksek',2005,5005,7010),
(8045,5,'Favori yemek',2005,5005,7005),
(8046,2,'Çok tuzluydu',2005,5005,7010),
(8047,5,'Taze ve sıcak',2005,5005,7005),
(8048,4,'Kesinlikle öneririm',2005,5005,7010),
(8049,5,'Hızlı servis',2005,5005,7005),
(8050,3,'Fiyat yüksek',2005,5005,7010);

