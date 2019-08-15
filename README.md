### 一、准备工作

#### 1.1 安装环境

该工具采用Python开发，因此首先需要安装Python，在此不做赘述。同时，由于采用到第三方Library，因此将需要安装以下依赖：

    $ pipenv install cryptography
    $ pipenv install pycryptodome
    
#### 1.2 更新设置 

openapi.py中定义基础参数，用来生成请求URL，请根据OpenAPI管理方提供的信息，更新`OpenAPI.ini`里的如下变量的值：

```
OPI_APP_ID = ''
OPI_APP_KEY = ''
OPI_APP_PRIVATE_KEY = ''
```

device.py用来请求硬件注册或登录，请根据OpenAPI管理方提供的信息，更新`OpenAPI.ini`里的如下变量的值：

```
DEV_AUTH_DEVICE_KEY = ''
DEV_AUTH_SEED_PREFIX = ''
DEV_AUTH_PRI_KEY = ''
DEV_AUTH_PID = ''
DEV_AUTH_SN = ''
```

合作伙伴可以在硬件注册成功之后，更新`OpenAPI.ini`里的变量`OPI_DEVICE_ID`和`OPI_DEVICE_KEY`，这样可重复使用，不必每次都注册或登录

```
OPI_DEVICE_ID = ''
OPI_DEVICE_KEY = ''
```

auth.py用来记录用户登录的参数，即QQ音乐OpenID登录方案，请根据实际取值来更新`OpenAPI.ini`里的变量：

```
QQMUSIC_OPENID_APPID = ''
QQMUSIC_OPENID_USERID = ''
QQMUSIC_ACCESS_TOKEN = ''
```   

#### 1.3 常见问题

如用户登录信息过期，会发现如下信息，此时需要更新`OpenAPI.ini`里的`QQMUSIC_OPENID_USERID`与`QQMUSIC_ACCESS_TOKEN`。

```json
{
    "ret": 11108,
    "sub_ret": -7,
    "msg": "联合登录下，QQ音乐open账号体系校验失败!"
}
```

如果设备登录信息过期，则会遇到如下信息，此时需要更新`OpenAPI.ini`的`OPI_DEVICE_ID`与`OPI_DEVICE_KEY`，
可以通过"二、硬件接入"来获取。

```json
{"msg":"联合登录下，OPI设备登陆态较验失败!","ret":11105,"sub_ret":1}
``` 
    
### 二、硬件接入

进入到目录下，执行如下操作，假定设备还没有`register`，则首先执行该动作

    $ python -m qqmusic.device.py --cmd=register

即可得到用于注册的URL(以下示例仅供参考，实际执行可能因时效等因素而失败，下同)：

>http://open.music.qq.com/fcgi-bin/fcg_music_custom_third_party_account_auth.fcg?app_id=12345773&app_key=lKdAGpAGeYRkSDwy&timestamp=1561000364&sign=8b5bd3d8abe452fc5afcca5c792c7d04&client_ip=10.68.108.41&third_part_account=19d8732a08bd1635300b9a645f8998ad362de9f39f6512e7914c7f1b82fe74300c22883213e828c7d440c366138c7edb2a22e5a07bdfd6397829cb4e53b4af26bbf2e95f8f22f3713466dc2c70755f5bae29289f6ff7bc30d32907d5269120b7837105cd27ffcb2e49517852176d3aa0bda338b294262954d466ef43c7c555d8d72112a0d992c810562decd14116a135492226617ae375c468e1a7ceaf6df9b4c7a8ba80fbff6f3c7e3e123fbaa9dd5155dbc484398f92349abf27b980ae4bb9b46202beb698d9afed1fca50c0594a104b64cc8ed3141af42728b54a1d9d661feef8e679605c90355908b1da48bac9807851a7c64f649060484182b5a0ecbc2c195c71bd9cf544d7bfc8198b51a3312c6853275906d8d7d76eb8c90c9f36b384cd0edba632ddb1ad8b53d716edd1eeb8&crypto_seed=1561000364&cmd=register

实际上，由于多人/多次执行上述动作，而一个设备ID只需要注册一次，因此当访问上述URL，会遇到提示注册失败的提示：

```json
{
   "msg" : "设备注册/登录失败! 错误提示: ERR_OPI_DEVICE_REGISTER_ALLCOATE_HAS_EXIST",
   "ret" : 101502,
   "sub_ret" : 1201
}
```

上述情况是正常的，因此此时应该执行`login`:

    $ python -m qqmusic.device.py --cmd=login

可以看到URL信息输出：

>http://open.music.qq.com/fcgi-bin/fcg_music_custom_third_party_account_auth.fcg?app_id=12345773&app_key=lKdAGpAGeYRkSDwy&timestamp=1561000930&sign=56b13558ebdc3f70f7f394a188b71867&client_ip=10.68.108.41&third_part_account=40e676aa73022c97459bc78f3333cb98ffa247b45a9a1d7bad75c8a84d606ce06ac37c0cc58b9f27c9c985e6fc1e0e12c88fba80b31aad5e4242b438b0983ed0c9c334fb19fc179636a5caf01fa911e02e047f062f92342815f93899bf46ed5146163d83092a130840f73d0a4d6c454165eecfab8b2c0a78d4e7ea11abfc6e586208870a32d055c7871e5ee69e5624abfba961c99d403e3629f6395ddfcc0cde78ff6381f54e7ecbed94fd9141320a25a011b527fbbd300f5b6209660a2ba489cff803ad4b26a6c1660d3b7df9b28f8b463482c0f07c3852b4ab682b7ade480385bf5b8f1bbb227b8cf9c8009151c2d7dcdde1d39b6b10f25c4d403d4337b57b5ca28e950707772bfbe7a1980b3b349962d11f3f12a75e5da1c567015bae42738cb6d5c7597a3443a9fc5e664ea5178a&crypto_seed=1561000930&cmd=login

访问后，可以得到`device_id`和`device_key`:

```json
{
   "device_id" : 4611692615497320450,
   "device_key" : "EC292C6EE52C09919A897D39FBB13ABDC03DB0D369BBEC52F662C6A912998199",
   "msg" : "ok",
   "ret" : 0,
   "sub_ret" : 0
}
```

### 三、访问OpenAPI

进入到目录下，执行如下操作，

    $ python -m qqmusic.agent.py

可以看到有帮助信息输出：

<pre><samp>usage: agent.py [-h] [--cmd_args [CMD_ARGS [CMD_ARGS ...]]]
                [--qm_app_id QM_APP_ID] [--qm_user_id QM_USER_ID]
                [--qm_token QM_TOKEN] [--opi_dev_id OPI_DEV_ID]
                [--opi_dev_key OPI_DEV_KEY]
                cmd
</samp></pre>

在OpenAPI中，有一些接口，除去公共参数，只需要命令字即可，不需要额外参数，此时运行工具比较简单。

例如，请求个人歌单目录，该情况下不需要`--cmd_args`：

    $ python -m qqmusic.agent.py fcg_music_custom_get_songlist_self.fcg

得到的输出如下：

>http://openrpc.music.qq.com/rpc_proxy/fcgi-bin/music_open_api.fcg?app_id=12345668&app_key=NsJCNxltHFpCkPuUfh&timestamp=1557906465&sign=e3ce30dfc1f4d037561d45adfc2177c3&client_ip=10.68.108.41&qqmusic_open_appid=1&qqmusic_open_id=7793175916240648422&qqmusic_access_token=a122abc6a7c613017876ec3899a79910508ded36268986fcbaf0c7a49061e0d6&opi_cmd=fcg_music_custom_get_songlist_self.fcg&login_type=5&user_login_type=6&device_login_type=4&opi_device_id=4611692615497154630&opi_device_key=3D31FB14B8B9766032690FDDE5091BE8AC5AE8D4AD3AED5D08732CB41DB03778

#### 3.1 使用参数`--cmd_args`

如果请求"我喜欢"的具体内容，即`fcg_music_custom_get_songlist_detail.fcg`，则它需要三个额外的参数`dissid`、`page`、`page_size`。

此时，执行工具是，就需要`--cmd_args`，如下：

    $ python -m qqmusic.agent.py fcg_music_custom_get_songlist_detail.fcg --cmd_args dissid=1142586426 page=1 page_size=5

得到的输出如下：

>http://openrpc.music.qq.com/rpc_proxy/fcgi-bin/music_open_api.fcg?app_id=12345668&app_key=NsJCNxltHFpCkPuUfh&timestamp=1557906740&sign=f97802b6c87f0ca59edd03149e4c5630&client_ip=10.68.108.41&qqmusic_open_appid=1&qqmusic_open_id=7793175916240648422&qqmusic_access_token=a122abc6a7c613017876ec3899a79910508ded36268986fcbaf0c7a49061e0d6&dissid=1142586426&page=1&page_size=5&opi_cmd=fcg_music_custom_get_songlist_detail.fcg&login_type=5&user_login_type=6&device_login_type=4&opi_device_id=4611692615497154630&opi_device_key=3D31FB14B8B9766032690FDDE5091BE8AC5AE8D4AD3AED5D08732CB41DB03778

OpenAPI中有五十多个接口，每一个接口是否需要用到`--cmd_args`，取决于OpenAPI文档的要求。