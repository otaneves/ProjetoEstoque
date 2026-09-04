CREATE DATABASE  IF NOT EXISTS `estoque` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `estoque`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: estoque
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `movimentacoes`
--

DROP TABLE IF EXISTS `movimentacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimentacoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `produto_id` int NOT NULL,
  `nome_produto` varchar(100) DEFAULT NULL,
  `usuario_id` int NOT NULL,
  `nome_usuario` varchar(100) DEFAULT NULL,
  `tipo` enum('ENTRADA','SAIDA') NOT NULL,
  `quantidade` int NOT NULL,
  `data_movimentacao` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `produto_id` (`produto_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `movimentacoes_ibfk_1` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`),
  CONSTRAINT `movimentacoes_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentacoes`
--

LOCK TABLES `movimentacoes` WRITE;
/*!40000 ALTER TABLE `movimentacoes` DISABLE KEYS */;
INSERT INTO `movimentacoes` VALUES (13,9,'PowerBank 10000mAh',2,'Victória','ENTRADA',15,'2026-08-14 14:57:27'),(14,9,'PowerBank 10000mAh',2,'Victória','SAIDA',5,'2026-08-14 14:59:25'),(15,11,'Caderno Tilibra',1,'Otavio','ENTRADA',20,'2026-08-14 22:05:02'),(16,11,'Caderno Tilibra',1,'Otavio','SAIDA',20,'2026-08-14 22:05:52'),(17,11,'Caderno Tilibra',2,'Victória','ENTRADA',20,'2026-08-14 22:07:11'),(18,11,'Caderno Tilibra',2,'Victória','ENTRADA',21,'2026-08-14 22:07:25'),(19,2,'Mochila',1,'Otávio','ENTRADA',20,'2026-09-01 02:11:44'),(20,1,'Mouse Gamer',1,'Otávio','SAIDA',100,'2026-09-01 02:27:15'),(21,1,'Mouse Gamer',2,'Victória','ENTRADA',10,'2026-09-01 02:27:56'),(22,1,'Mouse Gamer',1,'Otávio','ENTRADA',5,'2026-09-01 02:29:20'),(23,1,'Mouse Gamer',2,'Victória','ENTRADA',5,'2026-09-01 02:32:19'),(24,1,'Mouse Gamer',2,'Victória','SAIDA',10,'2026-09-01 02:32:34');
/*!40000 ALTER TABLE `movimentacoes` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `preencher_dados_movimentacao` BEFORE INSERT ON `movimentacoes` FOR EACH ROW BEGIN

    DECLARE nomeProdutoTemp VARCHAR(50);
    DECLARE nomeUsuarioTemp VARCHAR(100);

    SELECT nome
    INTO nomeProdutoTemp
    FROM produtos
    WHERE id = NEW.produto_id;

    SELECT nome
    INTO nomeUsuarioTemp
    FROM usuarios
    WHERE id = NEW.usuario_id;

    SET NEW.nome_produto = nomeProdutoTemp;
    SET NEW.nome_usuario = nomeUsuarioTemp;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `valor_compra` decimal(10,2) DEFAULT NULL,
  `valor_venda` decimal(10,2) NOT NULL,
  `quantidade` int NOT NULL DEFAULT '0',
  `quantidade_minima` int NOT NULL DEFAULT '0',
  `ativo` enum('S','N') NOT NULL DEFAULT 'S',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Mouse Gamer',75.00,150.00,10,5,'S'),(2,'Mochila',30.00,65.00,20,15,'S'),(3,'Notebook Gamer',1000.00,2000.00,8,5,'S'),(4,'Monitor Gamer',900.00,1500.00,5,2,'S'),(5,'Televisão Samsung',1500.00,2500.00,3,3,'S'),(6,'Caixa de Som',150.00,500.00,10,3,'S'),(9,'PowerBank 10000mAh',30.00,80.00,10,10,'S'),(10,'Caderno LogiTech',15.00,30.00,0,5,'S'),(11,'Caderno Tilibra',8.00,30.00,41,5,'S'),(12,'Caderno LogiTech',15.00,30.00,0,5,'S'),(13,'Caderno LogiTech',15.00,30.00,0,5,'N'),(14,'Samsung S22',1500.00,3000.00,0,1,'S'),(15,'Moletom Pichau',100.00,130.00,0,15,'S');
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `celular` varchar(11) NOT NULL,
  `data_nascimento` date DEFAULT (curdate()),
  `cpf` varchar(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `perfil` enum('admin','comum') NOT NULL,
  `data_cadastro` date DEFAULT (curdate()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `cpf` (`cpf`),
  UNIQUE KEY `cpf_2` (`cpf`),
  UNIQUE KEY `celular` (`celular`),
  UNIQUE KEY `celular_2` (`celular`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Otávio','12345678910','2006-01-10','12345678910','otavio@gmail.com','1234','admin','2026-08-18'),(2,'Victória','12345678911','2007-05-08','12345678911','vic@gmail.com','5678','admin','2026-08-18'),(5,'Mirela','12345678913','1973-10-03','12345678913','mirela@gmail.com','1001','admin','2026-08-18'),(11,'Guilherme','12345678900','2010-09-17','12345678900','gui@gmail.com','0000','comum','2026-08-21'),(12,'Patricia','12345678912','2005-01-01','12345678912','paty@gmail.com','0123','comum','2026-08-21');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'estoque'
--

--
-- Dumping routines for database 'estoque'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-04 15:20:29
