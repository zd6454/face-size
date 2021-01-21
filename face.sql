/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80022
 Source Host           : localhost:3306
 Source Schema         : face

 Target Server Type    : MySQL
 Target Server Version : 80022
 File Encoding         : 65001

 Date: 05/01/2021 16:22:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for qds
-- ----------------------------
DROP TABLE IF EXISTS `qds`;
CREATE TABLE `qds`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `ctime` datetime NULL DEFAULT NULL,
  `st` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 42 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of qds
-- ----------------------------
INSERT INTO `qds` VALUES (40, '3', '3', '2021-01-05 15:00:11', '异常');
INSERT INTO `qds` VALUES (41, '3', '3', '2021-01-05 15:00:49', '异常');
INSERT INTO `qds` VALUES (46, '123456', '123456', '2021-01-05 16:17:19', '异常');

-- ----------------------------
-- Table structure for qds_month
-- ----------------------------
DROP TABLE IF EXISTS `qds_month`;
CREATE TABLE `qds_month`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `no` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ctime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '/',
  `st_no` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qds_month
-- ----------------------------
INSERT INTO `qds_month` VALUES (1, '555', '55', '/', 0);
INSERT INTO `qds_month` VALUES (2, '5552', 'admin', '/', 0);
INSERT INTO `qds_month` VALUES (3, '3', '3', '/', 4);
INSERT INTO `qds_month` VALUES (9, '123456', '123456', '/', 1);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `face_token` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `wy`(`no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 84 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (75, '1', '1', 'b77f017b2d646498195ff69eaa57d546');
INSERT INTO `user` VALUES (76, '2', '2', 'ee899b1519049ca0222ea07514417d32');
INSERT INTO `user` VALUES (77, '12', '12', 'dc68c08f4f03b21fc6fec932ea6a3218');
INSERT INTO `user` VALUES (78, '2222', '2222', '5841245176ae17cb5dc6fb6cca512241');
INSERT INTO `user` VALUES (79, '1222', '122', '0ea213b6c1236d7bc0d579cf96033fe1');
INSERT INTO `user` VALUES (80, '555', '55', '82dfc4f28e0105f84dc09e64a64eebbc');
INSERT INTO `user` VALUES (81, '5552', 'admin', 'e0bd78b595ab5522bf5f999735f2bfb0');
INSERT INTO `user` VALUES (83, '3', '3', '38a784a59bd0af0166f4502a03568293');
INSERT INTO `user` VALUES (93, '123456', '123456', '4dc760e8ad00ae1a5cb8e1b35014b201');

-- ----------------------------
-- Triggers structure for table qds
-- ----------------------------
DROP TRIGGER IF EXISTS `qds_AFTER_INSERT`;
delimiter ;;
CREATE TRIGGER `qds_AFTER_INSERT` AFTER INSERT ON `qds` FOR EACH ROW BEGIN
if (new.st = "异常") then
update qds_month set st_no = st_no+1 where qds_month.no = new.no;
end if;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table user
-- ----------------------------
DROP TRIGGER IF EXISTS `user_AFTER_DELETE`;
delimiter ;;
CREATE TRIGGER `user_AFTER_DELETE` AFTER DELETE ON `user` FOR EACH ROW BEGIN
delete from qds_month where qds_month.no = old.no;
delete from qds where qds.no = old.no;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
