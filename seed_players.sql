-- ============================================
-- 无畏契约职业选手种子数据
-- 字符集 utf8mb4
-- ============================================

USE news_app;

SET FOREIGN_KEY_CHECKS = 0;

-- 清旧表(如果之前跑过 news 模块)
DROP TABLE IF EXISTS `related_news`;
DROP TABLE IF EXISTS `news`;
DROP TABLE IF EXISTS `news_category`;

-- 战队表
DROP TABLE IF EXISTS `team`;
CREATE TABLE `team` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `region` VARCHAR(20) NOT NULL COMMENT 'CN/NA/EMEA/APAC/KR',
  `logo_url` VARCHAR(255) DEFAULT NULL,
  `sort_order` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME DEFAULT NULL,
  `updated_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 选手表
DROP TABLE IF EXISTS `player`;
CREATE TABLE `player` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ign` VARCHAR(50) NOT NULL COMMENT '游戏内ID',
  `real_name` VARCHAR(50) DEFAULT NULL,
  `team_id` INT NOT NULL,
  `role` VARCHAR(20) NOT NULL COMMENT 'duelist/controller/initiator/sentinel',
  `nationality` VARCHAR(50) DEFAULT NULL,
  `birthday` DATETIME DEFAULT NULL,
  `photo_url` VARCHAR(255) DEFAULT NULL,
  `dpi` INT DEFAULT NULL,
  `sensitivity` FLOAT DEFAULT NULL,
  `crosshair_code` VARCHAR(500) DEFAULT NULL,
  `achievements` TEXT,
  `views` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME DEFAULT NULL,
  `updated_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_player_team_idx` (`team_id`),
  KEY `idx_player_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 战队
-- ============================================
INSERT INTO `team` (`id`, `name`, `region`, `sort_order`) VALUES
(1, 'EDward Gaming', 'CN', 1),
(2, 'Sentinels',     'NA', 2),
(3, 'FNATIC',        'EMEA', 3),
(4, 'LOUD',          'BR', 4),
(5, 'Gen.G',         'KR', 5);

-- ============================================
-- 选手
-- ============================================
INSERT INTO `player`
(`ign`, `real_name`, `team_id`, `role`, `nationality`, `birthday`, `dpi`, `sensitivity`, `crosshair_code`, `achievements`) VALUES

-- EDG 全员(2024 VCT Champions 冠军阵容)
('ZmjjKK',  '郑永康', 1, 'duelist',   '中国', '2004-03-03', 800, 0.395,
 '0;s;1;P;c;8;u;000000FF;h;0;b;1;0l;3;0v;5;0o;1;0a;1;0f;0;1b;0;S;c;4;s;0.6',
 '2024 VCT Champions 冠军;2024 Champions 总决赛MVP;VCT历史击杀数第一'),

('CHICHOO', '陈奕帆', 1, 'sentinel',  '中国', NULL, 800, 0.21,
 '0;s;1;P;c;5;u;1B29C1FF;h;0;f;0;s;0;0l;4;0o;0;0a;1;0f;0;1b;0',
 '2024 VCT Champions 冠军'),

('Smoggy',   NULL,     1, 'controller','中国', NULL, NULL, NULL,
 NULL,
 '2024 VCT Champions 冠军'),

('nobody',   NULL,     1, 'sentinel',  '中国', NULL, NULL, NULL,
 NULL,
 '2024 VCT Champions 冠军'),

('S1mon',    NULL,     1, 'initiator', '中国', NULL, NULL, NULL,
 NULL,
 '2024 VCT Champions 冠军'),

('Haodong',  NULL,     1, 'duelist',   '中国', NULL, NULL, NULL,
 '0;s;1;P;c;5;o;1;f;0;0t;1;0l;4;0o;0;0a;1;0f;0;1b;0',
 '2024 VCT Champions 冠军'),

-- Sentinels
('TenZ',     'Tyson Ngo', 2, 'duelist', '加拿大', '2001-07-23', 800, 0.355,
 '0;s;1;P;c;5;u;2AFF00FF;h;0;f;0;0l;2;0v;2;0o;1;0a;1;0f;0;1b;0',
 '2021 VCT Masters Reykjavík 冠军;2024 Masters Madrid 冠军'),

('Zekken',   'Zachary Patrone', 2, 'duelist', '美国', '2004-08-05', 800, 0.2,
 NULL,
 '2024 Masters Madrid 冠军'),

-- LOUD
('aspas',    'Erick Santos', 4, 'duelist', '巴西', '2002-11-10', 800, 0.18,
 '0;P;c;8;u;00008BFF;h;0;b;1;0l;4;0o;2;0a;1;0f;0;1b;0',
 '2022 VCT Champions 冠军'),

-- FNATIC
('Derke',    'Nikita Sirmitev', 3, 'duelist', '芬兰', '2003-09-10', 800, 0.6,
 NULL,
 '2023 VCT 年度最佳阵容');
