CREATE DEFINER=`root`@`localhost` TRIGGER `photo_schema`.`photo_tag_AFTER_INSERT` AFTER INSERT ON `photo_tag` FOR EACH ROW
BEGIN
	IF NEW.tagDescription not in (SELECT description from tag) then
		insert into tag (description) values (NEW.tagDescription);
	END IF;
END