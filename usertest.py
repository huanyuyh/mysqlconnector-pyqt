# 写入账号密码到文件
def save_credentials(username, password, filename="credentials.txt"):
    with open(filename, "w") as file:
        file.write(username + "\n")
        file.write(password + "\n")

# 从文件读取账号密码
def read_credentials(filename="credentials.txt"):
    with open(filename, "r") as file:
        username = file.readline().strip()
        password = file.readline().strip()
        return username, password

# 使用示例
save_credentials("your_username", "your_password")
username, password = read_credentials()
print(f"Username: {username}, Password: {password}")
