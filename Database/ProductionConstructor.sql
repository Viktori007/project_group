/*
 Navicat Premium Dump SQL

 Source Server         : Production.Constructor
 Source Server Type    : MySQL
 Source Server Version : 90100 (9.1.0)
 Source Host           : localhost:3306
 Source Schema         : ProductionConstructor

 Target Server Type    : MySQL
 Target Server Version : 90100 (9.1.0)
 File Encoding         : 65001

 Date: 22/02/2025 20:48:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for CalculationUnitProduct
-- ----------------------------
DROP TABLE IF EXISTS `CalculationUnitProduct`;
CREATE TABLE `CalculationUnitProduct`  (
  `CalculationUnitsId` int NOT NULL,
  `ProductId` int NOT NULL,
  PRIMARY KEY (`CalculationUnitsId`, `ProductId`) USING BTREE,
  INDEX `IX_CalculationUnitProduct_ProductId`(`ProductId` ASC) USING BTREE,
  CONSTRAINT `FK_CalculationUnitProduct_CalculationUnits_CalculationUnitsId` FOREIGN KEY (`CalculationUnitsId`) REFERENCES `CalculationUnits` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_CalculationUnitProduct_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of CalculationUnitProduct
-- ----------------------------

-- ----------------------------
-- Table structure for CalculationUnits
-- ----------------------------
DROP TABLE IF EXISTS `CalculationUnits`;
CREATE TABLE `CalculationUnits`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of CalculationUnits
-- ----------------------------
INSERT INTO `CalculationUnits` VALUES (1, 'м2');
INSERT INTO `CalculationUnits` VALUES (2, 'шт');

-- ----------------------------
-- Table structure for HistoryActions
-- ----------------------------
DROP TABLE IF EXISTS `HistoryActions`;
CREATE TABLE `HistoryActions`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of HistoryActions
-- ----------------------------
INSERT INTO `HistoryActions` VALUES (1, 'взято');
INSERT INTO `HistoryActions` VALUES (2, 'положено на склад');
INSERT INTO `HistoryActions` VALUES (3, 'использовано в продукте');

-- ----------------------------
-- Table structure for Images
-- ----------------------------
DROP TABLE IF EXISTS `Images`;
CREATE TABLE `Images`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Data` varbinary(4096) NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Images
-- ----------------------------

-- ----------------------------
-- Table structure for ItemStates
-- ----------------------------
DROP TABLE IF EXISTS `ItemStates`;
CREATE TABLE `ItemStates`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ItemStates
-- ----------------------------
INSERT INTO `ItemStates` VALUES (1, 'Брак');
INSERT INTO `ItemStates` VALUES (2, 'Нормально');

-- ----------------------------
-- Table structure for MaterialProduct
-- ----------------------------
DROP TABLE IF EXISTS `MaterialProduct`;
CREATE TABLE `MaterialProduct`  (
  `MaterialsId` int NOT NULL,
  `ProductId` int NOT NULL,
  PRIMARY KEY (`MaterialsId`, `ProductId`) USING BTREE,
  INDEX `IX_MaterialProduct_ProductId`(`ProductId` ASC) USING BTREE,
  CONSTRAINT `FK_MaterialProduct_Materials_MaterialsId` FOREIGN KEY (`MaterialsId`) REFERENCES `Materials` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_MaterialProduct_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of MaterialProduct
-- ----------------------------

-- ----------------------------
-- Table structure for MaterialProduction
-- ----------------------------
DROP TABLE IF EXISTS `MaterialProduction`;
CREATE TABLE `MaterialProduction`  (
  `MaterialsId` int NOT NULL,
  `ProductionId` int NOT NULL,
  PRIMARY KEY (`MaterialsId`, `ProductionId`) USING BTREE,
  INDEX `IX_MaterialProduction_ProductionId`(`ProductionId` ASC) USING BTREE,
  CONSTRAINT `FK_MaterialProduction_Materials_MaterialsId` FOREIGN KEY (`MaterialsId`) REFERENCES `Materials` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_MaterialProduction_Productions_ProductionId` FOREIGN KEY (`ProductionId`) REFERENCES `Productions` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of MaterialProduction
-- ----------------------------

-- ----------------------------
-- Table structure for MaterialTypes
-- ----------------------------
DROP TABLE IF EXISTS `MaterialTypes`;
CREATE TABLE `MaterialTypes`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of MaterialTypes
-- ----------------------------
INSERT INTO `MaterialTypes` VALUES (1, 'хлопок');
INSERT INTO `MaterialTypes` VALUES (2, 'синтетика');

-- ----------------------------
-- Table structure for Materials
-- ----------------------------
DROP TABLE IF EXISTS `Materials`;
CREATE TABLE `Materials`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UnitId` int NOT NULL,
  `MaterialTypeId` int NOT NULL,
  `StateId` int NOT NULL,
  `ImageId` int NULL DEFAULT NULL,
  `Width` double NOT NULL,
  `Height` double NOT NULL,
  `Color` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_Materials_ImageId`(`ImageId` ASC) USING BTREE,
  INDEX `IX_Materials_MaterialTypeId`(`MaterialTypeId` ASC) USING BTREE,
  INDEX `IX_Materials_StateId`(`StateId` ASC) USING BTREE,
  INDEX `IX_Materials_UnitId`(`UnitId` ASC) USING BTREE,
  CONSTRAINT `FK_Materials_CalculationUnits_UnitId` FOREIGN KEY (`UnitId`) REFERENCES `CalculationUnits` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_Materials_Images_ImageId` FOREIGN KEY (`ImageId`) REFERENCES `Images` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_Materials_ItemStates_StateId` FOREIGN KEY (`StateId`) REFERENCES `ItemStates` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_Materials_MaterialTypes_MaterialTypeId` FOREIGN KEY (`MaterialTypeId`) REFERENCES `MaterialTypes` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Materials
-- ----------------------------
INSERT INTO `Materials` VALUES (1, 'ткань', 1, 1, 2, NULL, 100, 100, '#ffffff');
INSERT INTO `Materials` VALUES (2, 'ткань', 2, 2, 2, NULL, 100, 100, '#ffffff');

-- ----------------------------
-- Table structure for OrderHistory
-- ----------------------------
DROP TABLE IF EXISTS `OrderHistory`;
CREATE TABLE `OrderHistory`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `OrderId` int NOT NULL,
  `OrderStatusId` int NOT NULL,
  `Date` datetime(6) NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_OrderHistory_OrderId`(`OrderId` ASC) USING BTREE,
  INDEX `IX_OrderHistory_OrderStatusId`(`OrderStatusId` ASC) USING BTREE,
  CONSTRAINT `FK_OrderHistory_Orders_OrderId` FOREIGN KEY (`OrderId`) REFERENCES `Orders` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_OrderHistory_OrderStatuses_OrderStatusId` FOREIGN KEY (`OrderStatusId`) REFERENCES `OrderStatuses` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of OrderHistory
-- ----------------------------

-- ----------------------------
-- Table structure for OrderItems
-- ----------------------------
DROP TABLE IF EXISTS `OrderItems`;
CREATE TABLE `OrderItems`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `ProductId` int NOT NULL,
  `Amount` int NOT NULL,
  `Price` double NOT NULL,
  `OrderId` int NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_OrderItems_OrderId`(`OrderId` ASC) USING BTREE,
  INDEX `IX_OrderItems_ProductId`(`ProductId` ASC) USING BTREE,
  CONSTRAINT `FK_OrderItems_Orders_OrderId` FOREIGN KEY (`OrderId`) REFERENCES `Orders` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_OrderItems_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of OrderItems
-- ----------------------------
INSERT INTO `OrderItems` VALUES (1, 2, 10, 100, 1);

-- ----------------------------
-- Table structure for OrderStatuses
-- ----------------------------
DROP TABLE IF EXISTS `OrderStatuses`;
CREATE TABLE `OrderStatuses`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of OrderStatuses
-- ----------------------------
INSERT INTO `OrderStatuses` VALUES (1, 'в обработке');
INSERT INTO `OrderStatuses` VALUES (2, 'готов');

-- ----------------------------
-- Table structure for Orders
-- ----------------------------
DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `ClientId` int NOT NULL,
  `Date` datetime(6) NOT NULL,
  `TotalPrice` double NOT NULL,
  `StatusId` int NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_Orders_ClientId`(`ClientId` ASC) USING BTREE,
  INDEX `IX_Orders_StatusId`(`StatusId` ASC) USING BTREE,
  CONSTRAINT `FK_Orders_OrderStatuses_StatusId` FOREIGN KEY (`StatusId`) REFERENCES `OrderStatuses` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_Orders_Users_ClientId` FOREIGN KEY (`ClientId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Orders
-- ----------------------------
INSERT INTO `Orders` VALUES (1, 1, '2025-02-11 21:55:40.000000', 10000, 1);

-- ----------------------------
-- Table structure for Productions
-- ----------------------------
DROP TABLE IF EXISTS `Productions`;
CREATE TABLE `Productions`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `WorkshopId` int NOT NULL,
  `Date` datetime(6) NOT NULL,
  `UserId` int NOT NULL,
  `ProductId` int NOT NULL,
  `Quantity` int NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_Productions_ProductId`(`ProductId` ASC) USING BTREE,
  INDEX `IX_Productions_UserId`(`UserId` ASC) USING BTREE,
  INDEX `IX_Productions_WorkshopId`(`WorkshopId` ASC) USING BTREE,
  CONSTRAINT `FK_Productions_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_Productions_Users_UserId` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_Productions_Workshops_WorkshopId` FOREIGN KEY (`WorkshopId`) REFERENCES `Workshops` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Productions
-- ----------------------------

-- ----------------------------
-- Table structure for Products
-- ----------------------------
DROP TABLE IF EXISTS `Products`;
CREATE TABLE `Products`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MainUnitId` int NOT NULL,
  `Grid` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `StateId` int NOT NULL,
  `ImageId` int NULL DEFAULT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_Products_ImageId`(`ImageId` ASC) USING BTREE,
  INDEX `IX_Products_MainUnitId`(`MainUnitId` ASC) USING BTREE,
  INDEX `IX_Products_StateId`(`StateId` ASC) USING BTREE,
  CONSTRAINT `FK_Products_CalculationUnits_MainUnitId` FOREIGN KEY (`MainUnitId`) REFERENCES `CalculationUnits` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_Products_Images_ImageId` FOREIGN KEY (`ImageId`) REFERENCES `Images` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_Products_ItemStates_StateId` FOREIGN KEY (`StateId`) REFERENCES `ItemStates` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Products
-- ----------------------------
INSERT INTO `Products` VALUES (1, 'носовой платок', 2, '', 2, NULL);
INSERT INTO `Products` VALUES (2, 'сумка', 2, '', 2, NULL);

-- ----------------------------
-- Table structure for Remains
-- ----------------------------
DROP TABLE IF EXISTS `Remains`;
CREATE TABLE `Remains`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `MaterialTypeId` int NOT NULL,
  `Amount` int NOT NULL,
  `UnitId` int NOT NULL,
  `Width` double NOT NULL,
  `Height` double NOT NULL,
  `Color` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_Remains_MaterialTypeId`(`MaterialTypeId` ASC) USING BTREE,
  INDEX `IX_Remains_UnitId`(`UnitId` ASC) USING BTREE,
  CONSTRAINT `FK_Remains_CalculationUnits_UnitId` FOREIGN KEY (`UnitId`) REFERENCES `CalculationUnits` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_Remains_MaterialTypes_MaterialTypeId` FOREIGN KEY (`MaterialTypeId`) REFERENCES `MaterialTypes` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Remains
-- ----------------------------
INSERT INTO `Remains` VALUES (1, 2, 5, 2, 10, 10, '#ffffff');
INSERT INTO `Remains` VALUES (2, 2, 1, 2, 4, 4, '#000000');

-- ----------------------------
-- Table structure for StorageCells
-- ----------------------------
DROP TABLE IF EXISTS `StorageCells`;
CREATE TABLE `StorageCells`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Palet` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `Count` int UNSIGNED NOT NULL,
  `ProductId` int NULL DEFAULT NULL,
  `MaterialId` int NULL DEFAULT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_StorageCells_MaterialId`(`MaterialId` ASC) USING BTREE,
  INDEX `IX_StorageCells_ProductId`(`ProductId` ASC) USING BTREE,
  CONSTRAINT `FK_StorageCells_Materials_MaterialId` FOREIGN KEY (`MaterialId`) REFERENCES `Materials` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_StorageCells_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of StorageCells
-- ----------------------------
INSERT INTO `StorageCells` VALUES (1, '1', 10, 1, NULL);
INSERT INTO `StorageCells` VALUES (2, '2', 4, NULL, 2);

-- ----------------------------
-- Table structure for StorageHistory
-- ----------------------------
DROP TABLE IF EXISTS `StorageHistory`;
CREATE TABLE `StorageHistory`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `ActorId` int NOT NULL,
  `Time` datetime(6) NOT NULL,
  `MaterialId` int NULL DEFAULT NULL,
  `ProductId` int NULL DEFAULT NULL,
  `CellId` int NULL DEFAULT NULL,
  `Amount` int NOT NULL,
  `ActionId` int NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_StorageHistory_ActionId`(`ActionId` ASC) USING BTREE,
  INDEX `IX_StorageHistory_ActorId`(`ActorId` ASC) USING BTREE,
  INDEX `IX_StorageHistory_CellId`(`CellId` ASC) USING BTREE,
  INDEX `IX_StorageHistory_MaterialId`(`MaterialId` ASC) USING BTREE,
  INDEX `IX_StorageHistory_ProductId`(`ProductId` ASC) USING BTREE,
  CONSTRAINT `FK_StorageHistory_HistoryActions_ActionId` FOREIGN KEY (`ActionId`) REFERENCES `HistoryActions` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_StorageHistory_Materials_MaterialId` FOREIGN KEY (`MaterialId`) REFERENCES `Materials` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_StorageHistory_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_StorageHistory_StorageCells_CellId` FOREIGN KEY (`CellId`) REFERENCES `StorageCells` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_StorageHistory_Users_ActorId` FOREIGN KEY (`ActorId`) REFERENCES `Users` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of StorageHistory
-- ----------------------------

-- ----------------------------
-- Table structure for Suppliers
-- ----------------------------
DROP TABLE IF EXISTS `Suppliers`;
CREATE TABLE `Suppliers`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DirectorName` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `INN` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `KPP` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Email` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `Address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Suppliers
-- ----------------------------
INSERT INTO `Suppliers` VALUES (1, 'OOO \"CringeSupplier\"', 'Вася', '987654321', '123456789', 'email@email.com', NULL);

-- ----------------------------
-- Table structure for Supplies
-- ----------------------------
DROP TABLE IF EXISTS `Supplies`;
CREATE TABLE `Supplies`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `SupplierId` int NOT NULL,
  `Date` datetime(6) NOT NULL,
  `TotalPrice` double NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_Supplies_SupplierId`(`SupplierId` ASC) USING BTREE,
  CONSTRAINT `FK_Supplies_Suppliers_SupplierId` FOREIGN KEY (`SupplierId`) REFERENCES `Suppliers` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Supplies
-- ----------------------------
INSERT INTO `Supplies` VALUES (1, 1, '2025-02-12 21:00:00.000000', 100000);

-- ----------------------------
-- Table structure for SupplyItems
-- ----------------------------
DROP TABLE IF EXISTS `SupplyItems`;
CREATE TABLE `SupplyItems`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `MaterialId` int NOT NULL,
  `Amount` int NOT NULL,
  `Price` double NOT NULL,
  `SupplyId` int NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_SupplyItems_MaterialId`(`MaterialId` ASC) USING BTREE,
  INDEX `IX_SupplyItems_SupplyId`(`SupplyId` ASC) USING BTREE,
  CONSTRAINT `FK_SupplyItems_Materials_MaterialId` FOREIGN KEY (`MaterialId`) REFERENCES `Materials` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_SupplyItems_Supplies_SupplyId` FOREIGN KEY (`SupplyId`) REFERENCES `Supplies` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of SupplyItems
-- ----------------------------
INSERT INTO `SupplyItems` VALUES (1, 2, 100, 1000, 1);

-- ----------------------------
-- Table structure for UnitConversions
-- ----------------------------
DROP TABLE IF EXISTS `UnitConversions`;
CREATE TABLE `UnitConversions`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `ProductId` int NOT NULL,
  `FromId` int NOT NULL,
  `ToId` int NOT NULL,
  `ConversionFactor` double NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_UnitConversions_FromId`(`FromId` ASC) USING BTREE,
  INDEX `IX_UnitConversions_ProductId`(`ProductId` ASC) USING BTREE,
  INDEX `IX_UnitConversions_ToId`(`ToId` ASC) USING BTREE,
  CONSTRAINT `FK_UnitConversions_CalculationUnits_FromId` FOREIGN KEY (`FromId`) REFERENCES `CalculationUnits` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_UnitConversions_CalculationUnits_ToId` FOREIGN KEY (`ToId`) REFERENCES `CalculationUnits` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_UnitConversions_Products_ProductId` FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of UnitConversions
-- ----------------------------
INSERT INTO `UnitConversions` VALUES (1, 1, 1, 2, 10);

-- ----------------------------
-- Table structure for UserRoles
-- ----------------------------
DROP TABLE IF EXISTS `UserRoles`;
CREATE TABLE `UserRoles`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of UserRoles
-- ----------------------------
INSERT INTO `UserRoles` VALUES (1, 'клиент');
INSERT INTO `UserRoles` VALUES (2, 'кладовщик');
INSERT INTO `UserRoles` VALUES (3, 'менеджер');
INSERT INTO `UserRoles` VALUES (4, 'директор');

-- ----------------------------
-- Table structure for Users
-- ----------------------------
DROP TABLE IF EXISTS `Users`;
CREATE TABLE `Users`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `RoleId` int NOT NULL,
  `Username` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Login` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Password` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_Users_RoleId`(`RoleId` ASC) USING BTREE,
  CONSTRAINT `FK_Users_UserRoles_RoleId` FOREIGN KEY (`RoleId`) REFERENCES `UserRoles` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Users
-- ----------------------------
INSERT INTO `Users` VALUES (1, 3, 'манагер', 'root', 'root');
INSERT INTO `Users` VALUES (2, 2, 'кладовщик', 'l', 'p');
INSERT INTO `Users` VALUES (3, 4, 'директор', 'l1', 'p1');
INSERT INTO `Users` VALUES (4, 1, 'клиент', 'l2', 'p2');

-- ----------------------------
-- Table structure for WorkshopTypes
-- ----------------------------
DROP TABLE IF EXISTS `WorkshopTypes`;
CREATE TABLE `WorkshopTypes`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of WorkshopTypes
-- ----------------------------
INSERT INTO `WorkshopTypes` VALUES (1, 'тряпки');
INSERT INTO `WorkshopTypes` VALUES (2, 'фурнитура');

-- ----------------------------
-- Table structure for Workshops
-- ----------------------------
DROP TABLE IF EXISTS `Workshops`;
CREATE TABLE `Workshops`  (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `WorkshopTypeId` int NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `IX_Workshops_WorkshopTypeId`(`WorkshopTypeId` ASC) USING BTREE,
  CONSTRAINT `FK_Workshops_WorkshopTypes_WorkshopTypeId` FOREIGN KEY (`WorkshopTypeId`) REFERENCES `WorkshopTypes` (`Id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Workshops
-- ----------------------------
INSERT INTO `Workshops` VALUES (1, '1', 1);
INSERT INTO `Workshops` VALUES (2, '1', 2);

-- ----------------------------
-- Table structure for __EFMigrationsHistory
-- ----------------------------
DROP TABLE IF EXISTS `__EFMigrationsHistory`;
CREATE TABLE `__EFMigrationsHistory`  (
  `MigrationId` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ProductVersion` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`MigrationId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of __EFMigrationsHistory
-- ----------------------------
INSERT INTO `__EFMigrationsHistory` VALUES ('20250222174211_Init', '9.0.1');
INSERT INTO `__EFMigrationsHistory` VALUES ('20250222174647_Trigger', '9.0.1');

-- ----------------------------
-- Triggers structure for table Orders
-- ----------------------------
DROP TRIGGER IF EXISTS `after_order_update`;
delimiter ;;
CREATE TRIGGER `after_order_update` AFTER UPDATE ON `Orders` FOR EACH ROW BEGIN
    -- Проверяем, изменился ли статус заказа
    IF NEW.StatusId <> OLD.StatusId THEN
        -- Вставляем новую запись в таблицу OrderHistory
        INSERT INTO OrderHistory (OrderId, OrderStatusId, Date)
        VALUES (NEW.Id, NEW.StatusId, NOW());
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;