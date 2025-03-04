import requests
import time
import qrcode
from datetime import datetime
from PIL import Image
from io import BytesIO

class BossZPSpider:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Referer": "https://www.zhipin.com/web/geek/job",
            "Origin": "https://www.zhipin.com"
        })
        self.session.proxies = {
            # 'http': 'http://127.0.0.1:7890',
            # 'https': 'http://127.0.0.1:7890'
        }

    def get_encrypt_key(self):
        """获取加密密钥（带30秒超时控制）"""
        try:
            resp = self.session.post(
                "https://www.zhipin.com/wapi/zppassport/captcha/randkey",
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 0:
                    return {
                        "qr_id": data["zpData"]["qrId"],
                        "rand_key": data["zpData"]["randKey"],
                        "secret_key": data["zpData"]["secretKey"],
                        "short_rand_key": data["zpData"]["shortRandKey"],
                        "expire_time": datetime.now().timestamp() + 30
                    }
                print(f"获取密钥失败：{data.get('message')}")
                return None
            print(f"HTTP错误码：{resp.status_code}")
            return None
        except requests.exceptions.Timeout:
            print("获取密钥请求超时")
            return None
        except Exception as e:
            print(f"密钥请求异常：{str(e)}")
            return None

    def _generate_jpeg_qrcode(self, url, box_size=10, border=4):
        """内部方法：生成JPEG格式的二维码图片"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=box_size,
                border=border,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=90)
            img_byte_arr.seek(0)
            return img_byte_arr
        except qrcode.exceptions.DataOverflowError:
            print("二维码内容过长，生成失败")
            return None
        except Exception as e:
            print(f"二维码生成失败: {str(e)}")
            return None
    def generate_qrcode(self, encrypt_data):
        """直接获取二维码图片数据（JPEG二进制流）"""
        if not encrypt_data:
            return None

        try:
            # 构造带认证信息的请求头
            headers = {
                "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
                "Referer": "https://www.zhipin.com/sem/10.html?sid=sem_pz_bdpc_dasou_title",
                "Priority": "u=5, i",
                "Sec-Fetch-Dest": "image",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "same-origin"
            }

            # 带cookie请求图片数据
            qr_url = f"https://www.zhipin.com/wapi/zpweixin/qrcode/getqrcode?content={encrypt_data['qr_id']}&w=167&h=167"
            resp = self.session.get(qr_url, headers=headers)

            if resp.status_code != 200:
                print(f"二维码接口HTTP {resp.status_code}")
                return None

            # 验证响应类型
            # if 'image/jpeg' not in resp.headers.get('Content-Type', ''):
            #     print(f"响应类型错误：{resp.headers.get('Content-Type')}")
            #     return None

            # 直接返回二进制数据
            print("成功获取二维码图片数据")
            return BytesIO(resp.content)

        except Exception as e:
            print(f"二维码获取异常：{str(e)}")
            return None
    def check_login_status(self, encrypt_data):
        """检查登录状态（带有效期验证）"""
        if not encrypt_data:
            return None

        status_url = "https://www.zhipin.com/wapi/zppassport/qrcode/scan"
        params = {
            "uuid": encrypt_data["qr_id"],
            "_": int(time.time()*1000)
        }

        print("\n等待扫描二维码（有效期30秒）...")
        while datetime.now().timestamp() < encrypt_data["expire_time"]:
            try:
                resp = self.session.get(status_url, params=params)
                if resp.status_code != 200:
                    print(f"状态接口HTTP {resp.status_code}")
                    time.sleep(2)
                    continue

                status_data = resp.json()
                if status_data.get("code") != 0:
                    print(f"状态检查失败：{status_data.get('message')}")
                    time.sleep(2)
                    continue

                status = status_data["data"]["status"]
                if status == 1:
                    print("\r状态：等待扫码...", end="")
                elif status == 2:
                    print("\r状态：已扫码，请确认登录...", end="")
                elif status == 3:
                    print("\n登录成功！")
                    return status_data["data"]["token"]
                elif status == 4:
                    print("\n二维码已过期")
                    return None

                time.sleep(2)
            except KeyboardInterrupt:
                print("\n用户中断操作")
                return None
            except Exception as e:
                print(f"\n状态检查异常：{str(e)}")
                return None

        print("\n二维码超时未扫描")
        return None

    def run(self):
        # 获取加密参数
        encrypt_data = self.get_encrypt_key()
        if not encrypt_data:
            print("无法获取加密参数，退出")
            return

        # 生成二维码图片
        jpeg_data = self.generate_qrcode(encrypt_data)
        if not jpeg_data:
            print("无法生成二维码，退出")
            return

        # 处理二维码图片
        try:
            # 保存到文件
            with open("boss_login_qr.jpg", "wb") as f:
                f.write(jpeg_data.getvalue())
            print("二维码已保存至 boss_login_qr.jpg")

            # 自动打开图片（仅限支持的系统）
            try:
                img = Image.open(jpeg_data)
                img.show()
            except:
                print("无法自动显示图片，请手动查看保存的文件")

        except Exception as e:
            print(f"文件保存失败：{str(e)}")
            return

        # 检查登录状态
        token = self.check_login_status(encrypt_data)
        if token:
            print(f"获取到访问令牌：{token[:15]}...")  # 部分显示token
            # 这里可以添加后续操作...
        else:
            print("登录流程未完成")

if __name__ == "__main__":
    print("启动BOSS直聘扫码登录...")
    spider = BossZPSpider()
    spider.run()
    print("程序执行结束")

# 到这一步了： 需要再去请求这个 ####Request URL: https://www.zhipin.com/wapi/zppassport/qrcode/scanLogin?qrId=bosszp-ec41f4c2-5ded-4f42-9467-198baf946a44
# 然后再进行一个url获取token: https://www.zhipin.com/wapi/zppassport/qrcode/dispatcher?qrId=bosszp-ec41f4c2-5ded-4f42-9467-198baf946a44&pk=header-login&fp=ggK%2BYo58kMQaOub6h4PcsodLF677r6%2FQNLN%2BSo9nf%2F36a6LtE7ySO9CyTK4f3oNzyxOYonhbIEcyJVVSODOQOjqf5BoRD4JoCrZFnRKzY3Mu59YIJGly62wl%2BbgN5H0e%2BcHvtjpJT3YSHCLvQrStvCYsNIc7zxrSuFpozejh9KxgqcEdxtIm7ft3iOyR373NVRZe6APh%2FZa1anQI8xOOtg%3D%3D
# 最后一个参数指纹， 我不知道该怎么做，
# 找到了app.94d95d9b.js。source里面找到的， 里面还在分析关于PK的逻辑， 还有uuid如何置换成qrid， 逻辑打通后就可以扫码登录了， 不过是否有必要也是另外一回事，
# 毕竟我其实可以进行一个， 浏览器自动化的方式扫码登录， 然后保存token， 进行成操作。 鉴于第一种需要分析算法逻辑， 所以先行第二种， 然后分析第一种
# 第一种失败， 里面有关于混淆技术的破解问题
#
#
# --希望能做一个更好命名的工具， 统一命名， 统一的注释， 统一的代码量去拆分代码