-- Email validation to sent
DELIMITER //
DROP TRIGGER IF EXISTS email_validation//
CREATE TRIGGER email_validation
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0
    END IF;
END//
DELIMITER ;
