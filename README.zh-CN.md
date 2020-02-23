# GPGMail crack

## 1. GPGMail 是什么

GPGMail 是 macOS 上 Mail 应用的一个扩展，它提供了邮件的公钥加密和签名服务。GPGMail 运行在 macOS 下，并且与加密相关的功能事实上是由 GNU Privacy Guard 提供的。

从 GPG Suite 2018.4 版本开始，GPGMail 不再使用免费许可。

## 2. 这个破解是如何运作的

在你键入你的 email 和激活码之后，GPGMail 会以 POST 请求的方式发送一些信息给 `https://v3.paddleapi.com`，这些信息不仅包括你刚刚键入的 email 和激活码，还有你电脑的系统类型和硬件 ID；这个 https 地址很可能是激活服务器。

之后这个所谓的激活服务器会检查收到的信息，并返回成功或者错误。

所以这个 keygen 所做的事情就是就是返回一个成功的结果，不管收到了怎样的 POST 请求。

## 3. 如何使用

由于这个 POST 请求是在 HTTPS 下的，我们必须实施中间人攻击。

### 3.1 导入自签名 SSL 证书

我已经准备好了一个 SSL 证书 `cert-crt.pem` 以及这个证书相对应的私钥 `cert-key.pem`。它们是通过以下命令生成的：

```bash
openssl req -x509 -newkey rsa:4096 -keyout cert-key.pem -out cert-crt.pem -nodes -days 3650 -subj '/CN=v3.paddleapi.com'
```

- PS: 当然如果你不放心，你可以自己生成证书，但务必保证`CN`名为`v3.paddleapi.com`。

现在你必须导入 SSL 证书 `cert-crt.pem` 到你的系统 keychain 中，并且总是信任该证书：

![macOS: Add Certificates](pic0.png)

![macOS: Trust dialog](pic1.png)

### 3.2 将 v3.paddleapi.com 解析到 127.0.0.1

在 `/etc/hosts` 文件中添加一项

```plain
127.0.0.1    v3.paddleapi.com
```

### 3.3 运行 HTTPS 服务器

```bash
sudo ./paddleapi_server.py
```

- 为什么要 `sudo` ?

  建立一个 HTTPS 服务器将会在 443 端口上绑定一个 socket，而这个 443 是小于 1024 的，位于常用端口范围内；在 macOS 系统中，这需要 root 权限。

### 3.4 前往 GPGMail 设置中激活

![macOS: GPGMail Support Plan](pic2.png)

- **注意：** 激活码可以是任何内容，但长度必须在 31~53 之间。

- **注意：** 你可以用 `gen_activation_code.py` 来生成一个随机的激活码。

  ```bash
  ./gen_activation_code.py
  ```

最后应该是像下面这个样子：

![macOS: GPGMail](pic3.png)

### 3.4 关闭 HTTPS 服务器并移除 SSL 证书

按下 `Ctrl + C` 来关闭 HTTPS 服务器.

**考虑到安全原因，建议你移除掉刚刚导入的 SSL 证书。**

### 3.5 恢复 hosts (可选)

如果你愿意的话，你可以在 `/etc/hosts` 中移除之前添加的项

```plain
127.0.0.1    v3.paddleapi.com
```
