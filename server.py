#!/usr/bin/env python3
import http.server
import os
import cgi
from urllib.parse import urlparse

# 设置端口号
PORT = 8000
UPLOAD_DIR = "./statics"  # 上传文件的目录

# 确保上传目录存在
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# 自定义处理器
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 请求的文件路径
        file_path = os.path.join(UPLOAD_DIR, self.path.lstrip("/"))
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # 如果文件存在，则提供文件下载
            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
            return
        else:
            # 如果文件不存在，返回 404
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # 处理文件上传
        if self.path == "/upload":
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                fields = cgi.parse_multipart(self.rfile, pdict)

                # 获取文件数据
                file_data = fields.get('file')[0]
                file_name = fields.get('file_name')[0].decode('utf-8')

                # 将文件保存到 statics 目录
                file_path = os.path.join(UPLOAD_DIR, file_name)
                with open(file_path, 'wb') as f:
                    f.write(file_data)

                # 响应上传结果，并返回下载链接
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"File uploaded successfully. Download link: ")
                self.wfile.write(f"http://localhost:{PORT}/{file_name}".encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Bad request")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


# 启动服务器
def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {PORT}")
    httpd.serve_forever()


# 主函数
if __name__ == "__main__":
    run()
