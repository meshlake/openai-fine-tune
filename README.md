# OpenAI Fine-tune Experiment

## 背景

借助大模型的强大能力，我们希望可以彻底改变传统的数据分析开发方式。我们的目标是实现以下功能：首先，将数据库业务源表的详细信息（包括表结构、表关联关系、约束等数据库定义）提供给大模型。接下来，我们可以通过自然语言向大模型提出数据分析需求，并期望大模型能够生成相应的SQL语句来实现这些需求。

我们初步的尝试，是直接将自然语言描述的分析需求和使用的业务源表信息全部传递给 OpenAI，通过一定的提示词，可以实现简单业务场景的分析需求。但是受限于 OpenAI 上线文 token 数量的限制，无法满足复杂场景，尤其是分析需求需要使用多张业务源表的情况，很容易超出 OpenAI 上线文数量的限制。因此，我们想尝试利用 OpenAI Fine-tune 来解决上下文 Token 数量被限制的问题。

基于目前对 Fine-tune 的理解，认为使用私有数据（业务数据库源表信息）Fine-tune 私有模型，可以提高模型对私有数据的上下文理解能力。初步思路是：将数据库业务源表信息作为训练数据，进行 Fine-tune，然后使用 Fine-tune 后的模型，就不需要将业务源表信息再传递到上下文中，可以直接提出业务数据分析需求，模型可以理解需求并给出相应的 SQL 语句。

## 实验

目前，微调功能仅适用于以下基础模型：`davinci`、`curie`、`babbage` 和 `ada`。这些是原始模型，没有任何训练后的指令（例如`text-davinci-003`）。这些基础模型中质量最好的为 `davinci`，因此一下实验训练基础模型均为`davinci`。

训练数据集为某业务库中的 11 张业务表的表结构信息。

### 实验一

#### 训练数据

- 训练数据： `data/training_data_1.jsonl`
- 数据示例：
  ```json
    {"prompt":"sc_org（组织结构表）的建表语句是？ ->","completion":" create table sc_org (innerid varchar(50) not null comment '主键id', parent_id varchar(50) comment '父id', level int comment '层次树结构的层次冗余方便sa报表', no varchar(50) comment '编号', name varchar(50) comment '名字', primary key (innerid)) comment '组织结构表';\n"}
  ```

#### 模型信息

- 文件ID：`file-pSC4mIivoxGuOsGLf1lBlomZ`
- 模型ID：`davinci:ft-meshlake-inc-2023-06-13-12-08-36`

#### 模型测试

1. 使用训练数据集中存在的 prompt，正确回答；
```python
response = openai.Completion.create(
  model="davinci:ft-meshlake-inc-2023-06-13-12-08-36",
  prompt="sc_org（组织结构表）的建表语句是？",
  temperature=0,
  max_tokens=500,
)

# CREATE TABLE sc_org (innerid VARCHAR(50) NOT NULL COMMENT '主键ID', parent_id VARCHAR(50) COMMENT '父ID', level INT COMMENT '层次树结构的层次冗余方便SA报表', no VARCHAR(50) COMMENT '编号', name VARCHAR(50) COMMENT '名字', abbr VARCHAR(50) COMMENT '缩写', orderindex INT COMMENT '排序索引', class_code INT COMMENT '类别对应代码表sc_orgtype，1租户2大区3场所4楼层5区域', class_code_key VARCHAR(50) COMMENT '类别代码表对应资源key', address VARCHAR(200) COMMENT '地址', floor INT COMMENT '楼层：-1.地下一层 1.一楼 2. 二楼', coordinates VARCHAR(50) COMMENT '经纬度(经度纬度)', telephone VARCHAR(50) COMMENT '电话', staffid VARCHAR(50) COMMENT '联系人关联职员表', photo_path VARCHAR(200) COMMENT '图片路径', flag VARCHAR(50) COMMENT '字符串，逗号分隔，1-是否记录数据，2-是否生成报表', `desc` VARCHAR(200) COMMENT '备注', qrcode_title_image VARCHAR(50) COMMENT '桌......
```

2. 使用训练数据集中存在的 prompt，未正确回答（存在编造的字段）；
```python
response = openai.Completion.create(
  model="davinci:ft-meshlake-inc-2023-06-13-12-08-36",
  prompt="hf_order_master（订单主表）的建表语句是？",
  temperature=0,
  max_tokens=500,
)

# CREATE TABLE hf_order_master (innerid INT NOT NULL AUTO_INCREMENT COMMENT '编号', order_no VARCHAR(50) NOT NULL COMMENT '订单编号(对外)', out_trade_no VARCHAR(50) COMMENT '第三方交易编号', order_type INT COMMENT '订单类型1支出订单2收入订单3未定4支出订单退款', order_type_name VARCHAR(50) COMMENT '订单类型名称', customer_id INT COMMENT '会员编号', customer_name VARCHAR(50) COMMENT '会员名称', card_id INT COMMENT '卡号', card_name VARCHAR(50) COMMENT '卡片名称', pay_type INT COMMENT '付款方式1自营支付宝2网上支付3现场支付4自营微信5网上微信6现场微信', pay_type_name VARCHAR(50) COMMENT '付款方式名称', order_time DATETIME COMMENT '订单生成时间', customer_time DATETIME COMMENT '客户生成时间', org_id INT COMMENT '组织ID', shop_id INT COMMENT '自提档口ID', booth_id INT COMMENT '档口ID', take_time DATETIME COMMENT '受款时间', payment_time DATETIME COMMENT '付款时间'......
```

3. 组织结构表有哪些字段？回答结果胡编乱造；
```python
response = openai.Completion.create(
  model="davinci:ft-meshlake-inc-2023-06-13-12-08-36",
  prompt="组织结构表有哪些字段？",
  temperature=0,
  max_tokens=500,
)

# A. 名称、类型、长度、字节数、数据\n\nB. 名称、类型、长度、字节数\n\nC. 名称、类型、长度\n\nD. 名称、类型\n\n4. 如果要把一个结构体转换成字符串，需要使用的函数是：\n\nA. 数据类型转换函数\n\nB. 数据结构转换函数\n\nC. 数据结构赋值函数\n\nD. 数据结构初始化函数\n\n5. 如果要把一个结构体转换成字符串，需要使用的函数是：\n\nA. 数据类型转换函数\n\nB. 数据结构转换函数\n\nC. 数据结构赋值函数\n\nD. 数据结构初始化函数\n\n6. 如果要把一个结构体转换成字符串，需要使用的函数是：......
```

### 实验二

#### 训练数据

- 数据文件： `data/training_data_2.jsonl`
- 数据说明：将同一张表的信息通过不同的prompt组织成多条记录

#### 模型信息

```json
{
  "object": "fine-tune",
  "id": "ft-O1HJx9nqbRVljFMX1tva28wW",
  "hyperparams": {
    "n_epochs": 15,
    "batch_size": 3,
    "prompt_loss_weight": 0.01,
    "learning_rate_multiplier": 0.3
  },
  "organization_id": "org-hZl4konejUHmNHNCbh9MZwEa",
  "model": "davinci",
  "training_files": [
    {
      "object": "file",
      "id": "file-cyttMQsPlACz0NZlTQmzQ57H",
      "purpose": "fine-tune",
      "filename": "./data/training_data_2.jsonl",
      "bytes": 167625,
      "created_at": 1686802266,
      "status": "processed",
      "status_details": null
    }
  ],
  "validation_files": [],
  "result_files": [
    {
      "object": "file",
      "id": "file-HdAnC71kYFo68Y4HJHw4PRBh",
      "purpose": "fine-tune-results",
      "filename": "compiled_results.csv",
      "bytes": 15957,
      "created_at": 1686803960,
      "status": "processed",
      "status_details": null
    }
  ],
  "created_at": 1686802267,
  "updated_at": 1686803961,
  "status": "succeeded",
  "fine_tuned_model": "davinci:ft-meshlake-inc-2023-06-15-04-39-19"
}
```

#### 模型测试

1. 订单主表的主键是？（瞎编的）
```python
response = openai.Completion.create(
  model="davinci:ft-meshlake-inc-2023-06-15-04-39-19",
  prompt="订单主表的主键是？",
  temperature=0,
  max_tokens=500,
)

#  A. order_id B. order_no C. order_id_no D. order_no_id
```

2. sc_shop（店铺表）的建表语句是？（瞎编的）
```python
response = openai.Completion.create(
  model="davinci:ft-meshlake-inc-2023-06-15-04-39-19",
  prompt="sc_shop（店铺表）的建表语句是？",
  temperature=0,
  max_tokens=500,
)

# create table sc_shop (id int auto_increment comment '自增id', shop_id int comment '店铺id', shop_name varchar(50) comment '店铺名称', type int comment '店铺类型:1-农贸市场2-营业中心3-分公司', address varchar(50) comment '店铺地址', telephone varchar(50) comment '店铺电话', mobile varchar(50) comment '店铺手机', official_websit e varchar(50) comment '官网访账记录', real_websit e varchar(50) comment '第三方网站访账记录', alipay_account varchar(50) comment '支付宝账户', alipay_id varchar(50) comment '支付宝id', amizhong_account varchar(50) comment '微信账户', amizh...
```

3. 订单主表有哪些字段（只返回一个问号）
```python
response = openai.Completion.create(
  model="davinci:ft-meshlake-inc-2023-06-15-04-39-19",
  prompt="订单主表有哪些字段",
  temperature=0,
  max_tokens=500,
)

# ？
```

4. 我需要统计订单退款表中所有退款成功的金额，请使用 mysql 的语法帮我写出SQL语句
```python
response = openai.Completion.create(
  model="davinci:ft-meshlake-inc-2023-06-15-04-39-19",
  prompt="我需要统计订单退款表中所有退款成功的金额，请使用 mysql 的语法帮我写出SQL语句",
  temperature=0,
  max_tokens=500,
)

# ，谢谢！
```

## 疑问

1. fine-tune 的数据集应该如何准备？
