/*
 Navicat Premium Data Transfer

 Source Server         : tuzi-hotel
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : tuzi-hotel

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 28/02/2021 17:54:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `img` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `price` decimal(10, 2) UNSIGNED ZEROFILL NOT NULL,
  `descp` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES (1, '标准大床房', '/static/img/BZD.jpg', 00000260.00, '标准双人间');
INSERT INTO `category` VALUES (2, '标准双人间', '/static/img/BZS.jpg', 00000300.00, '标准双人间');
INSERT INTO `category` VALUES (3, '高级大床房', '/static/img/HHD.jpg', 00000350.00, '这是高级大床房的描述');
INSERT INTO `category` VALUES (4, '高级双床房', '/static/img/HHS.jpg', 00000420.00, '这是高级双床房的描述');
INSERT INTO `category` VALUES (5, '豪华家庭房', '/static/img/JJT.jpg', 00000550.00, '这是标准间的描述');

-- ----------------------------
-- Table structure for order
-- ----------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `room_id` int(11) NULL DEFAULT NULL,
  `category_id` int(11) NULL DEFAULT NULL,
  `price` int(11) NULL DEFAULT NULL,
  `weak_time` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `need_weak` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `begin_time` bigint(255) NULL DEFAULT NULL,
  `end_time` bigint(255) NULL DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `mobile` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `category_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `room_descp` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` int(255) NULL DEFAULT 0 COMMENT '0是刚提交-1是退订2是离店',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 23 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order
-- ----------------------------
INSERT INTO `order` VALUES (1, 1, 1, 1, 200, '', 'on', 1610769600, 1610856000, 'admin', '15010226955', '标准间', '描述', -1);
INSERT INTO `order` VALUES (2, 1, 1, 1, 200, '', '', 1610769600, 1612858423, 'admin', '15010226955', '标准间', '描述', 2);
INSERT INTO `order` VALUES (3, 1, 1, 1, 200, '', '', 1610769600, 1612859290, 'admin', '15010226955', '标准间', '描述', 2);
INSERT INTO `order` VALUES (4, 1, 1, 1, 200, '', '', 1610769600, 1612859292, 'admin', '15010226955', '标准间', '描述', 2);
INSERT INTO `order` VALUES (5, 1, 1, 1, 200, '', '', 1610769600, 1612859294, 'admin', '15010226955', '标准间', '描述', 2);
INSERT INTO `order` VALUES (6, 1, 1, 1, 200, '', '', 1610769600, 1612859296, 'admin', '15010226955', '标准间', '描述', 2);
INSERT INTO `order` VALUES (7, 1, 1, 1, 200, '', '', 1610769600, 1611404500, 'admin', '15010226955', '标准间', '描述', 2);
INSERT INTO `order` VALUES (8, 2, 1, 1, 260, '2021-01-27 00:00:00', 'on', 1611374400, 1636171200, '187', '15010226955', '标准间123', '描述', 2);
INSERT INTO `order` VALUES (9, 4, 1, 1, 260, '2021-02-15 00:00:00', 'on', 1612065600, 1609473600, '1876993774', '1876993774', '标准间123', '描述', -1);
INSERT INTO `order` VALUES (10, 7, 1, 1, 260, '', '', 1610769600, 1611404500, '18769937742', '18769937742', '标准间123', '描述', 2);
INSERT INTO `order` VALUES (11, 7, 2, 2, 250, '', 'on', 1610769600, 1611404500, '18769937742', '18769937742', '高级大床房', '描述', 2);
INSERT INTO `order` VALUES (12, 7, 2, 2, 250, '', 'on', 1610769600, 1612859298, '18769937742', '18769937742', '高级大床房', '描述', 2);
INSERT INTO `order` VALUES (13, 7, 2, 2, 250, '', 'on', 1610769600, 1612859299, '18769937742', '18769937742', '高级大床房', '描述', 2);
INSERT INTO `order` VALUES (14, 7, 2, 2, 250, '', 'on', 1610769600, 1612859301, '18769937742', '18769937742', '高级大床房', '描述', 2);
INSERT INTO `order` VALUES (15, 7, 2, 2, 250, '', 'on', 1610769600, 1612859303, '18769937742', '18769937742', '高级大床房', '描述', 2);
INSERT INTO `order` VALUES (16, 7, 1, 1, 260, '', '', 1636430400, 1612855714, '18769937742', '18769937742', '标准间123', '描述', -1);
INSERT INTO `order` VALUES (17, 7, 1, 1, 260, '', '', 1636430400, 1612856484, '18769937742', '18769937742', '标准间123', '描述', -1);
INSERT INTO `order` VALUES (18, 7, 1, 1, 260, '', '', 1612929600, 1612856934, '18769937742', '18769937742', '标准间123', '描述', -1);
INSERT INTO `order` VALUES (19, 7, 1, 1, 260, '', '', 1613102400, 1612856950, '18769937742', '18769937742', '标准间123', '描述', -1);
INSERT INTO `order` VALUES (20, 5, 1, 1, 260, '', '', 1612929600, 1613016000, 'superuser', '15010223655', '标准间123', '描述', 0);
INSERT INTO `order` VALUES (22, 1, 2, 2, 250, '', '', 1612929600, 1612862292, 'admin', '15010226955', '高级大床房', '描述', -1);
INSERT INTO `order` VALUES (21, 5, 1, 1, 260, '', '', 1612929600, 1613016000, 'superuser', '15010223655', '标准间123', '描述', 0);

-- ----------------------------
-- Table structure for order_extra
-- ----------------------------
DROP TABLE IF EXISTS `order_extra`;
CREATE TABLE `order_extra`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `price` int(10) NULL DEFAULT NULL,
  `number` int(11) NULL DEFAULT NULL,
  `total` int(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 41 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order_extra
-- ----------------------------
INSERT INTO `order_extra` VALUES (1, 8, '牙刷', 8, 2, 16);
INSERT INTO `order_extra` VALUES (2, 8, '矿泉水', 2, 1, 2);
INSERT INTO `order_extra` VALUES (3, 8, '面包', 10, 2, 20);
INSERT INTO `order_extra` VALUES (4, 8, '日用品', 28, 1, 28);
INSERT INTO `order_extra` VALUES (5, 2, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (6, 2, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (7, 2, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (8, 2, '日用品', 28, 0, 0);
INSERT INTO `order_extra` VALUES (9, 3, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (10, 3, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (11, 3, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (12, 3, '日用品', 28, 0, 0);
INSERT INTO `order_extra` VALUES (13, 4, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (14, 4, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (15, 4, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (16, 4, '日用品', 28, 0, 0);
INSERT INTO `order_extra` VALUES (17, 5, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (18, 5, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (19, 5, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (20, 5, '日用品', 28, 0, 0);
INSERT INTO `order_extra` VALUES (21, 6, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (22, 6, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (23, 6, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (24, 6, '日用品', 28, 0, 0);
INSERT INTO `order_extra` VALUES (25, 12, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (26, 12, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (27, 12, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (28, 12, '日用品', 28, 0, 0);
INSERT INTO `order_extra` VALUES (29, 13, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (30, 13, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (31, 13, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (32, 13, '日用品', 28, 0, 0);
INSERT INTO `order_extra` VALUES (33, 14, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (34, 14, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (35, 14, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (36, 14, '日用品', 28, 0, 0);
INSERT INTO `order_extra` VALUES (37, 15, '牙刷', 8, 0, 0);
INSERT INTO `order_extra` VALUES (38, 15, '矿泉水', 2, 0, 0);
INSERT INTO `order_extra` VALUES (39, 15, '面包', 10, 0, 0);
INSERT INTO `order_extra` VALUES (40, 15, '日用品', 28, 0, 0);

-- ----------------------------
-- Table structure for order_money
-- ----------------------------
DROP TABLE IF EXISTS `order_money`;
CREATE TABLE `order_money`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NULL DEFAULT NULL,
  `money` int(255) NULL DEFAULT NULL,
  `source` int(255) NULL DEFAULT 1 COMMENT '1是定金2是房费3是附加',
  `status` int(255) NULL DEFAULT 0 COMMENT '0是未支付，1是已支付，-1是退款',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Fixed;

-- ----------------------------
-- Records of order_money
-- ----------------------------
INSERT INTO `order_money` VALUES (1, 2, 40, 1, 1);
INSERT INTO `order_money` VALUES (2, 3, 40, 1, 1);
INSERT INTO `order_money` VALUES (3, 4, 40, 1, -1);
INSERT INTO `order_money` VALUES (4, 5, 40, 1, 1);
INSERT INTO `order_money` VALUES (5, 6, 40, 1, 1);
INSERT INTO `order_money` VALUES (6, 7, 40, 1, 1);
INSERT INTO `order_money` VALUES (7, 8, 52, 1, 1);
INSERT INTO `order_money` VALUES (8, 9, 52, 1, -1);
INSERT INTO `order_money` VALUES (9, 10, 52, 1, 1);
INSERT INTO `order_money` VALUES (10, 11, 50, 1, 1);
INSERT INTO `order_money` VALUES (11, 12, 50, 1, 1);
INSERT INTO `order_money` VALUES (12, 13, 50, 1, 1);
INSERT INTO `order_money` VALUES (13, 14, 50, 1, 1);
INSERT INTO `order_money` VALUES (14, 15, 50, 1, 1);
INSERT INTO `order_money` VALUES (15, 16, 52, 1, -1);
INSERT INTO `order_money` VALUES (16, 17, 52, 1, -1);
INSERT INTO `order_money` VALUES (17, 18, 52, 1, 1);
INSERT INTO `order_money` VALUES (18, 19, 52, 1, -1);
INSERT INTO `order_money` VALUES (19, 20, 52, 1, 1);
INSERT INTO `order_money` VALUES (20, 21, 52, 1, 1);
INSERT INTO `order_money` VALUES (21, 22, 50, 1, 1);

-- ----------------------------
-- Table structure for room
-- ----------------------------
DROP TABLE IF EXISTS `room`;
CREATE TABLE `room`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orientation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '朝向',
  `have_windows` tinyint(1) NOT NULL,
  `have_book` tinyint(1) UNSIGNED ZEROFILL NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `category_id` int(10) UNSIGNED NOT NULL,
  `descp` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '描述',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of room
-- ----------------------------

INSERT INTO `room` VALUES (0011, '东', 1, 1, '0011', 1, '描述');
INSERT INTO `room` VALUES (0012, '南', 1, 0, '0012', 1, '描述');
INSERT INTO `room` VALUES (0013, '西', 0, 1, '0013', 1, '描述');
INSERT INTO `room` VALUES (0014, '北', 1, 1, '0014', 1, '描述');
INSERT INTO `room` VALUES (0015, '南', 0, 0, '0015', 1, '描述');
INSERT INTO `room` VALUES (0021, '东', 1, 1, '0021', 2, '描述');
INSERT INTO `room` VALUES (0022, '东', 0, 1, '0022', 2, '描述');
INSERT INTO `room` VALUES (0023, '东', 1, 0, '0023', 2, '描述');
INSERT INTO `room` VALUES (0024, '东', 0, 0, '0024', 2, '描述');
INSERT INTO `room` VALUES (0025, '东', 1, 1, '0025', 2, '描述');
INSERT INTO `room` VALUES (0026, '东', 0, 1, '0026', 2, '描述');
INSERT INTO `room` VALUES (0031, '北', 1, 1, '0031', 3, '描述');
INSERT INTO `room` VALUES (0032, '北', 0, 1, '0032', 3, '描述');
INSERT INTO `room` VALUES (0033, '北', 1, 0, '0033', 3, '描述');
INSERT INTO `room` VALUES (0034, '北', 1, 0, '0034', 3, '描述');
INSERT INTO `room` VALUES (0035, '北', 0, 1, '0035', 3, '描述');
INSERT INTO `room` VALUES (0036, '北', 0, 0, '0036', 3, '描述');
INSERT INTO `room` VALUES (0037, '北', 1, 1, '0037', 3, '描述');
INSERT INTO `room` VALUES (0038, '北', 1, 1, '0038', 3, '描述');
INSERT INTO `room` VALUES (0041, '北', 1, 1, '0041', 4, '描述');
INSERT INTO `room` VALUES (0042, '北', 1, 1, '0042', 4, '描述');
INSERT INTO `room` VALUES (0051, '北', 1, 1, '0051', 5, '描述');
-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_admin` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '0' COMMENT '0是普通1是admin2是boss',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_info
-- ----------------------------
INSERT INTO `user_info` VALUES (1, 'admin', 'admin132@qq.com', '21232f297a57a5a743894a0e4a801fc3', '15010226955', '2');
INSERT INTO `user_info` VALUES (4, '1876993774', '1876993774@qq.com', '2f5b4e610c927c81a09eebf67780871e', '1876993774', '0');
INSERT INTO `user_info` VALUES (5, 'superuser', 'superuser@qq.com', '0baea2f0ae20150db78f58cddac442a9', '15010223655', '1');
INSERT INTO `user_info` VALUES (6, '187699', '187699@qq.com', '9e5f954fc04383fe3593aeafb461941e', '187699', '0');
INSERT INTO `user_info` VALUES (7, '18769937742', '1876993774233@qq.com', 'b1b786573d0bf033979b77c0f7fda435', '18769937742', '0');

SET FOREIGN_KEY_CHECKS = 1;
