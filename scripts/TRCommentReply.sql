/* TRIGGER UTILIZADA PARA VALIDAR SE O VALOR INSERIDO NA COLUNA
reply_to FAZ REFERÊNCIA A UM COMENTÁRIO JÁ EXISTENTE.

RETORNOS:
		ID JÁ EXISTE = INSERE COM SUCESSO.
		REPLY_TO IS NULL = INSERE COM SUCESSO.
		ID NÃO EXISTE = GERA UM ERRO. */

DROP TRIGGER IF EXISTS `db`.`TRCommentReply`;

DELIMITER $$
USE `db`$$
CREATE TRIGGER `db`.`TRCommentReply` BEFORE INSERT ON `core_comment` FOR EACH ROW
return_label:
BEGIN
	DECLARE validator INT;

    IF new.reply_to IS null THEN
         LEAVE return_label;
    END IF;

	  SELECT
		  COUNT(*)
	  INTO validator FROM
		  core_comment
	  WHERE
		  id = NEW.reply_to;

	  IF validator = 0 THEN
        signal sqlstate '45000' set message_text = 'Error: Comentário informado não existe!';
	  END IF;
END$$
DELIMITER ;