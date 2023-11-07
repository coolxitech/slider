使用opencv和fastapi写的简单滑块识别接口

代码来源于[SliderCrack](https://github.com/crazyxw/SlideCrack),感谢作者的开源精神
使用fastapi编写HTTP接口，使用uvicorn启动服务

# 接口说明
使用方法：
1. 安装依赖
```bash
pip install -r requirements.txt
```
2. 启动服务
```bash
uvicorn main:app # 需要绑定外网可以添加--host 0.0.0.0
```
3. 访问接口
```bash
http://127.0.0.1:8000/
```
4. 接口返回
```json
{
    "code": 0,
    "msg": "识别成功",
    "data": {
        x轴距离长度
    }
}