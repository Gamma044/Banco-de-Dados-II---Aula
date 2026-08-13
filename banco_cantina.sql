-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: cantina
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aluno`
--

DROP TABLE IF EXISTS `aluno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aluno` (
  `id_aluno` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `matricula` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_aluno`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aluno`
--

LOCK TABLES `aluno` WRITE;
/*!40000 ALTER TABLE `aluno` DISABLE KEYS */;
INSERT INTO `aluno` VALUES (1,'GABRIEL','1'),(2,'CARLOS','2');
/*!40000 ALTER TABLE `aluno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `atendente`
--

DROP TABLE IF EXISTS `atendente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `atendente` (
  `id_atendente` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id_atendente`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atendente`
--

LOCK TABLES `atendente` WRITE;
/*!40000 ALTER TABLE `atendente` DISABLE KEYS */;
INSERT INTO `atendente` VALUES (1,'Lucas');
/*!40000 ALTER TABLE `atendente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gerente`
--

DROP TABLE IF EXISTS `gerente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gerente` (
  `id_gerente` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id_gerente`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gerente`
--

LOCK TABLES `gerente` WRITE;
/*!40000 ALTER TABLE `gerente` DISABLE KEYS */;
INSERT INTO `gerente` VALUES (1,'Pedro');
/*!40000 ALTER TABLE `gerente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_pedido`
--

DROP TABLE IF EXISTS `item_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_pedido` (
  `id_item` int(11) NOT NULL AUTO_INCREMENT,
  `quantidade` int(11) NOT NULL,
  `preco_unitario` decimal(10,2) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `id_produto` int(11) NOT NULL,
  PRIMARY KEY (`id_item`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_produto` (`id_produto`),
  CONSTRAINT `item_pedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`),
  CONSTRAINT `item_pedido_ibfk_2` FOREIGN KEY (`id_produto`) REFERENCES `produto` (`id_produto`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_pedido`
--

LOCK TABLES `item_pedido` WRITE;
/*!40000 ALTER TABLE `item_pedido` DISABLE KEYS */;
INSERT INTO `item_pedido` VALUES (2,9,10.00,2,2),(3,9,10.00,2,2),(4,4,5.50,2,1);
/*!40000 ALTER TABLE `item_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pedido` (
  `id_pedido` int(11) NOT NULL AUTO_INCREMENT,
  `horario` datetime NOT NULL,
  `forma_pagamento` varchar(30) NOT NULL,
  `id_aluno` int(11) NOT NULL,
  `id_atendente` int(11) NOT NULL,
  `status` varchar(20) DEFAULT 'pendente',
  PRIMARY KEY (`id_pedido`),
  KEY `id_aluno` (`id_aluno`),
  KEY `id_atendente` (`id_atendente`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_aluno`) REFERENCES `aluno` (`id_aluno`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`id_atendente`) REFERENCES `atendente` (`id_atendente`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'2026-08-12 20:56:50','dinheiro',1,1,'cancelado'),(2,'2026-08-12 20:58:20','dinheiro',1,1,'ativo');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produto`
--

DROP TABLE IF EXISTS `produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produto` (
  `id_produto` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `preco` decimal(10,2) NOT NULL,
  `codigo_barras` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_produto`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto`
--

LOCK TABLES `produto` WRITE;
/*!40000 ALTER TABLE `produto` DISABLE KEYS */;
INSERT INTO `produto` VALUES (1,'Arroz',5.50,'123123123'),(2,'feijao',10.00,'12312312313');
/*!40000 ALTER TABLE `produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produto_nao_perecivel`
--

DROP TABLE IF EXISTS `produto_nao_perecivel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produto_nao_perecivel` (
  `id_produto` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_produto`),
  CONSTRAINT `produto_nao_perecivel_ibfk_1` FOREIGN KEY (`id_produto`) REFERENCES `produto` (`id_produto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto_nao_perecivel`
--

LOCK TABLES `produto_nao_perecivel` WRITE;
/*!40000 ALTER TABLE `produto_nao_perecivel` DISABLE KEYS */;
/*!40000 ALTER TABLE `produto_nao_perecivel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produto_perecivel`
--

DROP TABLE IF EXISTS `produto_perecivel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produto_perecivel` (
  `id_produto` int(11) NOT NULL AUTO_INCREMENT,
  `data_validade` date NOT NULL,
  PRIMARY KEY (`id_produto`),
  CONSTRAINT `produto_perecivel_ibfk_1` FOREIGN KEY (`id_produto`) REFERENCES `produto` (`id_produto`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto_perecivel`
--

LOCK TABLES `produto_perecivel` WRITE;
/*!40000 ALTER TABLE `produto_perecivel` DISABLE KEYS */;
INSERT INTO `produto_perecivel` VALUES (1,'0000-00-00'),(2,'0000-00-00');
/*!40000 ALTER TABLE `produto_perecivel` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-12 21:09:45
