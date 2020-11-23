CREATE DATABASE `blog` /*!40100 DEFAULT CHARACTER SET latin1 */;

CREATE TABLE `blog`.`blog_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `author` varchar(20) NOT NULL DEFAULT 'N/A',
  `date_posted` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
