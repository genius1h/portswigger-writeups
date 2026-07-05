# Flask 靶场 - 漏洞复现记录

## 环境信息
- 靶场地址：http://127.0.0.1:5000
- Burp Proxy：127.0.0.1:8080

## 复现清单

### 1. SQL 注入 - 登录绕过
- 路由：/sqli/login

### 2. SQL 注入 - 数字型
- 路由：/sqli/data

### 3. XSS - 反射型
- 路由：/xss/reflected

### 4. XSS - 存储型
- 路由：/xss/stored

### 5. CSRF
- 路由：/csrf/transfer
- PoC 位置：poc/csrf_poc.html

### 6. SSRF
- 路由：/ssrf/fetch

### 7. 命令注入
- 路由：/rce/ping

### 8. 文件上传
- 路由：/upload

### 9. JWT 伪造
- 路由：/jwt/admin
- 弱密钥：secret

### 10. IDOR
- 路由：/idor/profile
