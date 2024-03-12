# 全量数据下载。初始是从Kaggle下载， https://www.kaggle.com/datasets/Cornell-University/arxiv?resource=download

# 基于Ubuntu
# 安装MySQL
sudo apt update
sudo apt install mysql-server
sudo apt install mysql-client
sudo apt install libmysqlclient-dev

## 首次登录
sudo mysql -u root -p
## mysql的用户，如果是root，必须要sudo才可以，所以需要创建普通用户
create database paper_default default charset=utf8;
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON database_name.* TO 'newuser'@'localhost';

## 建表
CREATE TABLE paper_base(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    is_del int NOT NULL comment "default is 0, 1 means deleted",
    p_id_uni VARCHAR(20) unique comment 'arxiv paper id',
    p_submitter VARCHAR(40) comment '',
    p_authors TEXT comment "author list",
    p_title TEXT comment "",
    p_comments TEXT comment "pages and pictures",
    p_journal_ref TEXT comment "所刊信息",
    p_doi TEXT COMMENT "数字对象标识符",
    p_report_no TEXT COMMENT "报告编号",
    p_categories TEXT COMMENT "Arxiv类别",
    p_license TEXT COMMENT "许可",
    p_abstract TEXT COMMENT "摘要",
    p_versions TEXT COMMENT "论文版本",
    p_update_date TEXT COMMENT "论文创建时间",
    create_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '论文基础';

# 安装ElasticSearch
sudo apt update
sudo apt install apt-transport-https ca-certificates wget

## 导入软件源的 GPG key：
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
## 添加 Elasticsearch 软件源 到系统
sudo sh -c 'echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" > /etc/apt/sources.list.d/elastic-8.x.list'

sudo apt update
sudo apt install elasticsearch

## 开机启动
sudo systemctl enable --now elasticsearch.service
curl -X GET "localhost:9200/"

## 查看服务消息
sudo journalctl -u elasticsearch

sudo nano /etc/elasticsearch/elasticsearch.yml
network.host: 0.0.0.0
# xpack.security.enabled:false
# xpack.security.enabled: true
# xpack.license.self_generated.type: basic
# xpack.security.transport.ssl.enabled: true
# /usr/share/elasticsearch/bin# ./elasticsearch-reset-password --interactive -u elastic
# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic https://localhost:9200

sudo systemctl restart elasticsearch

## 安装ik分词插件


## 建表


## 数据导入


# 安装Neo4j
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j
sudo service neo4j start
vim /etc/neo4j/neo4j.conf
## 把 #dbms.connectors.default_listen_address=0.0.0.0 取消注释即可
neo4j://localhost:7687 或7474
# 如果忘记密码，
# conf文件中，注释这一行，dbms.security.auth_enabled=false
# 重启服务，浏览器中，ALTER USER neo4j SET PASSWORD 'newpwd'; 然后重新注释，重启服务。


# 安装faiss
pip install faiss-gpu

## 数据导入


# 数据分析